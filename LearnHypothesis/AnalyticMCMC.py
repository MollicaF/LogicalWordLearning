import pickle
from Model import *
from optparse import OptionParser
import numpy

######################################################################################################
#   Option Parser
######################################################################################################
parser = OptionParser()
parser.add_option("--human", dest='data_loc', type='string', help="Generalization Data location",
                  default='human.data')
parser.add_option("--space", dest='space_loc', type='string', help="Hypothesis Space location",
                  default='Emmaneal.pkl')
parser.add_option("--out", dest="out_path", type="string", help="Output file (a csv of samples)",
                  default="Profile")
parser.add_option("--viz", dest="viz", action="store_true", help="Make Vizualization Files?")
parser.add_option("--samples", dest="samples", type="int", default=1000, help="Number of samples desired")

(options, args) = parser.parse_args()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Define the grammar
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from Model.Givens import simple_tree_objs

grammar = makeGrammar(simple_tree_objs, nterms=['Tree', 'Set', 'Gender', 'Generation', 'Ancestry', 'Paternity'])

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Load the hypotheses
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''
with open(options.space_loc, 'r') as f:
    hypotheses = list(pickle.load(f))

print "# Loaded hypotheses: ", len(hypotheses)
'''

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Load the human data
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from Model.Givens import simple_tree_context

L = []  # each hypothesis's cumulative likelihood to each data point
GroupLength = []
NYes = []
NTrials = []
Output = []

'''
# cache the set for each hypothesis
for h in hypotheses:
    h.cached_set = h('Word', simple_tree_context, set(['ego']))
'''

with open(options.data_loc, 'r') as f:
    for i, line in enumerate(f.readlines()):
        entry = line.strip('\n').split(',')
        if i < 1:
            order = entry
        else:
            #data = [KinshipData('Word', 'ego', entry[2], simple_tree_context),
            #        KinshipData('Word', 'ego', entry[3], simple_tree_context)]
            #L.append([h.compute_likelihood(data) for h in hypotheses])
            #gl = 0
            for j in xrange(5, len(entry)):  # for each predictive response
                if entry[j] not in ('NA', 'NA\n'):
                    NYes.append(int(entry[j]))
                    NTrials.append(int(entry[4]))
                    #Output.append([1 * (order[j] in h.cached_set) for h in hypotheses])
                    #gl += 1
            #GroupLength.append(gl)

print "# Loaded %s observed rows" % len(NYes)
print "# Organized %s groups" % len(GroupLength)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Get the rule count matrices
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''
from LOTlib.Inference.GrammarInference import create_counts

# Decide which rules to use
which_rules = [r for r in grammar if r.nt in ['SET']]

counts, sig2idx, prior_offset = create_counts(grammar, hypotheses, which_rules=which_rules)

print "# Computed counts for each hypothesis & nonterminal"
'''
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Make model files for vizualization
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if options.viz:
    numpy.savetxt('Viz/Likelihoods_' + options.out_path + '.csv', numpy.array(L).T)

    with open('Viz/Model_' + options.out_path + '.csv', 'w') as f:
        f.writelines('\n'.join([','.join([str(r) for r in h]) for h in numpy.array(Output).T]))

    with open('Viz/Counts_' + options.out_path + '.csv', 'w') as f:
        f.writelines('\n'.join([','.join([str(r) for r in h]) for h in counts['SET']]))

    for r in which_rules: print r

from numpy import dot, outer

Output = numpy.loadtxt('Viz/Model_FullSpace.csv', delimiter=',')
counts = {'SET': numpy.loadtxt('Viz/Counts_FullSpace.csv', delimiter=',')}
L = numpy.loadtxt('Viz/Likelihoods_FullSpace.csv')

R = numpy.array(Output)
C = counts['SET']
L = numpy.array(L)
H = numpy.array(NYes).reshape((-1, L.shape[1]))
N = numpy.array(NTrials).reshape((-1, L.shape[1]))

R = R.reshape((L.shape[1], L.shape[0], H.shape[0]))

from scipy.misc import factorial
def logpmf(X, N, P):
    return numpy.log((factorial(N)/(factorial(X)*factorial(N-X))) * P**X * (1-P)**(N-X))

def binomial(X):
    post = outer(dot(C, X), numpy.ones(L.shape[1])) + L
    u = numpy.max(post)
    Z = u + numpy.log(numpy.sum(numpy.exp(post-u)))
    post = numpy.exp(post - Z)
    p = 0
    for g in xrange(L.shape[1]):
        pred = dot(post.T[g, :], R[g,:])
        #p += numpy.sum(binom.logpmf(H[:, g], N[:, g], pred))
        p += numpy.sum(logpmf(H[:, g], N[:, g], pred))
    return -1*p

from scipy.optimize import minimize
from scipy.stats import dirichlet

best = ([], numpy.Inf)
for _ in xrange(10):
    o = minimize(binomial, dirichlet.rvs(numpy.ones(30))[0], bounds=[(0, numpy.Inf)]*30)
    if not o.success: print o.message

    a = o.x + abs(numpy.min(o.x))
    a = a / numpy.sum(a)
    if binomial(a) < best[1]:
        best = (a, binomial(a))

print best