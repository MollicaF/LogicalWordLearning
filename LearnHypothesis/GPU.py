"""

    export THEANO_FLAGS='cuda.root=/usr/local/cudaxx/,device=cpu,floatX=float32,force_device=True' && python GPU.py
"""

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
Rlocal = np.loadtxt('Model_'+ options.model_loc +'.csv', delimiter=',')
Clocal = np.loadtxt('Counts_'+ options.model_loc +'.csv', delimiter=',')
Llocal = np.loadtxt('Likelihoods_'+options.model_loc+'.csv')

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

from theano import function, config, shared, sandbox
import theano.tensor as T
import numpy

# Load stuff onto the GPU

Hlocal = np.array(NYes).reshape((-1, Llocal.shape[1]))
Nlocal = np.array(NTrials).reshape((-1, Llocal.shape[1]))
Rlocal = Rlocal.reshape((Llocal.shape[1], Llocal.shape[0], Hlocal.shape[0]))

L = shared(Llocal, config.floatX)
N = shared(Nlocal, config.floatX)
R = shared(Rlocal, config.floatX)
H = shared(Hlocal, config.floatX)
C = shared(Clocal, config.floatX)

ones = shared(np.ones(Llocal.shape[1]), config.floatX)

t0 = time.time()

X = shared(np.log(dirichlet.rvs(np.ones(30))[0]), config.floatX)

# f1 = function([], sandbox.cuda.basic_ops.gpu_from_host(T.outer(T.dot(C, X), ones) + L))
f1 = function([], T.outer(T.dot(C, X), ones) + L)

posterior_score = shared(f1())
# print type(posterior_score), posterior_score
#
f2 = function([], T.exp(posterior_score-T.log(T.sum(T.exp(posterior_score-T.max(posterior_score, axis=0))))-T.max(posterior_score, axis=0)))  # TODO: u should be columnwise)
posterior = shared(f2())

#
# # print type(posterior), posterior
#

P = shared(np.ones(8), config.floatX)

human_ll = 0
for g in xrange(Llocal.shape[1]):
    f3 = function([], T.dot( posterior.T[g, :], R[g,:]))
    p = f3()

    human_ll += np.sum( np.log(p)*Hlocal[:, g] + np.log(1.-p)*(Nlocal[:,g] - Hlocal[:,g]) )

    # Probably not on gpu
    # human_ll += function([], T.sum( T.log(P)*H[:, g] + T.log(1.-P)*(N[:,g] - H[:,g])) )()

print human_ll
#
t1 = time.time()

print t1-t0



from scipy.optimize import minimize

#
# print "## Loaded all the data and model."
# print "## Starting the ascent!!!"

# best = ([], np.Inf)
# for _ in xrange(1):
#     o = minimize(binomial, np.log(dirichlet.rvs(np.ones(30))[0]))
#     if not o.success: print o.message
#
#     a = np.exp(o.x)
#     a = a / np.sum(a)
#     if binomial(a) < best[1]:
#         best = (a, binomial(np.log(a)))
#
# print best
