"""
export THEANO_FLAGS='cuda.root=/usr/local/cuda/,device=gpu,floatX=float32,force_device=True,warn_float64=pdb' && python GPU.py
"""
floatX = 'float32'

from optparse import OptionParser
import numpy as np
from numpy import dot, outer
from scipy.misc import factorial
from scipy.stats import dirichlet, norm
import time

######################################################################################################
#   Option Parser
######################################################################################################
parser = OptionParser()
parser.add_option("--human", dest='data_loc', type='string', help="Generalization Data location",
                  default='human.data')
parser.add_option("--model", dest="model_loc", type='string', help="Model Data Code Name",
                  default='FullSpace')
parser.add_option("--samples", dest="samples", type="int", default=1, help="Number of samples desired")

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
# GPU
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
posterior_score = T.outer(T.dot(C, X)/pt, ones) + L/llt

posterior = T.exp(posterior_score-T.log(T.sum(T.exp(posterior_score-T.max(posterior_score, axis=0)), axis=0))-T.max(posterior_score, axis=0))

def binom(g, ll):
    p = T.dot(posterior.T[g,:], R[g, :])
    p = 0.0001 + 0.9998 * p
    return ll + T.sum(T.log(p) * H[:, g] + T.log(1. - p) * (N[:, g] - H[:, g]))

seq = T.arange(45)
scan_results, scan_updates = scan(fn=binom,
                                  outputs_info=T.as_tensor_variable(np.asarray(0, config.floatX)),
                                  sequences=seq)
positive_ll = -1.*(scan_results[-1] + T.sum(X) - 2*((llt-1)**2) - 2*((pt-1)**2))

human_ll = function(inputs=[X, llt, pt], outputs=positive_ll)

def last(params):
    x  = np.array(params[0:30], dtype=config.floatX)
    lt = np.array(params[30], dtype=config.floatX)
    pt = np.array(params[31], dtype=config.floatX)
    a  = human_ll(x,lt,pt)
    print a
    return np.array(a, dtype="float64")

gyx = gradient.jacobian(positive_ll, X)
gyl = gradient.jacobian(positive_ll, llt)
gyp = gradient.jacobian(positive_ll, pt)

human_grad = function(inputs=[X, llt, pt], outputs=[gyx, gyl, gyp])


def human_ll_grad(x):
    a  = np.array(x[0:30], dtype=config.floatX)
    lt = np.array(x[30], dtype=config.floatX)
    pt = np.array(x[31], dtype=config.floatX)
    res = human_grad(a,lt,pt)
    res = np.append(np.append(res[0], res[1]), res[2])
    print res
    return np.array(res, dtype="float64")


from scipy.optimize import minimize, fmin_tnc

bounds = [(-np.inf, np.inf)] * 30 + [(0, np.inf)]*2

print "## Loaded all the data and model."
print "## Starting the ascent!!!"

Nsamples = 1

best = np.zeros((Nsamples, 33))
for i in xrange(Nsamples):
    print 'Starting run', i
    inp = dirichlet.rvs(np.ones(30))[0]
    o = minimize(last, np.append(np.log(inp, dtype=config.floatX), [1.1, 1.2]), jac=human_ll_grad, bounds=bounds, method="CG")
    if not o.success: print o.message
    else:
	print 'Gradient', human_ll_grad(o.x)
        a = np.exp(o.x)
        a = a / np.sum(a)
        best[i,:] = np.append(a, -1*last(o.x))

np.savetxt('SamplesMANGO.csv',best,delimiter=',')

print 'Finished!'
