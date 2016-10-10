import pickle
from Model import *
from Model.Givens import turkish, english, pukapuka, four_gen_tree_context
from optparse import OptionParser
from LOTlib.TopN import TopN

#############################################################################################
#    Option Parser
#############################################################################################
parser = OptionParser()
parser.add_option("--read", dest="filename", type="string", help="Pickled results",
                  default="../LearnLexicon/English/Final/COMBO_ENG.pkl")
parser.add_option("--family", dest="family", type="string", help="Family", default='english')
parser.add_option("--data", dest="N", type="int", default=1000,
                  help="If > 0, recomputes the likelihood on a sample of data this size")
parser.add_option("--alpha", dest="alpha", type="int", default=0.90, help="Noise value")

(options, args) = parser.parse_args()

#############################################################################################
#    Functions and Things
#############################################################################################
def normalize(damount):
    huge_data = makeUniformData(target, four_gen_tree_context, n=damount, alpha=options.alpha)
    lexicon = { w : TopN(N=25, key='stored_likelihood') for w in target.all_words() }
    for h in hyps:
        for w in h.all_words():
            h.value[w].stored_likelihood = h.compute_word_likelihood(huge_data, w) / float(damount)
            lexicon[w].add(h.value[w])

    return lexicon

#############################################################################################
#    Evaluation Loop
#############################################################################################

with open(options.filename, 'r') as f:
    hyps = list(pickle.load(f))

target = eval(options.family)

lex = normalize(1000)

for w in target.all_words():
    for i, h in enumerate(lex[w]):
        print w, i, h.compute_prior(), h.stored_likelihood, h.display % str(h.value)