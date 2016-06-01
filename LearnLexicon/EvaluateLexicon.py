import pickle
from Model import *
from optparse import OptionParser
from Model.Givens import turkishA, four_gen_tree_context

target = turkishA

#############################################################################################
#    Option Parser
#############################################################################################
parser = OptionParser()
parser.add_option("--read", dest="input_loc", type="string", help="Pickled results",
                  default="pukapuka300.pkl")
parser.add_option("--pickle", dest="pkl_loc", type="string", help="Output a pkl", default=None)
parser.add_option("--write", dest="out_path", type="string", help="Results csv",
                  default="results.csv")

parser.add_option("--data", dest="data_size", type="int", default=1000,
                  help="If > 0, recomputes the likelihood on a sample of data this size")
parser.add_option("--alpha", dest="alpha", type="int", default=0.90, help="Noise value")

(options, args) = parser.parse_args()

#############################################################################################
#    SUPER COOL FUNCTION
#############################################################################################


def assess_hyp(hypothesis, target_lexicon, context):
    findings = []
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
        findings.append([hypothesis.prior, hypothesis.point_ll, w, correct_count,
                         len(hypothesized_word_data), len(true_word_data)])
    return findings

#############################################################################################
#    MAIN CODE
#############################################################################################

print "Making data set of size %s . . ."%options.data_size
huge_data = makeLexiconData(target, four_gen_tree_context, n=options.data_size, alpha=options.alpha, verbose=True)

print "Loading hypothesis space . . ."
hypothesis_space = set()
with open(options.input_loc, 'r') as f:
    hypothesis_space.update(pickle.load(f))


print "Assessing hypotheses . . ."
results = []
result_strings = []
for s, h in enumerate(hypothesis_space):
    # Normalize and calculate point_ll
    h.compute_likelihood(huge_data)
    h.point_ll = h.likelihood / float(options.data_size)
    for wrd in assess_hyp(h, target, four_gen_tree_context):
        result = [s] + wrd
        result_strings.append(', '.join(str(i) for i in result))
        results.append(result)


print "Writing csv file . . ."
with open(options.out_path, 'w') as f:
    f.write('\n'.join(result_strings))


if options.pkl_loc is not None:
    with open(options.pkl_loc, 'w') as f:
        pickle.dump(results, f)
