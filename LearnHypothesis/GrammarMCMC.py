from LearnHypothesis import *
import numpy
######################################################################################################
#   Option Parser
######################################################################################################
parser = OptionParser()
parser.add_option("--human", dest='data_loc', type='string', help="Generalization Data location",
                  default='human.data')
parser.add_option("--space", dest='space_loc', type='string', help="Hypothesis Space location",
                  default='2dp_HypothesisSpace.pkl')
parser.add_option("--out", dest="out_path", type="string", help="Output file (a csv of samples)",
                  default="FullSpace")
parser.add_option("--viz", dest='viz', action='store_true', help="Make Vizualization Files?")


parser.add_option("--samples", dest="samples", type="int", default=1000, help="Number of samples desired")
parser.add_option("--skip", dest="skip", type="int", default=100, help="Number of steps between saved samples")

(options, args) = parser.parse_args()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Define the grammar
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from Model.Givens import simple_tree_objs

grammar = makeGrammar(simple_tree_objs, nterms=['Tree', 'Set', 'Gender', 'Generation', 'Ancestry', 'Paternity'])

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Load the hypotheses
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
from LOTlib.Inference.GrammarInference import create_counts

# Decide which rules to use
which_rules = [r for r in grammar if r.nt in ['SET']]

counts, sig2idx, prior_offset = create_counts(grammar, hypotheses, which_rules=which_rules)

print "# Computed counts for each hypothesis & nonterminal"

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Make model files for vizualization
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if options.viz:
    numpy.savetxt('Viz/Likelihoods_' + options.out_path + '.csv', numpy.array(L).T)

    with open('Viz/Model_' + options.out_path + '.csv', 'w') as f:
        f.writelines('\n'.join([','.join([str(r) for r in h]) for h in numpy.array(Output).T]))

    with open('Viz/Counts_' + options.out_path + '.csv', 'w') as f:
        f.writelines('\n'.join([','.join([str(r) for r in h]) for h in counts['SET']]))

    for r in which_rules: print r

from LOTlib.Inference.GrammarInference.SimpleGrammarHypothesis import SimpleGrammarHypothesis
from LOTlib.Inference.GrammarInference.FullGrammarHypothesis import FullGrammarHypothesis

from LOTlib.Inference.Samplers.MetropolisHastings import MHSampler

h0 = SimpleGrammarHypothesis(counts, L, GroupLength, prior_offset, NYes, NTrials, Output)
#h0 = FullGrammarHypothesis(counts, L, GroupLength, prior_offset, NYes, NTrials, Output)

writ = []
mhs = MHSampler(h0, [], options.samples, skip=options.skip)
for s, h in break_ctrlc(enumerate(mhs)):

    if isinstance(h, SimpleGrammarHypothesis):
        a = str(mhs.acceptance_ratio()) + ',' + str(h.prior) + ',' + str(h.likelihood) +  ',RULES,' +\
            ','.join([str(x) for x in h.value['SET'].value])
    else:
        assert isinstance(h, FullGrammarHypothesis)
        a = str(mhs.acceptance_ratio()) + ',' + str(h.prior) + ',' + str(h.likelihood) +  ',' + \
        str(h.value['alpha'].value[0]) + ',' + str(h.value['beta'].value[0]) + ',' + \
        str(h.value['prior_temperature']) + ',' + str(h.value['likelihood_temperature'])  + ',RULES,' +\
            ','.join([str(x) for x in h.value['rulep']['SET'].value])
    print a
    writ.append(a)

with open('Viz/' + options.out_path + '.csv', 'w') as f:
    f.writelines('\n'.join(writ))
