import pickle
import numpy as np
from Model import *
from Model.Givens import turkish, english, pukapuka, four_gen_tree_context, four_gen_tree_objs, simple_tree_context
from optparse import OptionParser
from LOTlib.Inference.GrammarInference.Precompute import create_counts

#############################################################################################
#    Option Parser
#############################################################################################
parser = OptionParser()
parser.add_option("--read", dest="filename", type="string", help="Pickled results",
                  default="../LearnLexicon/PukaPuka/Mixing/Mixed2Puka.pkl")
parser.add_option("--family", dest="family", type="string", help="Family", default='pukapuka')
parser.add_option("--data", dest="N", type="int", default=1000,
                  help="If > 0, recomputes the likelihood on a sample of data this size")
parser.add_option("--alpha", dest="alpha", type="int", default=0.90, help="Noise value")

(options, args) = parser.parse_args()

#############################################################################################
#    Functions and Things
#############################################################################################

from scipy.special import beta
def multdir(counts, alpha):
    n  = np.sum(counts, axis=1)
    a0 = np.sum(alpha)
    numerator   = np.log(n * beta(a0, n))
    denominator = [np.sum([np.log(x * beta(a, x)) for x, a in zip(c, alpha) if x > 0]) for c in counts]
    return numerator - denominator

grammar = makeGrammar(four_gen_tree_objs, nterms=['Tree', 'Set', 'Gender', 'Generation'])


def compute_reuse_prior(lex):
    counts = create_counts(grammar, [lex.value[w] for w in lex.all_words()])[0]
    prior =0.0
    for k in counts.keys():
        c = np.sum(counts[k], axis=0)
        prior += multdir([c], np.ones(len(c))/float(len(c)))[0]

    return prior


def do_I_abstract(h):
    return 'X' in [x.name for x in h.value.subnodes()]


with open(options.filename, 'r') as f:
    hyps = list(pickle.load(f))

target = eval(options.family)

#############################################################################################
#    Evaluation Loop
#############################################################################################
results = []
result_strings = []

huge_data = makeLexiconData(target, four_gen_tree_context, n=options.N, alpha=options.alpha, verbose=False)

for s, h in enumerate(hyps):
    h.compute_likelihood(huge_data)
    h.point_ll = h.likelihood / len(huge_data)

Data = np.arange(650) + 1
Likelihood = np.outer(Data, np.array([h.point_ll for h in hyps]))
Prior = np.outer(np.ones(650), np.array([h.prior for h in hyps]))
Posterior = Likelihood + Prior

maxP = np.max(Posterior, axis=1)

Z = np.log(np.sum(np.exp(Posterior - np.outer(maxP,np.ones(Posterior.shape[1]))), axis=1)) + maxP
Posterior = Posterior - np.outer(Z, np.ones(Posterior.shape[1]))

context = four_gen_tree_context

R = np.zeros((len(hyps[0].all_words()), len(hyps), len(context.objects)))

with open('VizPF/key.txt', 'w') as f:
    f.write(','.join(context.objects))

for hi, h in enumerate(hyps):
    for wi, w in enumerate(h.all_words()):
        if do_I_abstract(h.value[w]):
            for oi, o in enumerate(context.objects):
                if o in h.value[w]('foo', context, set(['ego'])):
                    R[wi, hi, oi] = 1.0


for wi, w in enumerate(target.all_words()):
    np.savetxt('VizPF/Simplicity_' + w + '.csv', np.dot(np.exp(Posterior), R[wi]),delimiter=',')


Likelihood = np.outer(Data, np.array([h.point_ll for h in hyps]))
Prior = np.outer(np.ones(650), np.array([compute_reuse_prior(h) for h in hyps]))
Posterior = Likelihood + Prior

maxP = np.max(Posterior, axis=1)

Z = np.log(np.sum(np.exp(Posterior - np.outer(maxP,np.ones(Posterior.shape[1]))), axis=1)) + maxP
Posterior = Posterior - np.outer(Z, np.ones(Posterior.shape[1]))

for wi, w in enumerate(target.all_words()):
    np.savetxt('VizPF/Reuse_' + w + '.csv', np.dot(np.exp(Posterior), R[wi]),delimiter=',')
