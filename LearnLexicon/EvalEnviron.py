import pickle
import numpy as np
from Model import *
from Model.Givens import *
from scipy.special import beta
from optparse import OptionParser
from LOTlib.Inference.GrammarInference.Precompute import create_counts

#############################################################################################
#    Option Parser
#############################################################################################
parser = OptionParser()
parser.add_option("--read", dest="filename", type="string", help="Pickled results",
                  default="PKL/fsENG.pkl")
parser.add_option("--write", dest="out_path", type="string", help="Results csv",
                  default="results.csv")
parser.add_option("--recurse", dest='recurse', action='store_true', help='Should we allow recursion?', default=False)
parser.add_option("--family", dest="family", type="string", help="Family", default='english')
parser.add_option("--data", dest="N", type="int", default=10000,
                  help="If > 0, recomputes the likelihood on a sample of data this size")
parser.add_option("--alpha", dest="alpha", type="float", default=0.90, help="Noise value")
parser.add_option("--epsilon", dest="epsilon", type="float", default=0.0, help="Ego-centricity")
parser.add_option("--s", dest="s", type="float", default=0., help="zipf parameter")
parser.add_option("--datafile", dest="datafile", type='str', default=None, help="Where is the data?")

(options, args) = parser.parse_args()

#############################################################################################
#    Functions and Things
#############################################################################################
target = eval(options.family)
ground_truth = target.make_true_data(four_gen_tree_context)

if options.recurse:
    grammar = makeGrammar(four_gen_tree_objs, nterms=['Tree', 'Set', 'Gender', 'Generation'],
                          recursive=True, words=target.all_words())
else:
    grammar = makeGrammar(four_gen_tree_objs, nterms=['Tree', 'Set', 'Gender', 'Generation'])

if options.datafile is None:
    if options.family=='english':
        huge_data = makeZipfianLexiconData(target, four_gen_tree_context,
                                           dfreq=engFreq,
                                           n=options.N,
                                           alpha=options.alpha,
                                           s=options.s,
                                           epsilon=options.epsilon)
    else:
        huge_data = makeZipfianLexiconData(target, four_gen_tree_context,
                                           n=options.N,
                                           alpha=options.alpha,
                                           s=options.s,
                                           epsilon=options.epsilon)
else:
    with open(options.datafile, 'r') as f:
        huge_data = pickle.load(f)


def multdir(counts, alpha):
    n = np.sum(counts, axis=1)
    a0 = np.sum(alpha)
    numerator = np.log(n * beta(a0, n))
    denominator = [np.sum([np.log(x * beta(a, x)) for x, a in zip(c, alpha) if x > 0]) for c in counts]
    return numerator - denominator


def compute_reuse_prior(lex):
    counts = create_counts(grammar, [lex.value[w] for w in lex.all_words()])[0]
    prior = 0.0
    for k in counts.keys():
        c = np.sum(counts[k], axis=0)
        prior += multdir([c], np.ones(len(c))/float(len(c)))[0]

    return prior


def do_I_abstract(h):
    return int( 'X' in [x.name for x in h.value.subnodes()])


def do_I_recurse(h):
    return int( 'recurse_' in [x.name for x in h.value.subnodes()])


def assess_inv_hyp(hypothesis, target_lexicon, context):
    findings = []
    hypothesized_lexicon_data = hypothesis.make_true_data(context)
    for w in target_lexicon.all_words():
        data = [dp for dp in huge_data if dp.word == w]
        hypothesized_word_data = set()
        for dp in hypothesized_lexicon_data:
            if dp[0] == w:
                hypothesized_word_data.add(dp)
        true_word_data = set()
        for dp in ground_truth:
            if dp[0] == w:
                true_word_data.add(dp)
        correct_count = 0
        for dp in hypothesized_word_data:
            if dp in true_word_data:
                correct_count += 1
        findings.append([w,  # Word
                         hypothesis.value[w].compute_prior(),  # Hypothesis Prior
                         hypothesis.compute_likelihood(data, eval=True)/float(len(data)),  # Hypothesis Likelihood
                         hypothesis.compute_prior(),  # Lexicon Prior
                         compute_reuse_prior(hypothesis),  # Recursive Prior
                         hypothesis.point_ll,  # Lexicon Likelihood
                         correct_count,  # No. Correct Objects
                         len(hypothesized_word_data),  # No. Proposed Objects
                         len(true_word_data),  # No. True Objects
                         do_I_abstract(hypothesis.value[w]),  # Abstraction?
                         do_I_recurse(hypothesis.value[w]),  # Recursion?
                         str(h.value[w])])  # Hypothesis
        print findings[-1]
    return findings


print "Loading the data"
with open(options.filename, 'r') as f:
    hyps = pickle.load(f)

print "Loaded %s hypotheses" % (len(hyps))
#############################################################################################
#    Evaluation Loop
#############################################################################################
results = []
result_strings = []

for s, h0 in enumerate(hyps):
    h = KinshipLexicon(alpha=options.alpha, epsilon=options.epsilon, s=options.s)
    for w in h0.all_words():
        h0.value[w].grammar = grammar
        h.set_word(w, h0.value[w])
    h.compute_likelihood(huge_data, eval=True)
    h.point_ll = h.likelihood / len(huge_data)
    for wrd in assess_inv_hyp(h, target, four_gen_tree_context):
        result = [s] + wrd
        result_strings.append(', '.join(str(i) for i in result))
        results.append(result)

print "Writing csv file . . ."
with open(options.out_path, 'w') as f:
    f.write('\n'.join(result_strings))