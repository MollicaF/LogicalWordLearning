"""
export THEANO_FLAGS='cuda.root=/usr/local/cuda/,device=gpu,floatX=float32,force_device=True,warn_float64=pdb' && python GPU.py
"""
floatX = 'float32'

from optparse import OptionParser
import numpy as np
from numpy import dot, outer
from scipy.misc import factorial
from copy import copy
from scipy.stats import dirichlet, norm, gamma, beta
import time
from LOTlib.Miscellaneous import sample1, flip

######################################################################################################
#   Option Parser
######################################################################################################
parser = OptionParser()
parser.add_option("--human", dest='data_loc', type='string', help="Generalization Data location",
                  default='human.data')
parser.add_option("--model", dest="model_loc", type='string', help="Model Data Code Name",
                  default='FullSpace')
parser.add_option("--samples", dest="samples", type="int", default=1000, help="Number of samples desired")
parser.add_option("--skip", dest="skip", type="int", default=100, help="Number of samples desired")

(options, args) = parser.parse_args()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Load the model
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Rlocal = np.loadtxt('Model_'+ options.model_loc +'.csv', delimiter=',', dtype=floatX)
Clocal = np.loadtxt('Counts_'+ options.model_loc +'.csv', delimiter=',', dtype=floatX)
Llocal = np.loadtxt('Likelihoods_'+options.model_loc+'.csv', dtype=floatX)

print "# Model loaded"

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Load the human data
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

NYes = []
NTrials = []

d = np.genfromtxt(options.data_loc, dtype=None, delimiter=',')

for i, entry in enumerate(d):
    if i < 1:
        order = entry
    else:
        for j in xrange(5, len(entry)):  # for each predictive response
            if entry[j] not in ('NA', 'NA\n'):
                NYes.append(int(entry[j]))
                NTrials.append(int(entry[4]))

print "# Loaded human data"

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GPU Graph
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from theano import function, config, shared, sandbox, scan, gradient
import theano.tensor as T

import theano
theano.config.floatX=floatX
config.floatX=floatX

# Load stuff onto the GPU

Hlocal = np.array(NYes, dtype=floatX).reshape((-1, Llocal.shape[1]))
Nlocal = np.array(NTrials, dtype=floatX).reshape((-1, Llocal.shape[1]))
Rlocal = Rlocal.reshape((Llocal.shape[1], Llocal.shape[0], Hlocal.shape[0]))

L = shared(Llocal, config.floatX)
N = shared(Nlocal, config.floatX)
R = shared(Rlocal, config.floatX)
H = shared(Hlocal, config.floatX)
C = shared(Clocal, config.floatX)

ones = shared(np.ones(Llocal.shape[1], dtype=floatX), config.floatX)

# Define tensor variables
if floatX=='float32': 
    X = T.fvector("X")
    llt = T.fscalar("llt")
    pt = T.fscalar("pt")
if floatX=='float64': 
    X = T.dvector("X")
    llt = T.dscalar("llt")
    pt = T.dscalar("pt")

# Define the graph
posterior_score = T.outer(T.dot(C, T.log(X))/pt, ones) + L/llt

posterior = T.exp(posterior_score-T.log(T.sum(T.exp(posterior_score-T.max(posterior_score, axis=0)), axis=0))-T.max(posterior_score, axis=0))

def binom(g, ll):
    p = T.dot(posterior.T[g, :], R[g, :])
    p = 0.0001 + 0.9998 * p
    return ll + T.sum(T.log(p) * H[:, g] + T.log(1. - p) * (N[:, g] - H[:, g]))

seq = T.arange(45)
scan_results, scan_updates = scan(fn=binom,
                                  outputs_info=T.as_tensor_variable(np.asarray(0, config.floatX)),
                                  sequences=seq)
positive_ll = scan_results[-1] + T.sum(X) - 2*((llt-1)**2) - 2*((pt-1)**2)

human_ll = function(inputs=[X, llt, pt], outputs=positive_ll)

def last(val, llt, ptt):
    x  = np.array(val, dtype=config.floatX)
    lt = np.array(llt, dtype=config.floatX)
    pt = np.array(ptt, dtype=config.floatX)
    a = human_ll(x,lt,pt)
    return np.array(a, dtype='float64')

gyx = gradient.jacobian(positive_ll, X)
gyl = gradient.jacobian(positive_ll, llt)
gyp = gradient.jacobian(positive_ll, pt)

human_grad = function(inputs=[X, llt, pt], outputs=[gyx, gyl, gyp])

print "## Loaded all the data and model."

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Proposer
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def propose(value, llt, pt, proposal_scale=10000, SMOOTHING=1e-6, sd=0.5):
    if flip(0.8):
        ret = copy(value)

        if len(value) == 1: return ret, 0.0  # handle singleton rules

        inx = sample1(range(0, len(value)))

        ret[inx] = np.random.beta(value[inx] * proposal_scale,
                                  proposal_scale - value[inx] * proposal_scale)

        # add a tiny bit of smoothing away from 0/1
        #ret[inx] = (1.0 - SMOOTHING) * ret[inx] + SMOOTHING / 2.0

        ret = ret / sum(ret)
        '''
        ret[inx] = np.random.gamma(value[inx] * proposal_scale, 1./proposal_scale)
        fb = gamma.logpdf(ret[inx], value[inx] * proposal_scale, 1./proposal_scale) + gamma.logpdf(v, 1) - \
             gamma.logpdf(value[inx], ret[inx] * proposal_scale, 1./proposal_scale) - gamma.logpdf(1, v)
        fb = sum(gamma.logpdf(ret, value)) + gamma.logpdf(v, 1) - \
             sum(gamma.logpdf(value, ret)) - gamma.logpdf(1, v)
        '''
        fb = beta.logpdf(ret[inx], value[inx] * proposal_scale, proposal_scale - value[inx] * proposal_scale) - \
             beta.logpdf(value[inx], ret[inx] * proposal_scale, proposal_scale - ret[inx] * proposal_scale)

        return ret, llt, pt, fb
    else:
        ret_lt = np.random.normal(llt, sd)
        ret_pt = np.random.normal(llt, sd)

        if ret_lt <= 0 or ret_pt <=0:
            fb = -np.Infinity
        else:
            fb = sum([norm.logpdf(ret_lt, llt, sd), norm.logpdf(ret_pt, pt, sd)]) - \
                 sum([norm.logpdf(llt, ret_lt, sd), norm.logpdf(pt, ret_pt, sd)])

    return value, ret_lt, ret_pt, fb


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Runtime Code
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print "## Starting the ascent!!!"

Nsamples = options.samples

#  Initialize values
current_value, current_lt, current_pt = dirichlet.rvs(np.ones(30))[0], 1., 1.
current_likelihood = last(current_value, current_lt, current_pt)

samples = []
acc_count = 0.
for s, n in enumerate(xrange(Nsamples)):
    proposal_val, proposal_lt, proposal_pt, fb = propose(current_value, current_lt, current_pt)
    proposal_likelihood = last(proposal_val, proposal_lt, proposal_pt)
    if flip(np.exp(proposal_likelihood - current_likelihood + fb)):
        acc_count += 1.
        current_likelihood, current_value, current_lt, current_pt = proposal_likelihood, proposal_val, proposal_lt, proposal_pt
        if s % options.skip == 0:
            samples.append((current_likelihood, current_value, current_lt, current_pt))
            print acc_count/(s+1), samples[-1]
    else:
        if s % options.skip == 0:
            samples.append((current_likelihood, current_value, current_lt, current_pt))
            print acc_count / (s+1), samples[-1]

import pickle
with open('hahaha.pkl', 'w') as f:
    pickle.dump(samples, f)

'''
best = np.zeros((Nsamples, 33))
for i in xrange(Nsamples):
    print 'Starting run', i
    inp =
    o = minimize(last, , jac=human_ll_grad, bounds=bounds)
    if not o.success: print o.message
    else:
        print 'Gradient', human_ll_grad(o.x)
        a = np.exp(o.x)
        a = a / np.sum(a)
        best[i,:] = np.append(a, -1*last(o.x))

np.savetxt('SamplesMANGO.csv',best,delimiter=',')

print 'Finished!'
'''