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
parser.add_option("--grammar", dest='grammar', type="string", help='Char or def?', default='def')
parser.add_option("--recurse", dest='recurse', action='store_true', help='Should we allow recursion?', default=False)
parser.add_option("--family", dest='family', type='string', help='What system to learn', default='english')
parser.add_option("--context", dest='context', type='string', help='What family tree to learn', default='Info1')
parser.add_option("--out", dest="out_path", type="string",
                  help="Output file (a pickle of FiniteBestSet)", default="shift.pkl")

parser.add_option("--steps", dest="steps", type="int", default=500000, help="Number of samples to run")
parser.add_option("--top", dest="top_count", type="int", default=100, help="Top number of hypotheses to store")
parser.add_option("--chains", dest="chains", type="int", default=7,
                  help="Number of chains to run (new data set for each chain)")

parser.add_option("--alpha", dest="alpha", type="float", default=0.90, help="Noise value")
parser.add_option("--epsilon", dest="epsilon", type="float", default=0.0, help="Ego-centricity")
parser.add_option("--s", dest="s", type="float", default=0., help="zipf parameter")

parser.add_option("--data", dest="data", type="int", default=-1,       help="Amount of data")
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

if options.context == 'Info1':
    from Model.FeatureGiven import Info1_tree_context, Info1_obj
    the_context = Info1_tree_context
    the_objects = Info1_obj
elif options.context == 'Info2':
    from Model.FeatureGiven import Info2_tree_context, Info2_obj
    the_context = Info2_tree_context
    the_objects = Info2_obj
elif options.context == 'Info3':
    from Model.FeatureGiven import Info3_tree_context, Info3_obj
    the_context = Info3_tree_context
    the_objects = Info3_obj
elif options.context == 'Info4':
    from Model.FeatureGiven import Info4_tree_context, Info4_obj
    the_context = Info4_tree_context
    the_objects = Info4_obj
else:
    assert False, "Context does not exist!!!"

if options.family == 'pukapuka':
    from Model.Givens import pukapuka, pukapuka_words
    target = pukapuka
    target_words = pukapuka_words
elif options.family == 'turkish':
    from Model.Givens import turkish, turkish_words
    target = turkish
    target_words = turkish_words
elif options.family == 'english':
    from Model.Givens import english, english_words
    target = english
    target_words = english_words
else:
    assert False, "Which language am I surrounded by?"

if options.grammar == "def":
    my_grammar = makeGrammar(the_objects, words=target_words,
                             nterms=grammar_set, recursive=options.recurse)
elif options.grammar == 'char':
    my_grammar = makeCharGrammar(the_context)
else:
    assert False, "What grammar am I using?"

######################################################################################################
#   Chain Function
######################################################################################################
def run(data_amount):
    print "Starting chain on %s data points"%data_amount
    data = makeTreeLexiconData(target, the_context, n=data_amount, alpha=options.alpha, epsilon=options.epsilon, verbose=True)

    h0 = KinshipLexicon(alpha=options.alpha)
    for w in target_words:
        h0.set_word(w, LOTHypothesis(my_grammar, display='lambda recurse_, C, X: %s'))

    hyps = TopN(N=options.top_count)

    mhs = MHSampler(h0, data, options.steps, likelihood_temperature=options.llt, prior_temperature=options.prior_temp)

    for samples_yielded, h in break_ctrlc(enumerate(mhs)):
        if samples_yielded % 100 == 0:
            print h.prior, h.likelihood, h
        hyps.add(h)

    import pickle
    print 'Writing ' + data[0].X + data[0].Y + str(data_amount) + data[0].word + '.pkl'
    with open('Chains/' + data[0].X + data[0].Y + str(data_amount) + data[0].word + '.pkl', 'w') as f:
        pickle.dump(hyps, f)

    return hyps

###################################################################################
# Main Running
###################################################################################

argarray = map(lambda x: [x], options.data_pts * options.chains)

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

        #sys.stdout.flush()

#sys.stdout.flush()

import pickle
with open(options.out_path, 'w') as f:
    pickle.dump(seen, f)
