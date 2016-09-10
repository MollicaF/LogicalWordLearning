import pickle
import numpy as np
from Model import *
from Model.Givens import turkish, english, pukapuka, four_gen_tree_context, four_gen_tree_objs
from fractions import Fraction
from LOTlib.Miscellaneous import log
from LOTlib.Eval import RecursionDepthException
from LOTlib.Hypotheses.Priors.LZPrior import *
from optparse import OptionParser
from LOTlib.Inference.GrammarInference.Precompute import create_counts
#from progressbar import ProgressBar

#############################################################################################
#    Option Parser
#############################################################################################
parser = OptionParser()
parser.add_option("--read", dest="filename", type="string", help="Pickled results",
                  default="PukaPuka/Mixing/Mixed2Puka.pkl")
parser.add_option("--write", dest="out_path", type="string", help="Results csv",
                  default="Results_PUK.csv")
parser.add_option("--family", dest="family", type="string", help="Family", default='pukapuka')
parser.add_option("--data", dest="N", type="int", default=1000,
                  help="If > 0, recomputes the likelihood on a sample of data this size")
parser.add_option("--alpha", dest="alpha", type="int", default=0.90, help="Noise value")

(options, args) = parser.parse_args()

#############################################################################################
#    Functions and Things
#############################################################################################

# For the Zipfian learner we assume egocentrism around peeta

four_gen_tree_context.distance = {'Amanda': 6, 'Anne': 33, 'aragorn': 9, 'Arwen': 14, 'Brandy': 13, 'Celebrindal': 37,
             'Clarice': 18, 'elrond': 36, 'Eowyn': 21, 'fabio': 29, 'fred': 32, 'frodo': 4, 'Galadriel': 35,
             'gandalf': 34, 'han': 22, 'harry': 15, 'Hermione': 8, 'gary': 17, 'james': 30, 'joey': 28,
             'Katniss': 2, 'legolas': 26, 'Leia': 25, 'Lily': 31, 'luke': 23, 'Luna': 27, 'Mellissa': 19, 'merry': 10,
             'Padme': 24,'peeta': 1, 'Prue': 5, 'ron': 20, 'Rose': 11, 'Sabrina': 3, 'salem': 16, 'sam': 12, 'Zelda': 7}

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


def assess_inv_hyp(hypothesis, target_lexicon, context):
    findings = []
    ground_truth = target_lexicon.make_true_data(context)
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
        findings.append([w,                                                                     # Word
                         hypothesis.value[w].compute_prior(),                                   # Hypothesis Prior
                         hypothesis.compute_word_likelihood(data, w)/float(len(data)),          # Hypothesis Likelihood
                         hypothesis.prior,                                                      # Lexicon Prior
                         compute_reuse_prior(hypothesis),                                     # Recursive Prior
                         hypothesis.point_ll,                                                   # Lexicon Likelihood
                         #compute_Zipf_likelihood(hypothesis, zipf1data[w], 1)/float(len(data)), # Zipf1 Likelihood
                         #compute_Zipf_likelihood(hypothesis, zipf2data[w], 2)/float(len(data)), # Zipf2 Likelihood
                         #compute_Zipf_likelihood(hypothesis, zipf3data[w], 3)/float(len(data)), # Zipf3 Likelihood
                         correct_count,                                                         # No. Correct Objects
                         len(hypothesized_word_data),                                           # No. Proposed Objects
                         len(true_word_data)])                                                  # No. True Objects
    return findings


with open(options.filename, 'r') as f:
    hyps = pickle.load(f)

target = eval(options.family)

#print 'Making all the data . . .'

#############################################################################################
#    Evaluation Loop
#############################################################################################
results = []
result_strings = []

huge_data = makeLexiconData(target, four_gen_tree_context, n=options.N, alpha=options.alpha, verbose=False)

#zipf1data = {w: makeZipfianLexiconData(target, w, four_gen_tree_context, n=options.N, s=1, alpha=options.alpha) for
#             w in target.all_words()}
#zipf2data = {w: makeZipfianLexiconData(target, w, four_gen_tree_context, n=options.N, s=2, alpha=options.alpha) for
#             w in target.all_words()}
#zipf3data = {w: makeZipfianLexiconData(target, w, four_gen_tree_context, n=options.N, s=3, alpha=options.alpha) for
#             w in target.all_words()}

for s, h in enumerate(hyps):
    h.compute_likelihood(huge_data)
    h.point_ll = h.likelihood / len(huge_data)
    for wrd in assess_inv_hyp(h, target, four_gen_tree_context):
        result = [s] + wrd
        result_strings.append(', '.join(str(i) for i in result))
        results.append(result)

print "Writing csv file . . ."
with open(options.out_path, 'w') as f:
    f.write('\n'.join(result_strings))
