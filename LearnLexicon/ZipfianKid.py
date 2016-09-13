import pickle
import numpy as np
from fractions import Fraction
from Model.Givens import english, four_gen_tree_context, four_gen_tree_objs
from LOTlib.Inference.GrammarInference.Precompute import create_counts
from Model import *
from optparse import OptionParser

parser = OptionParser()
parser.add_option("--read", dest="filename", type="string", help="Pickled results",
                  default="PukaPuka/Mixing/Mixed2Puka.pkl")
(options, args) = parser.parse_args()

print "Loading hypotheses . . ."
with open(options.filename, 'r') as f:
    hyps = pickle.load(f)

#######################################################################
bootstrap = 1

four_gen_tree_context.distance = {'Amanda': 6, 'Anne': 33, 'aragorn': 9, 'Arwen': 14, 'Brandy': 13, 'Celebrindal': 37,
                                  'Clarice': 18, 'elrond': 36, 'Eowyn': 21, 'fabio': 29, 'fred': 32, 'frodo': 4,
                                  'Galadriel': 35,
                                  'gandalf': 34, 'han': 22, 'harry': 15, 'Hermione': 8, 'gary': 17, 'james': 30,
                                  'joey': 28,
                                  'Katniss': 2, 'legolas': 26, 'Leia': 25, 'Lily': 31, 'luke': 23, 'Luna': 27,
                                  'Mellissa': 19, 'merry': 10,
                                  'Padme': 24, 'peeta': 1, 'Prue': 5, 'ron': 20, 'Rose': 11, 'Sabrina': 3, 'salem': 16,
                                  'sam': 12, 'Zelda': 7}

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
    prior = 0.0
    for k in counts.keys():
        c = np.sum(counts[k], axis=0)
        prior += multdir([c], np.ones(len(c))/float(len(c)))[0]

    return prior


def compute_Zipf_likelihood(hyp, data, context, s):
    ll = 0
    trueset = hyp.make_true_data(context)
    all_poss = len(hyp.all_words()) * len(context.objects) ** 2
    all_poss_speakers = set([t[1] for t in trueset])
    margin = float(sum(Fraction(1, d) ** s for d in xrange(1, len(all_poss_speakers) + 1)))

    for datum in data:
        if (datum.word, datum.X, datum.Y) in trueset:
            pS = (context.distance[datum.X] ** -s) / margin

            bagR = {w : hyp(w, context, set([datum.X])) for w in hyp.all_words()}
            uniqR = []
            for w in hyp.all_words():
                uniqR.extend(bagR[w])
            marginR = float(sum(Fraction(1, d) ** s for d in xrange(1, len(uniqR) + 1)))

            pRgS = (context.distance[datum.Y] ** -s) / marginR

            pWgRS = 1./sum([1. for w in hyp.all_words() if datum.Y in bagR[w]])

            ll += np.log(hyp.alpha * pS * pRgS * pWgRS + ((1. - hyp.alpha) / all_poss))
        else:
            ll += np.log((1. - hyp.alpha) / all_poss)

    return ll / hyp.likelihood_temperature


def assess_inv_hyp(hypothesis, target_lexicon, context):
    output = []
    ground_truth = target_lexicon.make_true_data(context)
    hypothesized_lexicon_data = hypothesis.make_true_data(context)
    for w in target_lexicon.all_words():
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
        out = [w]
        out.append(int(len(true_word_data) == len(hypothesized_word_data) and len(true_word_data) == correct_count))
        out.append(float(correct_count)/len(hypothesized_word_data))
        out.append(float(correct_count)/len(true_word_data))
        out.append(do_I_abstract(hypothesis.value[w]))
        output.append(out)
    return output

def do_I_abstract(h):
    return int( 'X' in [x.name for x in h.value.subnodes()])

#######################################################################

for itr in xrange(bootstrap):
    print "Begining bootstrap number " + str(itr)
    for s in [0, 1, 2, 3]:
        print "Starting Zipfian Distribution, s = " + str(s)
        for dp in [1] + range(2, 199, 2) + range(200, 600, 50):
            print "Running data amount " + str(dp)
            data = makeZipfianLexiconData(english,'',four_gen_tree_context, n=dp, s=s)
            Priors = np.zeros((len(hyps), 3))
            Params = np.array(['HypNo','Word','Acc','Precision','Recall','Abstraction','LexAccuracy'])[np.newaxis]
            for i, h in enumerate(hyps):
                stats = assess_inv_hyp(h, english, four_gen_tree_context)
                if sum([stat[1] for stat in stats]) == len(english.all_words()):
                    stats = [[i] + pars + [1] for pars in stats]
                else:
                    stats = [[i] + pars + [0] for pars in stats]
                Params = np.vstack((Params, stats))
                like = compute_Zipf_likelihood(h, data, four_gen_tree_context, s=s)
                Priors[i, 0] = i
                Priors[i, 1] = h.compute_prior() + like
                Priors[i, 2] = compute_reuse_prior(h) + like
            np.savetxt('ZipfRun/ZipfRun_S_' + str(s) + '_N_' + str(dp) + '_Boot_' + str(itr) + '_Params.csv', Params,
                       '%s', delimiter=',')
            np.savetxt('ZipfRun/ZipfRun_S_' + str(s) + '_N_' + str(dp) + '_Boot_' + str(itr) + '_Post.csv', Priors, delimiter=',')

