from LOTlib.Miscellaneous import display_option_summary
from LOTlib.MPI.MPI_map import MPI_map, is_master_process
import pickle
import numpy as np
from Model import *
from optparse import OptionParser
from Model.GrammarMH2 import AlphaBetaGrammarMH
from LOTlib.Inference.Samplers.MetropolisHastings import MHSampler
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
parser.add_option("--scale", dest="scale", type="float", help="Scale for the dirichlet proposal.", default=600.)

parser.add_option("--steps", dest="steps", type="int", default=1000000, help="Number of samples to run")
parser.add_option("--thin", dest="thin", type="int", default=100, help="Number of steps between saved samples")
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
    for i, line in enumerate(f.readlines()):
        entry = line.strip('\n').split(',')
        if i < 1:
            order = entry
        else:
            data = [KinshipData('Word', 'ego', entry[2], simple_tree_context),
                    KinshipData('Word', 'ego', entry[3], simple_tree_context)]
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
    h0 = AlphaBetaGrammarMH(counts, hypotheses, L, GroupLength, prior_offset, NYes, NTrials, Output, scale=options.scale)
    mhs = MHSampler(h0, [], options.steps)
    for s, h in enumerate(mhs):
        if s % options.thin == 0:
            a = str(mhs.acceptance_ratio()) + ',' + str(h.prior) + ',' + str(h.likelihood) + ',' + ','.join([str(x) for x in h.value['SET']])
            print a
            hyps.add(a)
    with open("Chains/Chain_"+str(a)+".pkl", 'w') as f:
        pickle.dump(hyps, f)
    return hyps

argarray = map(lambda x: [x], np.arange(options.chains))

if is_master_process():
    display_option_summary(options)

hypothesis_set = set()
for fs in MPI_map(run, argarray, progress_bar=False):
    hypothesis_set.update(fs)

with open(options.out_path, 'w') as f:
    pickle.dump(hypothesis_set, f)
