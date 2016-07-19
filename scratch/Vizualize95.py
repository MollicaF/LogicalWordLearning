'''
For each word and data amount,
    how many hypotheses are in 95% of the mass (by word and by lexicon) and
    what does the probability of their extensions look like?
'''

import pickle
import numpy as np
from Model import *
from Model.Givens import *
from optparse import OptionParser

######################################################################################################
#   Option Parser
######################################################################################################
parser = OptionParser()
parser.add_option("--family", dest='family', type='string', help="What is the target",
                  default='english')
parser.add_option("--space", dest="space", type='string', help="Pickled hypotheses",
                  default='truncated.pkl')
parser.add_option("--out", dest="out_loc", type='string', help="Output file location",
                  default='GibbsEnglish.pkl')
parser.add_option("--size", dest="size", type='int', help='Normaliation data size', default=1000)
parser.add_option("--alpha", dest="alpha", type='float', help='Reliability of a data point', default=0.9)
parser.add_option("--samples", dest="samples", type="int", help="Number of samples desired", default=100000)


(options, args) = parser.parse_args()
######################################################################################################
#   Load Lexicons
######################################################################################################
target = eval(options.family)

# Load in the lexicons
hypothesis_space = []
with open(options.space, 'r') as f:
    hypothesis_space.extend(pickle.load(f))

######################################################################################################
#   Make normalization data
######################################################################################################

'''
makeLexiconData is biased to sample from relationships in proportion to their existence on the tree.
For example, if there are more father relations than uncles on the tree, there should be more father relations
than uncle relations in the sample you get back. makeUniformData is going to return you N of each relationship
with the noise probability conditioned on each word.
'''

def makeUniformData(lexicon, context, n=1000, alpha=0.9):
    output = []
    data = {w : [] for w in lexicon.all_words()}
    trueset = lexicon.make_true_data(context)
    for dp in trueset:
        data[dp[0]].extend([KinshipData(dp[0], dp[1], dp[2], context)])
    gos = int(n * alpha)
    for w in lexicon.all_words():
        for _ in xrange(gos):
            output.append(sample1(data[w]))
        for _ in xrange(n-gos):
            output.append(KinshipData(w, sample1(context.objects), sample1(context.objects), context))
    return output


huge_data = makeLexiconData(target, four_gen_tree_context, n=options.size*len(target.all_words()),
                            alpha=options.alpha, verbose=False)

#huge_data = makeUniformData(target, four_gen_tree_context, n=options.size, alpha=options.alpha)

# Normalize hypotheses
for h in hypothesis_space:
    h.point_likelihood = h.compute_likelihood(huge_data) / float(options.size)

def countMass(hyps, data):
    posterior_score = np.array([h.point_likelihood*data + h.prior for h in hyps])
    u = max(posterior_score)
    Z = u + np.log(sum(np.exp(posterior_score - u )))
    a = np.exp(posterior_score - Z)
    mass = 0
    numHyps = 0
    probs = sorted(a)
    probs.reverse()
    for h in probs:
        if mass < 0.95:
            mass += h
            numHyps += 1
        else:
            return numHyps

for i in range(0, 110, 10):
    print 'Having seen', i, 'data points, there are', countMass(hypothesis_space, 0), 'hypotheses within 95% of the probability mass.'

# Cache hypothesis output
imp_objs = ['Katniss', 'peeta', 'Sabrina', 'frodo', 'merry', 'Brandy', 'Rose', 'Leia', 'han', 'aragorn', 'Arwen',
            'salem', 'Zelda', 'Mellissa', 'joey', 'fabio']
extensions = dict()
for w in target.all_words():
    for h in hypothesis_space:
        h.cached_set = h(w, four_gen_tree_context, set(['Prue']))

    extensions[w] = np.array([[1 * (obj in h.cached_set) for h in hypothesis_space] for obj in imp_objs])


def whereMass(hyps, data, objects=imp_objs):
    posterior_score = np.array([h.point_likelihood * data + h.prior for h in hyps])
    u = max(posterior_score)
    Z = u + np.log(np.sum(np.exp(posterior_score - u)))
    post = np.exp(posterior_score - Z)
    out = [[o for o in objects] + ['Word']]
    for w in target.all_words():
        out.append(list(np.append(np.dot(post, extensions[w].T), w)))
    return out

MAX = 110
MIN = 0
BY  = 10

resultados = []
for s, d in enumerate(range(MIN, MAX, BY)):
    for i, l in enumerate(whereMass(hypothesis_space, d)):
        if i > 0 or s == 0:
            resultados.append([str(s*BY)] + [str(li) for li in l])

out = '\n'.join([','.join(r) for r in resultados])
with open('ObjProbs.csv', 'w') as f:
    f.write(out)