import pickle
import numpy as np
from optparse import OptionParser
from Model import *
from Model.Givens import turkish, english, pukapuka, iroquois, four_gen_tree_context, four_gen_tree_objs
from LOTlib.Inference.GrammarInference.Precompute import create_counts
from LOTlib.TopN import TopN

parser = OptionParser()
parser.add_option("--read", dest="filename", type="string", help="Pickled results",
                  default="PukaPuka/Mixing/Mixed2Puka.pkl")
parser.add_option("--read2", dest="filename2", type="string", help="Pickled results",
                  default=None)
parser.add_option("--topN", dest="Nsize", type="int", help="Number of hypotheses to save",
                  default=1000)
parser.add_option("--write", dest="out_path", type="string", help="Results csv",
                  default="Results_PUK.csv")
parser.add_option("--family", dest="family", type="string", help="Family", default='pukapuka')
parser.add_option("--recurse", dest='recurse', action='store_true', help='Should we allow recursion?', default=False)

(options, args) = parser.parse_args()

target = eval(options.family)

if options.recurse:
    grammar = makeGrammar(four_gen_tree_objs, nterms=['Tree', 'Set', 'Gender', 'Generation'],
                          recursive=True, words=target.all_words())
else:
    grammar = makeGrammar(four_gen_tree_objs, nterms=['Tree', 'Set', 'Gender', 'GenerationS', 'Taboo'])

from scipy.special import beta
def multdir(counts, alpha):
    n  = np.sum(counts, axis=1)
    a0 = np.sum(alpha)
    numerator   = np.log(n * beta(a0, n))
    denominator = [np.sum([np.log(x * beta(a, x)) for x, a in zip(c, alpha) if x > 0]) for c in counts]
    return numerator - denominator


def compute_reuse_prior(lex):
    counts = create_counts(grammar, [lex.value[w] for w in lex.all_words()])[0]
    prior =0.0
    for k in counts.keys():
        c = np.sum(counts[k], axis=0)
        prior += multdir([c], np.ones(len(c))/float(len(c)))[0]

    return prior


d = set()

print "Loading Space 1: " + options.filename
with open(options.filename, 'r') as f:
    d.update(pickle.load(f))

if options.filename2 is not None:
    print "Loading Space 2: " + options.filename2
    with open(options.filename2, 'r') as f:
        d.update(pickle.load(f))

Mass = set()

for a in range(1, 25, 2) + range(25, 251, 25):
    print "Grabbing Top " + str(options.Nsize) + " from " + str(a) + ' dp'
    data = makeZipfianLexiconData(target, four_gen_tree_context, n=a, alpha=0.9, s=0.0, epsilon=0.0)
    simplicity_mass = TopN(N=options.Nsize)
    reuse_mass = TopN(N=options.Nsize)
    for h in d:
        h.posterior_score = h.compute_likelihood(data) + compute_reuse_prior(h)
        reuse_mass.add(h)
        h.compute_posterior(data)
        simplicity_mass.add(h)
    Mass.update(simplicity_mass)
    Mass.update(reuse_mass)


print "Writing output file for " + str(len(Mass)) + ' hypotheses.'
with open(options.out_path, 'w') as f:
    pickle.dump(Mass, f)

