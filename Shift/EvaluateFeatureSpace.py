import os
import pickle
from LOTlib.Miscellaneous import log
from Data import makeVariableLexiconData
from optparse import OptionParser
from fractions import Fraction
from Model.Givens import mother, brother, uncle, grandma
from FeatureGiven import *

#############################################################################################
#    Option Parser
#############################################################################################
parser = OptionParser()
parser.add_option("--read", dest="input_loc", type="string", help="Pickled results",
                  default="Data/Baseline.pkl")
parser.add_option("--pickle", dest="pkl_loc", type="string", help="Output a pkl", default=None)
parser.add_option("--write", dest="out_path", type="string", help="Results csv",
                  default="Results_PUK.csv")

parser.add_option("--data", dest="data_size", type="int", default=1000,
                  help="If > 0, recomputes the likelihood on a sample of data this size")
parser.add_option("--word", dest="word", type="string", help="Word you are learning", default="uncle")
parser.add_option("--alpha", dest="alpha", type="int", default=0.90, help="Reliability value (0-1]")

(options, args) = parser.parse_args()

#############################################################################################
#    SUPER COOL FUNCTION (Takes 30 min to run)
#############################################################################################

def compute_likelihood(self, s, data, word):
    ll = 0
    context = data[0].context  # Hack same context for all likelihood
    trueset = self.make_true_data(context)
    all_poss = len(self.all_words()) * len(context.objects) ** 2
    all_poss_speakers = set([t[1] for t in trueset])
    margin = float(sum(Fraction(1, d) ** s for d in xrange(1, len(all_poss_speakers) + 1)))

    for datum in data:
        if (datum.word, datum.X, datum.Y) in trueset:
            pS = (context.distance[datum.Y] ** -s) / margin
            pRgS = (context.distance[datum.Y] ** -s) / sum(
                [(context.distance[ref] ** -s) for ref in self(word, context, set([datum.X]))])
            ll += log(self.alpha * pS * pRgS + ((1. - self.alpha) / all_poss))
        else:
            ll += log((1. - self.alpha) / all_poss)

    self.likelihood = ll / self.likelihood_temperature

    self.update_posterior()
    return self.likelihood

# Note assess_hypothesis really assess a lexicon
def assess_hyp(hypothesis, target_lexicon, context):
    findings = []
    ground_truth = set(target_lexicon.make_true_data(context))
    hypothesized_lexicon_data = set(hypothesis.make_true_data(context))
    # For each word
    for w in target_lexicon.all_words():
        # Find hypothesized data about that word
        hypothesized_word_data = set()
        for dp in hypothesized_lexicon_data:
            if dp[0] == w:
                hypothesized_word_data.add(dp)
        # Find true data about that word
        true_word_data = set()
        for dp in ground_truth:
            if dp[0] == w:
                true_word_data.add(dp)
        # Count up the correct data points
        correct_count = 0
        for dp in hypothesized_word_data:
            if dp in true_word_data:
                correct_count += 1
        # Figure out if it was characteristic or defining
        hyptype = hypothesis.value[w].value.args[0].returntype
        # Add it to the results: So Ideally we would have a line like this for every different context and all the contexts together
        findings.append([hyptype, hypothesis.prior, hypothesis.point_ll[0], hypothesis.point_ll[1],
                         hypothesis.point_ll[2], w, correct_count, len(hypothesized_word_data), len(true_word_data), hypothesis.value])
    return findings

#############################################################################################
#    MAIN CODE
#############################################################################################

print "Making data sets of size %s . . ." % options.data_size
huge_data_0 = makeVariableLexiconData(eval(options.word), options.word, the_context, n=options.data_size,
                                      s=0, alpha=options.alpha)
huge_data_1 = makeVariableLexiconData(eval(options.word), options.word, the_context, n=options.data_size,
                                      s=1, alpha=options.alpha)
huge_data_2 = makeVariableLexiconData(eval(options.word), options.word, the_context, n=options.data_size,
                                      s=2, alpha=options.alpha)

print "Loading hypothesis space . . ."
hypothesis_space = set()
for i in os.listdir(options.input_loc):
    with open(options.input_loc + i, 'r') as f:
        hypothesis_space.update(pickle.load(f))

print "Assessing hypotheses . . ."
results = []
result_strings = []
for s, h in enumerate(hypothesis_space):
    pll_s0 = compute_likelihood(h, 0.0, huge_data_0, options.word) / float(options.data_size)
    pll_s1 = compute_likelihood(h, 1.0, huge_data_1, options.word) / float(options.data_size)
    pll_s2 = compute_likelihood(h, 2.0, huge_data_2, options.word) / float(options.data_size)
    h.point_ll = [pll_s0, pll_s1, pll_s2]
    for wrd in assess_hyp(h, eval(options.word), the_context):
        result = [s] + wrd
        result_strings.append(', '.join(str(i) for i in result))
        results.append(result)

print "Writing csv file . . ."
with open(options.out_path, 'w') as f:
    f.write('\n'.join(result_strings))

if options.pkl_loc is not None:
    with open(options.pkl_loc, 'w') as f:
        pickle.dump(results, f)
