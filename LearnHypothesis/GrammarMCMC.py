from LOTlib.Miscellaneous import display_option_summary
from LOTlib.MPI.MPI_map import MPI_map, is_master_process
import pickle
import sys
import numpy as np
from LOTlib import break_ctrlc
from Model import *
from optparse import OptionParser
from Model.GrammarMH import GrammarMH
np.set_printoptions(threshold=np.inf)

######################################################################################################
#   Option Parser
######################################################################################################
parser = OptionParser()
parser.add_option("--human", dest='data_loc', type='string', help="Generalization Data location",
                  default='human.data')
parser.add_option("--space", dest='space_loc', type='string', help="Hypothesis Space location",
                  default='Snowcharming.pkl')
parser.add_option("--out", dest="out_path", type="string", help="Output file (a pickle of FiniteBestSet)",
                  default="DidItWork.pkl")

parser.add_option("--steps", dest="steps", type="int", default=100, help="Number of samples to run")
parser.add_option("--thin", dest="thin", type="int", default=10, help="Number of steps between saved samples")
parser.add_option("--chains", dest="chains", type="int", default=1, help="Number of chains to run")

(options, args) = parser.parse_args()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Define the grammar
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from Model.Givens import simple_tree_objs

grammar = makeGrammar(simple_tree_objs, nterms=['Tree', 'Set', 'Gender', 'Generation', 'Ancestry', 'Paternity'])

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Load the hypotheses
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# map each concept to a hypothesis
with open(options.space_loc, 'r') as f:
    hypotheses = list(pickle.load(f))

print "# Loaded hypotheses: ", len(hypotheses)

# for h in hypotheses:
# print h
#hypotheses = hypotheses[:10] # TODO: REMOVE THIS LINE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Load the human data
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from Model.Givens import simple_tree_context

L = []  # each hypothesis's cumulative likelihood to each data point
GroupLength = []
NYes = []
NTrials = []
Output = []

# cache the set for each hypothesis
for h in hypotheses:
    h.cached_set = h('Word', simple_tree_context, set(['ego']))

with open(options.data_loc, 'r') as f:
    # Each line is a "group"

    for i, line in enumerate(f.readlines()):

        entry = line.strip('\n').split(',')
        if i < 1:
            order = entry
        else:
            # get the conditioning data
            data = [KinshipData('Word', 'ego', entry[2], simple_tree_context),
                    KinshipData('Word', 'ego', entry[3], simple_tree_context)]
            # update the likelihood for each hypothesis on data
            L.append([h.compute_likelihood(data) for h in hypotheses])

            gl = 0
            for j in xrange(5, len(entry)):  # for each predictive response
                if entry[j] not in ('NA', 'NA\n'):
                    NYes.append(int(entry[j]))
                    NTrials.append(int(entry[4]))

                    Output.append([1 * (order[j] in h.cached_set) for h in hypotheses])

                    gl += 1

            GroupLength.append(gl)

print "# Loaded %s observed rows" % len(NYes)
print "# Organized %s groups" % len(GroupLength)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Get the rule count matrices
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from LOTlib.GrammarInference.GrammarInference import create_counts

# Decide which rules to use
which_rules = [r for r in grammar if r.nt in ['SET']]

counts, sig2idx, prior_offset = create_counts(grammar, hypotheses, which_rules=which_rules)

print "# Computed counts for each hypothesis & nonterminal"

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MCMC
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def run(a):
    hyps = set()
    e = GrammarMH(counts, hypotheses, L, GroupLength, prior_offset, NYes, NTrials, Output, steps=options.steps)
    for s, h in enumerate(break_ctrlc(e)):
        if s % options.thin:
            hyps.add(h)
            print float(h.acceptance_count) / h.proposal_count
            print h.prior, h.likelihood, h.posterior, \
                '\n\t', h.params['llt'], h.params['alpha'], h.params['beta'], \
                '\n\t', h.params['x_SET'], '\n'
            sys.stdout.flush()

    with open("Chains/Chain_"+str(a)+".pkl", 'w') as f:
        pickle.dump(hyps, f)

    return hyps

argarray = map(lambda x: [x], np.arange(options.chains))

if is_master_process():
    display_option_summary(options)

hypothesis_set = set()
for fs in MPI_map(run, argarray, progress_bar=True):
    hypothesis_set.update(fs)

with open(options.out_path, 'w') as f:
    pickle.dump(hypothesis_set, f)
