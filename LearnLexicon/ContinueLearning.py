import pickle
import numpy
import sys
from LOTlib.Hypotheses.LOTHypothesis import LOTHypothesis
from LOTlib.MPI.MPI_map import MPI_map, is_master_process
from LOTlib.Inference.MetropolisHastings import MHSampler
from LOTlib.Miscellaneous import display_option_summary, Infinity
from LOTlib.TopN import TopN
from LOTlib import break_ctrlc
from Model import *
from optparse import OptionParser

######################################################################################################
#   Option Parser
######################################################################################################
parser = OptionParser()
parser.add_option("--priors", dest='Prior', type="string", help='Any special priors?', default=None)
parser.add_option("--recurse", dest='recurse', action='store_true', help='Should we allow recursion?', default=True) # False
parser.add_option("--family", dest='family', type='string', help='What family tree to learn', default='english')
parser.add_option("--out", dest="out_path", type="string",
                  help="Output file (a pickle of FiniteBestSet)", default="EnglishRecurse.pkl")
parser.add_option("--read", dest="old", type="string",
                  help="Pickle of Finite Best Set Basis", default="BestEng.pkl")

parser.add_option("--steps", dest="steps", type="int", default=500000, help="Number of samples to run")
parser.add_option("--top", dest="top_count", type="int", default=100, help="Top number of hypotheses to store")
parser.add_option("--chains", dest="chains", type="int", default=3,
                  help="Number of chains to run (new data set for each chain)")

parser.add_option("--alpha", dest="alpha", type="float", default=0.90, help="Noise value")


parser.add_option("--data", dest="data", type="int", default=1000,       help="Amount of data") # -1
parser.add_option("--dmin", dest="data_min", type="int", default=10,   help="Min data to run")
parser.add_option("--dmax", dest="data_max", type="int", default=251, help="Max data to run")
parser.add_option("--dstep", dest="data_step", type="int", default=10, help="Step size for varying data")

parser.add_option("--llt", dest="llt", type="float", default=1.0, help="Likelihood temperature")
parser.add_option("--pt", dest="prior_temp", type="float", default=1.0, help="Likelihood temperature")

(options, args) = parser.parse_args()

if options.data == -1:
    options.data_pts = range(options.data_min, options.data_max, options.data_step)
else:
    options.data_pts = [options.data]

######################################################################################################
#   Specify Language Grammar
######################################################################################################
grammar_set = ['Tree', 'Set', 'Gender', 'Generation'] #, 'Ancestry', 'Paternity']
if options.family == 'hawaiian':
    from Model.Givens import hawaiian, four_gen_tree_context, hawaiian_words, four_gen_tree_objs

    target = hawaiian
    target_words = hawaiian_words
    if options.Prior is None:
        my_grammar = makeGrammar(four_gen_tree_objs, words=hawaiian_words,
                                 nterms=grammar_set, recursive=options.recurse)
    else:
        my_grammar = makeBiasedGrammar(four_gen_tree_objs, words=hawaiian_words,
                                       nterms=grammar_set, recursive=options.recurse)
elif options.family == 'pukapuka':
    from Model.Givens import pukapuka, four_gen_tree_context, pukapuka_words, four_gen_tree_objs

    target = pukapuka
    target_words = pukapuka_words
    if options.Prior is None:
        my_grammar = makeGrammar(four_gen_tree_objs, words=pukapuka_words,
                                 nterms=grammar_set, recursive=options.recurse)
    else:
        my_grammar = makeBiasedGrammar(four_gen_tree_objs, words=pukapuka_words,
                                       nterms=grammar_set, recursive=options.recurse)
elif options.family == 'sudanese':
    from Model.Givens import sudanese, four_gen_tree_context, sudanese_words, four_gen_tree_objs

    target = sudanese
    target_words = sudanese_words
    if options.Prior is None:
        my_grammar = makeGrammar(four_gen_tree_objs, words=sudanese_words,
                                 nterms=grammar_set, recursive=options.recurse)
    else:
        my_grammar = makeBiasedGrammar(four_gen_tree_objs, words=sudanese_words,
                                       nterms=grammar_set, recursive=options.recurse)
elif options.family == 'turkish':
    from Model.Givens import turkish, four_gen_tree_context, turkish_words, four_gen_tree_objs

    target = turkish
    target_words = turkish_words
    if options.Prior is None:
        my_grammar = makeGrammar(four_gen_tree_objs, words=turkish_words,
                                 nterms=grammar_set, recursive=options.recurse)
    else:
        my_grammar = makeBiasedGrammar(four_gen_tree_objs, words=turkish_words,
                                       nterms=grammar_set, recursive=options.recurse)
elif options.family == 'eskimo':
    from Model.Givens import eskimo, four_gen_tree_context, eskimo_words, four_gen_tree_objs

    target = eskimo
    target_words = eskimo_words
    if options.Prior is None:
        my_grammar = makeGrammar(four_gen_tree_objs, words=eskimo_words,
                                 nterms=grammar_set, recursive=options.recurse)
    else:
        my_grammar = makeBiasedGrammar(four_gen_tree_objs, words=eskimo_words,
                                       nterms=grammar_set, recursive=options.recurse)
elif options.family == 'iroquois':
    from Model.Givens import iroquois, four_gen_tree_context, iroquois_words, four_gen_tree_objs

    target = iroquois
    target_words = iroquois_words
    if options.Prior is None:
        my_grammar = makeGrammar(four_gen_tree_objs, words=iroquois_words,
                                 nterms=grammar_set, recursive=options.recurse)
    else:
        my_grammar = makeBiasedGrammar(four_gen_tree_objs, words=iroquois_words,
                                       nterms=grammar_set, recursive=options.recurse)
elif options.family == 'omaha':
    from Model.Givens import omaha, four_gen_tree_context, omaha_words, four_gen_tree_objs

    target = omaha
    target_words = omaha_words
    if options.Prior is None:
        my_grammar = makeGrammar(four_gen_tree_objs, words=omaha_words,
                                 nterms=grammar_set, recursive=options.recurse)
    else:
        my_grammar = makeBiasedGrammar(four_gen_tree_objs, words=omaha_words,
                                       nterms=grammar_set, recursive=options.recurse)

elif options.family == 'crow':
    from Model.Givens import crow, four_gen_tree_context, crow_words, four_gen_tree_objs

    target = crow
    target_words = crow_words
    if options.Prior is None:
        my_grammar = makeGrammar(four_gen_tree_objs, words=crow_words,
                                 nterms=grammar_set, recursive=options.recurse)
    else:
        my_grammar = makeBiasedGrammar(four_gen_tree_objs, words=crow_words,
                                       nterms=grammar_set, recursive=options.recurse)

elif options.family == 'english':

    from Model.Givens import english, four_gen_tree_context, english_words, four_gen_tree_objs

    target = english

    target_words = english_words

    if options.Prior is None:

        my_grammar = makeGrammar(four_gen_tree_objs, words=english_words,

                                 nterms=grammar_set, recursive=options.recurse)

    else:

        my_grammar = makeBiasedGrammar(four_gen_tree_objs, words=english_words,

                                       nterms=grammar_set, recursive=options.recurse)

else:
    from Model.Givens import target, four_gen_tree_context, genderless_english_words, four_gen_tree_objs

    target_words = genderless_english_words
    if options.Prior is None:
        my_grammar = makeGrammar(four_gen_tree_objs, words=genderless_english_words,
                                 nterms=grammar_set, recursive=options.recurse)
    else:
        my_grammar = makeBiasedGrammar(four_gen_tree_objs, words=genderless_english_words,
                                       nterms=grammar_set, recursive=options.recurse)

######################################################################################################
#   Chain Function
######################################################################################################
def run(hypothesis, data_amount):
    print "Starting chain on %s data points"%data_amount
    data = makeLexiconData(target, four_gen_tree_context, n=data_amount, alpha=options.alpha, verbose=True)

    h0 = KinshipLexicon(alpha=options.alpha)
    for w in target_words:
        h0.set_word(w, LOTHypothesis(grammar=my_grammar, value=hypothesis.value[w].value, display='lambda recurse_, C, X: %s'))

    hyps = TopN(N=options.top_count)

    mhs = MHSampler(h0, data, options.steps, likelihood_temperature=options.llt, prior_temperature=options.prior_temp)

    for samples_yielded, h in break_ctrlc(enumerate(mhs)):
        if samples_yielded % 100 == 0:
            pass #print h.likelihood, h.prior, h
        hyps.add(h)

    import pickle
    print 'Writing ' + data[0].X + data[0].Y + str(data_amount) + data[0].word + '.pkl'
    with open('Chains/' + data[0].X + data[0].Y + str(data_amount) + data[0].word + '.pkl', 'w') as f:
        pickle.dump(hyps, f)

    return hyps

###################################################################################
# Main Running
###################################################################################

print '## Loading hypothesis space'
with open(options.old, 'r') as f:
    base_hyps = list(pickle.load(f))

runs = [[h, dp] for h in base_hyps for dp in options.data_pts]

argarray = map( lambda x : x, runs * options.chains)

print len(argarray)

if is_master_process():
    display_option_summary(options)

seen = set()
for fs in break_ctrlc(MPI_map(run, numpy.random.permutation(argarray), progress_bar=False)) :
    for h in fs.get_all():
        if h not in seen:
            seen.add(h)
            if h.prior > -Infinity:
                print h.prior, \
                    h.likelihood, \
                    h \

        sys.stdout.flush()

sys.stdout.flush()

with open(options.out_path, 'w') as f:
    pickle.dump(seen, f)
