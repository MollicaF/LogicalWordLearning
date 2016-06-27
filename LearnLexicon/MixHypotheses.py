import pickle
import numpy as np
from copy import copy
from Model import *
from Model.Givens import *
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
parser.add_option("--size", dest="size", type='int', help='Normaliation data size', default=1000)
parser.add_option("--alpha", dest="alpha", type='float', help='Reliability of a data point', default=0.9)
parser.add_option("--samples", dest="samples", type="int", help="Number of samples desired", default=100000)


(options, args) = parser.parse_args()
######################################################################################################
#   Load Lexicons
######################################################################################################
target = eval(options.family)

# Load in the lexicons
hypothesis_space = []
with open(options.space, 'r') as f:
    hypothesis_space.extend(pickle.load(f))

print '## Loaded', len(hypothesis_space), 'hypotheses.'

huge_data = makeLexiconData(target, four_gen_tree_context, n=options.size, alpha=options.alpha, verbose=False)
# Split lexicon's into hypotheses
lexicon = { w : set() for w in target.all_words() }
for h in hypothesis_space:
    for w in h.all_words():
        data = [dp for dp in huge_data if dp.word == w]
        h.value[w].stored_likelihood = h.compute_likelihood(data)
        lexicon[w].add(h.value[w])

for w in lexicon.keys():
    length = len(lexicon[w])
    lexicon[w] = list(lexicon[w])
    if len(lexicon[w])==length: print length, 'hypotheses for', w

# Renormalize posterior over hypotheses
L = dict()
#P = np.zeros((len(target.all_words()), len(hypothesis_space)))
for i, w in enumerate(target.all_words()):
    L[w] = [h.compute_prior() + h.stored_likelihood for h in lexicon[w]]
    #P[i, :] = L[w]

#np.savetxt('Post.csv', P, delimiter=',')
# How many hyps per mass?
def countMass(hyps):
    [h.compute_posterior(huge_data) for h in hyps]
    u = max([h.posterior_score for h in hyps])
    Z = u + np.log(sum(np.exp([h.posterior_score - u for h in hyps])))
    a = np.exp([h.posterior_score - Z for h in hyps])
    mass = 0
    numHyps = 0
    probs = sorted(a)
    probs.reverse()
    for h in probs:
        if mass < 0.95:
            mass += h
            numHyps += 1
        else:
            return numHyps

#print "Initial No. Hyps w/in 95% mass:", countMass(hypothesis_space)

######################################################################################################
#   Sampler Class
######################################################################################################

inx = 0
words = target.all_words()
# def propose(current_state, bag=lexicon, probs=L):
#     proposal = copy(current_state)
#     for w in current_state.value.keys():
#         proposal.value[w].value = weighted_sample(bag[w], probs=probs[w], log=True).value
#     return proposal
def propose(current_state, bag=lexicon, probs=L):
    global inx
    proposal = copy(current_state)
    if inx > len(words)-1:
        inx = 0
    proposal.value[words[inx]].value = weighted_sample(bag[words[inx]], probs=probs[words[inx]], log=True).value
    inx += 1
    return proposal

proposer = lambda x : propose(x)

from LOTlib.Inference.Samplers.Sampler import Sampler
class Gibbs(Sampler):
    def __init__(self, current_sample, data, steps=np.Infinity, proposer=proposer, skip=0,
                 prior_temperature=1.0, likelihood_temperature=1.0, acceptance_temperature=1.0, trace=False,
                 shortcut_likelihood=True):

        self.__dict__.update(locals())
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
#   Run Time Code
######################################################################################################

gs = Gibbs(hypothesis_space[0], huge_data, steps=options.samples)

gibbed = set()
for s, h in enumerate(gs):
    if h not in gibbed:
        print h.prior, h.likelihood, h
        gibbed.add(h)

with open(options.out_loc, 'w') as f:
    pickle.dump(gibbed, f)

#print "Final No. Hyps w/in 95% mass:", countMass(gibbed)
print len(hypothesis_space), 'altered to', len(gibbed)