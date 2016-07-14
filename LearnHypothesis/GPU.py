"""
export THEANO_FLAGS='cuda.root=/usr/local/cuda/,device=gpu,floatX=float32,force_device=True,warn_float64=pdb' && python GPU.py
"""
floatX = 'float32'

from optparse import OptionParser
import numpy as np
from numpy import dot, outer
from scipy.misc import factorial
from scipy.stats import dirichlet
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
if floatX=='float32': X = T.fvector("X")
if floatX=='float64': X = T.dvector("X")

# Define the graph
posterior_score = T.outer(T.dot(C, X), ones) + L

posterior = T.exp(posterior_score-T.log(T.sum(T.exp(posterior_score-T.max(posterior_score, axis=0)), axis=0))-T.max(posterior_score, axis=0))

def binom(g, ll):
    p = T.dot(posterior.T[g, :], R[g, :])
    p = 0.0001 + 0.9998 * p
    return ll + T.sum(T.log(p) * H[:, g] + T.log(1. - p) * (N[:, g] - H[:, g]))

seq = T.arange(45)
scan_results, scan_updates = scan(fn=binom,
                                  outputs_info=T.as_tensor_variable(np.asarray(0, config.floatX)),
                                  sequences=seq)
positive_ll = -1.*scan_results[-1]

human_ll = function(inputs=[X], outputs=positive_ll)

def last(x):
    #t0 = time.time()
    return human_ll(np.array(x, dtype=config.floatX))
    #print a, time.time() - t0
    #return a

gy = gradient.jacobian(positive_ll, X)

human_grad = function(inputs=[X], outputs=gy)
#t0 = time.time()
#print human_grad(np.ones(30, dtype=config.floatX)/30.), time.time() - t0


def human_ll_grad(x):
    #t0 = time.time()
    return human_grad(np.array(x, dtype=config.floatX))
    #print 'Jacobian', time.time() - t0
    #return a

from scipy.optimize import minimize, fmin_tnc

print "## Loaded all the data and model."
print "## Starting the ascent!!!"

Nsamples = 250

best = np.zeros((Nsamples, 31))
for i in xrange(Nsamples):
    print 'Starting run', i
    inp = dirichlet.rvs(np.ones(30))[0] #np.ones(30, dtype=config.floatX)/30.
    #o = minimize(last, np.log(inp, dtype=config.floatX), jac=human_ll_grad, method='BFGS', options={'disp':True})
    o = minimize(last, np.log(inp, dtype=config.floatX), jac=human_ll_grad, method="SLSQP", options={'ftol':1e-6})
    if not o.success: print o.message
    else:
        a = np.exp(o.x)
        #print a
        a = a / np.sum(a)
        best[i,:] = np.append(a, -1*last(a))


np.savetxt('SamplesBANANA.csv',best,delimiter=',')

print 'Finished!'
