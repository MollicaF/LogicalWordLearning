import pickle
import numpy
from LOTlib.Miscellaneous import setup_directory
from Model import *

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set up some logging
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

LOG = "stan-log"
setup_directory(LOG) # make a directory for ourselves

# Make sure we print the entire matrix
numpy.set_printoptions(threshold=numpy.inf)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Define the grammar
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from Model.Givens import simple_tree_objs

grammar = makeGrammar(simple_tree_objs,  nterms=['Tree', 'Set', 'Gender', 'Generation', 'Ancestry', 'Paternity'])

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Load the hypotheses
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# map each concept to a hypothesis
with open('Snowcharming.pkl', 'r') as f:
    hypotheses = list(pickle.load(f))

print "# Loaded hypotheses: ", len(hypotheses)

#for h in hypotheses:
    #print h 
#hypotheses = hypotheses[:10] # TODO: REMOVE THIS LINE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Load the human data
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from Model.Givens import simple_tree_context

L           = [] # each hypothesis's cumulative likelihood to each data point
GroupLength = []
NYes        = []
NTrials     = []
Output      = []

# cache the set for each hypothesis
for h in hypotheses:
    h.cached_set = h('Word', simple_tree_context, set(['ego']))

with open("human.data", 'r') as f:
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
            L.append([ h.compute_likelihood(data) for h in hypotheses] )

            gl = 0
            for j in xrange(5, len(entry)): # for each predictive response
                if entry[j] not in ('NA', 'NA\n'):
                    NYes.append(   int(entry[j]) )
                    NTrials.append(int(entry[4]))

                    Output.append( [ 1*(order[j] in h.cached_set) for h in hypotheses])

                    gl += 1

            GroupLength.append(gl)

print "# Loaded %s observed rows" % len(NYes)
print "# Organized %s groups" % len(GroupLength)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Get the rule count matrices
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from LOTlib.GrammarInference.GrammarInference import create_counts

# Decide which rules to use
which_rules = [ r for r in grammar if r.nt in ['SET'] ]

counts, sig2idx, prior_offset = create_counts(grammar, hypotheses, which_rules=which_rules, log=LOG)

print "# Computed counts for each hypothesis & nonterminal"

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Run Stan
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import pystan
from LOTlib.GrammarInference.GrammarInference import make_stan_code

stan_code = make_stan_code(counts, template='model-DMPCFG-Binomial.stan', log=LOG) #NOT THE DEFAULT TEMPLATE MAKE ONE WITH LL TEMP template="location"

stan_data = {
    'N_HYPOTHESES': len(hypotheses),
    'N_DATA': len(NTrials),
    'N_GROUPS': len(GroupLength),

    'PriorOffset': prior_offset,

    'L': L,
    'GroupLength':GroupLength,

    'NYes':    NYes,
    'NTrials': NTrials,
    'Output': Output
}
stan_data.update({ 'count_%s'%nt:counts[nt] for nt in counts.keys()}) # add the prior counts. Note we have to convert their names here

print "# Summary of model size:"
for nt in counts:
    print "# Matrix %s is %s x %s" % (nt, counts[nt].shape[0], counts[nt].shape[1])

sm = pystan.StanModel(model_code=stan_code)

print "# Created Stan model"

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Run Stan optimization and bootstrap
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

fit = sm.optimizing(data=stan_data)

for k in fit:
    if isinstance(fit[k].tolist(), list):
        for i, v in enumerate(fit[k].tolist()):
            print "real", k, i, v
    else:
        print "real", k, 0, fit[k].tolist()


## And bootstrap
#import scipy.stats

#y = numpy.array(NYes, dtype=float) # so we can take ratios
#n = numpy.array(NTrials)

#for rep in xrange(100):

    ## Resample our yeses
    #stan_data['NYes'] = scipy.stats.binom.rvs(n, y/n)

    ## and re-run
    #fit = sm.optimizing(data=stan_data)

    #for k in fit:
        #if isinstance(fit[k].tolist(), list):
            #for i, v in enumerate(fit[k].tolist()):
                #print "boot", k, i, v
        #else:
            #print "boot", k, 0, fit[k].tolist()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Run Stan sampling
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# samples = sm.sampling(data=stan_data, iter=100, chains=4, sample_file="./stan_samples")

# print "# Running"
# fit = pystan.stan(model_code=stan_code,  data=stan_data, warmup=50, iter=500, chains=4)
# print(fit)

## And save
# with open("stan_fit.pkl", 'w') as f:
#     pickle.dump(fit, f)

# fit.plot().savefig("fig.pdf")

# print(fit.extract(permuted=True))
