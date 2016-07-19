import pickle
import numpy as np
from copy import copy
from Model import *
from Model.Givens import *
from LOTlib.MPI.MPI_map import MPI_map, is_master_process
from LOTlib import break_ctrlc
from LOTlib.TopN import TopN
from LOTlib.Miscellaneous import display_option_summary
from LOTlib.Miscellaneous import weighted_sample
from optparse import OptionParser

######################################################################################################
#   Option Parser
######################################################################################################
parser = OptionParser()
parser.add_option("--family", dest='family', type='string', help="What is the target",
                  default='english')
parser.add_option("--space", dest="space", type='string', help="Pickled hypotheses",
                  default='truncated.pkl')
parser.add_option("--out", dest="out_loc", type='string', help="Output file location",
                  default='GibbsEnglish.pkl')

parser.add_option("--alpha", dest="alpha", type='float', help='Reliability of a data point', default=0.9)
parser.add_option("--samples", dest="samples", type="int", help="Number of samples desired", default=100000)
parser.add_option("--top", dest="top_count", type="int", default=100, help="Top number of hypotheses to store")
parser.add_option("--chains", dest="chains", type="int", default=1,
                  help="Number of chains to run (new data set for each chain)")

parser.add_option("--data", dest="data", type="int", default=-1,       help="Amount of data")
parser.add_option("--dmin", dest="data_min", type="int", default=10,   help="Min data to run")
parser.add_option("--dmax", dest="data_max", type="int", default=251, help="Max data to run")
parser.add_option("--dstep", dest="data_step", type="int", default=10, help="Step size for varying data")

(options, args) = parser.parse_args()

if options.data == -1:
    options.data_pts = range(options.data_min, options.data_max, options.data_step)
else:
    options.data_pts = [options.data]

######################################################################################################
#   Sampler Class
######################################################################################################
from LOTlib.Inference.Samplers.Sampler import Sampler
class Gibbs(Sampler):
    def __init__(self, current_sample, data, steps=np.Infinity, proposer=None, skip=0,
                 prior_temperature=1.0, likelihood_temperature=1.0, acceptance_temperature=1.0, trace=False,
                 shortcut_likelihood=True):

        self.__dict__.update(locals())
        self.__dict__.pop('self')
        self.was_accepted = None

        if proposer is None:
            self.proposer = lambda x: x.propose()

        self.samples_yielded = 0
        self.set_state(current_sample, compute_posterior=(current_sample is not None))
        self.reset_counters()

    def reset_counters(self):
        """
        Reset acceptance and proposal counters.
        """
        self.acceptance_count = 0
        self.proposal_count   = 0
        self.posterior_calls  = 0

    def next(self):
        """Generate another sample."""
        if self.samples_yielded >= self.steps:
            raise StopIteration
        else:
            for _ in xrange(self.skip + 1):

                self.proposal = self.proposer(self.current_sample)

                assert self.proposal is not self.current_sample, "*** Proposal cannot be the same as the current sample!"
                assert self.proposal.value is not self.current_sample.value, "*** Proposal cannot be the same as the current sample!"

                # Call myself so memoized subclasses can override
                self.compute_posterior(self.proposal, self.data)

                self.current_sample = self.proposal

            self.samples_yielded += 1
            return self.current_sample

######################################################################################################
#   Load Lexicons
######################################################################################################
target = eval(options.family)

# Load in the lexicons
hypothesis_space = []
with open(options.space, 'r') as f:
    hypothesis_space.extend(pickle.load(f))

print '## Loaded', len(hypothesis_space), 'hypotheses.'

from LOTlib.Hypotheses.LOTHypothesis import LOTHypothesis
grammar_set = ['Tree', 'Set', 'Gender', 'Generation'] #, 'Ancestry', 'Paternity']
my_grammar = makeGrammar(four_gen_tree_objs, words=turkish_words,
                         nterms=grammar_set)

def makeLexicon():
    lexicon = { w : set() for w in target.all_words() }
    for h in hypothesis_space:
        for w in h.all_words():
            lexicon[w].add(h.value[w])

    for w in lexicon.keys():
        length = len(lexicon[w])
        lexicon[w] = list(lexicon[w])
        if len(lexicon[w])==length: print length, 'hypotheses for', w

    return lexicon

def normalize(damount):
    huge_data = makeUniformData(target, four_gen_tree_context, n=damount, alpha=options.alpha)
    # Renormalize posterior over hypotheses
    L = dict()
    for i, w in enumerate(target.all_words()):
        L[w] = [h.compute_prior() + h.compute_word_likelihood(huge_data) for h in lexicon[w]]
    return L, huge_data

def run(damount):
    L, hugeData = normalize(damount)
    words = target.all_words()
    def propose(current_state, bag=lexicon, probs=L):
        mod = len(current_state.all_words())
        proposal = copy(current_state)
        proposal.value[words[propose.inx % mod]].value = weighted_sample(bag[words[propose.inx % mod]],
                                                                probs=probs[words[propose.inx % mod]], log=True).value
        propose.inx += 1
        return proposal
    propose.inx = 0
    proposer = lambda x : propose(x)

    h0 = KinshipLexicon(alpha=options.alpha)
    for w in target.all_words():
        h0.set_word(w, LOTHypothesis(my_grammar, display='lambda recurse_, C, X: %s'))

    gs = Gibbs(h0, hugeData, proposer=proposer, steps=options.samples)
    hyps = TopN(N=options.top_count)
    for s, h in enumerate(gs):
        hyps.add(h)

    return hyps

######################################################################################################
#   Run Time Code
######################################################################################################

lexicon = makeLexicon()

argarray = map(lambda x: [x], options.data_pts * options.chains)

if is_master_process():
    display_option_summary(options)

seen = set()
for fs in break_ctrlc(MPI_map(run, argarray, progress_bar=False)) :
    for h in fs.get_all():
        seen.add(h)

with open(options.out_loc, 'w') as f:
    pickle.dump(seen, f)
