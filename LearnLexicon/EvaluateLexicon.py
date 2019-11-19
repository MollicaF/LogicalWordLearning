import pickle
import numpy as np
from Model import *
from Model.Givens import *
from fractions import Fraction
from LOTlib.Miscellaneous import log
from LOTlib.Eval import RecursionDepthException
from LOTlib.Hypotheses.Priors.LZPrior import *
from optparse import OptionParser
from LOTlib.GrammarInference.Precompute import create_counts

#############################################################################################
#    Option Parser
#############################################################################################
parser = OptionParser()
parser.add_option("--read", dest="filename", type="string", help="Pickled results",
                  default="PukaPuka/Mixing/Mixed2Puka.pkl")
parser.add_option("--write", dest="out_path", type="string", help="Results csv",
                  default="Results_PUK.csv")
parser.add_option("--recurse", dest='recurse', action='store_true', help='Should we allow recursion?', default=False)
parser.add_option("--family", dest="family", type="string", help="Family", default='pukapuka')
parser.add_option("--data", dest="N", type="int", default=1000,
                  help="If > 0, recomputes the likelihood on a sample of data this size")
parser.add_option("--alpha", dest="alpha", type="float", default=0.90, help="Noise value")
parser.add_option("--epsilon", dest="epsilon", type="float", default=0.50, help="Ego-centricity")
parser.add_option("--s", dest="s", type="float", default=0.0, help="zipf parameter")
parser.add_option("--datafile", dest="datafile", type='str', default=None, help="Where is the data?")

(options, args) = parser.parse_args()

#############################################################################################
#    Functions and Things
#############################################################################################

target = eval(options.family)

from scipy.special import beta
def multdir(counts, alpha):
    n  = np.sum(counts, axis=1)
    a0 = np.sum(alpha)
    numerator   = np.log(n * beta(a0, n))
    denominator = [np.sum([np.log(x * beta(a, x)) for x, a in zip(c, alpha) if x > 0]) for c in counts]
    return numerator - denominator

if options.recurse:
    grammar = makeGrammar(four_gen_tree_objs, nterms=['Tree', 'Set', 'Gender', 'Generation'],
                          recursive=True, words=target.all_words())
else:
    grammar = makeGrammar(four_gen_tree_objs, nterms=['Tree', 'Set', 'Gender', 'Generation'])


def compute_reuse_prior(lex):
    counts = create_counts(grammar, [lex.value[w] for w in lex.all_words()])[0]
    prior =0.0
    for k in counts.keys():
        c = np.sum(counts[k], axis=0)
        prior += multdir([c], np.ones(len(c))/float(len(c)))[0]

    return prior

def compute_word_ll(word, h, data):
    data = [dp for dp in data if dp.word == word]
    if len(data) == 0:
        return 0
    context = data[0].context
    trueset = set()
    for x in context.objects:
        for y in h('', context, set([x])):  # x must be a set here
            trueset.add((word, x, y))
    all_poss = len(context.objects) ** 2
    ll = 0
    for datum in data:
        if (datum.word, datum.X, datum.Y) in trueset:
            ll += log(options.alpha / len(trueset) + ((1. - options.alpha) / all_poss))
        else:
            ll += log((1. - options.alpha) / all_poss)
    return ll

def compute_Zipf_likelihood(lexicon, data, s):
    constants = dict()
    ll = 0
    for datum in data:
        if datum.context in constants.keys():
            trueset = constants[datum.context][0]
            all_poss = constants[datum.context][1]
            margin = constants[datum.context][2]
        else:
            try:
                if datum.context.ego is None:
                    trueset = {w: lexicon.make_word_data(w, datum.context) for w in lexicon.all_words()}
                else:
                    trueset = {w: lexicon.make_word_data(w, datum.context, fixX=datum.context.ego)
                               for w in lexicon.all_words()}

                all_poss = len(datum.context.objects) ** 2
                all_poss_speakers = set([t[1] for t in trueset])
                margin = float(sum(Fraction(1, d) ** s for d in xrange(1, len(all_poss_speakers) + 1)))
                constants[datum.context] = [trueset, all_poss, margin]
            except RecursionDepthException:
                return -Infinity

        if (datum.word, datum.X, datum.Y) in trueset[datum.word]:
            pS = (datum.context.distance[datum.Y] ** -s ) / margin
            pRgS = (datum.context.distance[datum.Y] ** -s) / sum(
                [(datum.context.distance[ref] ** -s) for ref in lexicon(datum.word, datum.context, set([datum.X]))])
            ll += log(lexicon.alpha * pS * pRgS + ((1. - lexicon.alpha) / all_poss))
        else:
            ll += log((1. - lexicon.alpha) / all_poss)

    return ll / lexicon.likelihood_temperature


def do_I_abstract(h):
    return int( 'X' in [x.name for x in h.value.subnodes()])

def assess_inv_hyp(hypothesis, target_lexicon, context):
    findings = []
    ground_truth = target_lexicon.make_true_data(context)
    hypothesized_lexicon_data = hypothesis.make_true_data(context)
    for w in target_lexicon.all_words():
        abstract = do_I_abstract(hypothesis.value[w])
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
        findings.append([w,                                                                     # Word
                         hypothesis.value[w].compute_prior(),                                   # Hypothesis Prior grammar.log_probability(hypothesis.value[w].value)
                         hypothesis.compute_likelihood(data)/float(len(data)),          # Hypothesis Likelihood
                         hypothesis.prior,                                                      # Lexicon Prior
                         compute_reuse_prior(hypothesis),                                     # Recursive Prior
                         hypothesis.point_ll,                                                   # Lexicon Likelihood
                         #compute_Zipf_likelihood(hypothesis, zipf1data[w], 1)/float(len(data)), # Zipf1 Likelihood
                         #compute_Zipf_likelihood(hypothesis, zipf2data[w], 2)/float(len(data)), # Zipf2 Likelihood
                         #compute_Zipf_likelihood(hypothesis, zipf3data[w], 3)/float(len(data)), # Zipf3 Likelihood
                         correct_count,                                                         # No. Correct Objects
                         len(hypothesized_word_data),                                           # No. Proposed Objects
                         len(true_word_data),
                         abstract])                                                  # No. True Objects
    return findings


with open(options.filename, 'r') as f:
    hyps = pickle.load(f)


#print 'Making all the data . . .'

#############################################################################################
#    Evaluation Loop
#############################################################################################
results = []
result_strings = []

if options.datafile is None:
    huge_data = makeZipfianLexiconData(target, four_gen_tree_context, n=5000, alpha=options.alpha, s=options.s, epsilon=options.epsilon) #options.alpha
    '''
    huge_data = []
    for t in target.make_true_data(four_gen_tree_context, fixX='ego'):
        huge_data.append(KinshipData(t[0],t[1],t[2],four_gen_tree_context))
    for t in target.make_true_data(four_gen_tree_context):
        huge_data.append(KinshipData(t[0], t[1], t[2], four_gen_tree_context))
    '''
else:
    with open(options.datafile, 'r') as f:
        huge_data = pickle.load(f)

#zipf1data = {w: makeZipfianLexiconData(target, w, four_gen_tree_context, n=options.N, s=1, alpha=options.alpha) for
#             w in target.all_words()}
#zipf2data = {w: makeZipfianLexiconData(target, w, four_gen_tree_context, n=options.N, s=2, alpha=options.alpha) for
#             w in target.all_words()}
#zipf3data = {w: makeZipfianLexiconData(target, w, four_gen_tree_context, n=options.N, s=3, alpha=options.alpha) for
#             w in target.all_words()}

for s, h0 in enumerate(hyps):
    h = KinshipLexicon()
    for w in h0.all_words():
        hw = h0.value[w]
        hw.grammar = grammar
        h.set_word(w, hw)
    h.s = options.s
    h.epsilon = options.epsilon
    h.compute_likelihood(huge_data)
    h.point_ll = h.likelihood / len(huge_data)
    for wrd in assess_inv_hyp(h, target, four_gen_tree_context):
        result = [s] + wrd
        result_strings.append(', '.join(str(i) for i in result))
        results.append(result)

print "Writing csv file . . ."
with open(options.out_path, 'w') as f:
    f.write('\n'.join(result_strings))
