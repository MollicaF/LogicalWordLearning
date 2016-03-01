import pickle
from LOTlib import break_ctrlc
from LOTlib.Miscellaneous import display_option_summary
from LOTlib.MPI.MPI_map import MPI_map, is_master_process
from LOTlib.Inference.MetropolisHastings import MHSampler
from LOTlib.MCMCSummary.TopN import TopN
from LOTlib.Hypotheses.LOTHypothesis import LOTHypothesis
from Model import *
from itertools import combinations
from optparse import OptionParser
from random import random

######################################################################################################
#   Option Parser
######################################################################################################
parser = OptionParser()
parser.add_option("--pre", dest="OUT_PATH", type="string", help="Output file (a pickle of FiniteBestSet)",
                  default="Results/")

parser.add_option("--steps", dest="STEPS", type="int", default=100000, help="Number of samples to run")
parser.add_option("--top", dest="TOP_COUNT", type="int", default=1000, help="Top number of hypotheses to store")
parser.add_option("--chains", dest="CHAINS", type="int", default=1,
                  help="Number of chains to run (new data set for each chain)")

parser.add_option("--alpha", dest="ALPHA", type="float", default=0.90, help="Noise value")
parser.add_option("--k", dest="k", type="int", default=2, help="All k-combinations")
parser.add_option("--random", dest='randomize', type="string", default=False, help="Randomize gramamar priors")

parser.add_option("--llt", dest="llt", type="float", default=1.0, help="Likelihood temperature")

(options, args) = parser.parse_args()

######################################################################################################
#   Specify Grammar
######################################################################################################
from Model.Givens import simple_tree_context, simple_tree_objs

my_grammar = makeGrammar(simple_tree_objs, nterms=['Tree', 'Set', 'Gender', 'Generation', 'Ancestry', 'Paternity'])

if options.randomize:
    for r in my_grammar:
        r.p = random()

######################################################################################################
#   Chain Function
######################################################################################################
def run(data_pts):
    print "Start run on ", str(data_pts)

    y = [pt.Y for pt in data_pts]
    filename = "".join(y)

    hyps = TopN(N=options.TOP_COUNT)
    h0 = KinshipLexicon(alpha=options.ALPHA)
    h0.set_word('Word', LOTHypothesis(my_grammar, value=None, display='lambda recurse_, C, X:%s'))
    mhs = MHSampler(h0, data_pts, options.STEPS, likelihood_temperature=options.llt)

    for samples_yielded, h in break_ctrlc(enumerate(mhs)):
        hyps.add(h)

    with open(options.OUT_PATH + filename + '.pkl', 'w') as f:
        pickle.dump(hyps, f)

    return filename, hyps

###################################################################################
# Main Running
###################################################################################

data = [list(pt) for pt in combinations([KinshipData('Word','ego','Snow', simple_tree_context),
        KinshipData('Word', 'ego', 'charming', simple_tree_context),
        KinshipData('Word', 'ego', 'Emma', simple_tree_context),
        KinshipData('Word', 'ego', 'Mira', simple_tree_context),
        KinshipData('Word', 'ego', 'rump', simple_tree_context),
        KinshipData('Word', 'ego', 'Regina', simple_tree_context),
        KinshipData('Word', 'ego', 'henry', simple_tree_context),
        KinshipData('Word', 'ego', 'neal', simple_tree_context),
        KinshipData('Word', 'ego', 'baelfire', simple_tree_context),
        KinshipData('Word', 'ego', 'Maryann', simple_tree_context)], options.k)]

argarray = map(lambda x: [x], data * options.CHAINS)

if is_master_process():
    display_option_summary(options)

hypothesis_space = set()
for s, h in MPI_map(run, argarray, progress_bar=True):
    hypothesis_space.update(h)
    print "Done with " + s

with open(options.OUT_PATH + str(options.k) + "dp_HypothesisSpace.pkl", 'w') as f:
    pickle.dump(hypothesis_space, f)
