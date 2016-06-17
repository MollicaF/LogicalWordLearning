from optparse import OptionParser
import numpy as np
from numpy import dot, outer
from scipy.misc import factorial

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
R = np.loadtxt('Viz/Model_'+ options.model_loc +'.csv', delimiter=',')
C = np.loadtxt('Viz/Counts_'+ options.model_loc +'.csv', delimiter=',')
L = np.loadtxt('Viz/Likelihoods_'+options.model_loc+'.csv')

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


H = np.array(NYes).reshape((-1, L.shape[1]))
N = np.array(NTrials).reshape((-1, L.shape[1]))
R = R.reshape((L.shape[1], L.shape[0], H.shape[0]))

def logpmf(X, N, P):
    return np.log(P)*X + np.log(1-P)*(N-X)

def realogpmf(X, N, P):
    return np.log(factorial(N)/(factorial(X)*factorial(N-X))) + np.log(P)*X + np.log(1-P)*(N-X)

def binomial(X):
    post = outer(dot(C, X), np.ones(L.shape[1])) + L
    u = np.max(post, axis=0)
    Z = u + np.log(np.sum(np.exp(post-u)))
    post = np.exp(post - Z)
    p = 0
    for g in xrange(L.shape[1]):
        pred = dot(post.T[g, :], R[g,:])
        p += np.sum(logpmf(H[:, g], N[:, g], pred))
    print p
    return -1*p

from scipy.optimize import minimize
from scipy.stats import dirichlet

print "## Loaded all the data and model."
print "## Starting the ascent!!!"

best = ([], np.Inf)
for _ in xrange(1):
    o = minimize(binomial, np.log(dirichlet.rvs(np.ones(30))[0]))
    if not o.success: print o.message

    a = np.exp(o.x)
    a = a / np.sum(a)
    if binomial(a) < best[1]:
        best = (a, binomial(np.log(a)))

print best
