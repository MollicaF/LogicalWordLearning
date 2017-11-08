import numpy
import sys
from LOTlib.Hypotheses.LOTHypothesis import LOTHypothesis
from LOTlib.MPI.MPI_map import MPI_map, is_master_process
from LOTlib.Inference.MetropolisHastings import MHSampler
from LOTlib.Miscellaneous import display_option_summary, Infinity
from LOTlib.MCMCSummary.TopN import TopN
from LOTlib import break_ctrlc
from optparse import OptionParser

######################################################################################################
#   Option Parser
######################################################################################################
parser = OptionParser()
parser.add_option("--out", dest="out_path", type="string",
                  help="Output file (a pickle of FiniteBestSet)", default="uninformativePrior.pkl")

parser.add_option("--steps", dest="steps", type="int", default=1000000, help="Number of samples to run")
parser.add_option("--top", dest="top_count", type="int", default=1000, help="Top number of hypotheses to store")
parser.add_option("--chains", dest="chains", type="int", default=8,
                  help="Number of chains to run (new data set for each chain)")

parser.add_option("--alpha", dest="alpha", type="float", default=0.90, help="Reliability value [0-1)")
parser.add_option("--s", dest="s", type="float", default=1.00, help="Zipfian Exponent")
parser.add_option("--type", dest="hypType", type='string', default='char', help='Char or Def?')
parser.add_option("--word", dest="word", type='string', default='uncle', help='Which word are we learning?')

parser.add_option("--data", dest="data", type="int", default=-1, help="Amount of data")
parser.add_option("--dmin", dest="data_min", type="int", default=10, help="Min data to run")
parser.add_option("--dmax", dest="data_max", type="int", default=251, help="Max data to run")
parser.add_option("--dstep", dest="data_step", type="int", default=10, help="Step size for varying data")

parser.add_option("--llt", dest="llt", type="float", default=1.0, help="Likelihood temperature")
parser.add_option("--pt", dest="prior_temp", type="float", default=1.0, help="Likelihood temperature")

(options, args) = parser.parse_args()

if options.data == -1:
    options.data_pts = range(options.data_min, options.data_max, options.data_step)
else:
    options.data_pts = [options.data]

from Model.Data import makeZipfianLexiconData
from Model.FeatureGiven import *
from Model.Givens import uncle, brother, mother, grandma

if options.hypType == 'def':
    grammar = def_grammar
elif options.hypType == 'char':
    grammar = char_grammar
else:
    raise ValueError('Hypothesis Type not properly defined!')

######################################################################################################
#   Chain Function
######################################################################################################
def run(data_amount):
    print "Starting chain on %s data points" % data_amount
    data = makeVariableLexiconData(eval(options.word), options.word, the_context, n=data_amount, s=options.s,
                                   alpha=options.alpha, verbose=True)

    h0 = KinshipLexicon(words=[options.word], alpha=options.alpha)
    h0.set_word(options.word, LOTHypothesis(grammar, value=None, display='lambda recurse_, C, X:%s'))

    hyps = TopN(N=options.top_count)

    mhs = MHSampler(h0, data, options.steps, likelihood_temperature=options.llt,
                    prior_temperature=options.prior_temp)

    for samples_yielded, h in break_ctrlc(enumerate(mhs)):
        if samples_yielded % 1000 == 0:
            print h.prior, h.likelihood, h
        hyps.add(h)

    return hyps

###################################################################################
# Main Running
###################################################################################

argarray = map(lambda x: [x], options.data_pts * options.chains)

if is_master_process():
    display_option_summary(options)

seen = set()
for fs in MPI_map(run, numpy.random.permutation(argarray), progress_bar=False):
    for h in fs.get_all():
        if h not in seen:
            seen.add(h)
            if h.prior > -Infinity:
                print h.prior, \
                    h.likelihood, \
                    h
                sys.stdout.flush()

sys.stdout.flush()

import pickle

with open(options.out_path, 'w') as f:
    pickle.dump(seen, f)
