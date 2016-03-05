from LOTlib.MPI.MPI_map import MPI_map
import pickle
import numpy as np
from numpy.random import normal
from scipy.stats import multivariate_normal as mvnormal
from scipy.misc import logsumexp
from scipy.stats import uniform, dirichlet, binom
from LOTlib import break_ctrlc
from Model import *

np.set_printoptions(threshold=np.inf)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Define the grammar
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from Model.Givens import simple_tree_objs

grammar = makeGrammar(simple_tree_objs, nterms=['Tree', 'Set', 'Gender', 'Generation', 'Ancestry', 'Paternity'])

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Load the hypotheses
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# map each concept to a hypothesis
with open('2dp_HypothesisSpace.pkl', 'r') as f:
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

class GrammarMH(object):
    def __init__(self, Counts, Hypotheses, L, GroupLength, prior_offset, Nyes, Ntrials, acc, step=0.005, steps=np.inf):
        ##MCMC
        self.samples_yielded = 0
        self.steps = steps
        self.acceptance_count = 0
        self.proposal_count = 0
        self.step = step
        self.params = dict()
        self.posterior = -np.inf
        self.likelihood = 0
        self.prior = 0
        ## Data
        self.__dict__.update(locals())
        self.N_hyps = len(Hypotheses)
        self.N_groups = len(GroupLength)
        self.nts = Counts.keys()
        self.cnts = [Counts[nt].shape[1] for nt in self.nts]
        for x in self.nts:
            self.params['count_%s' % x] = Counts[x]

        self.initialize_params()

    def initialize_params(self):
        while self.posterior == -np.inf:
            self.params['alpha'] = np.random.random()
            self.params['beta'] = np.random.random()
            self.params['llt'] = np.random.random()
            for x, c in zip(self.nts, self.cnts):
                self.params['x_%s' % x] = dirichlet.rvs(np.ones(c))[0]
            self.prior = self.compute_prior()
            self.likelihood = self.compute_likelihood()
            self.posterior = self.prior + self.likelihood

    def propose(self):
        self.proposal_count =+ 1
        proposal = dict()
        proposal['alpha'] = normal(self.params['alpha'], self.step)
        proposal['beta']  = normal(self.params['beta'], self.step)
        proposal['llt']   = normal(self.params['llt'], self.step)
        for x in self.nts:
            if False:
                inx = sample1(range(len(self.params['x_%s' % x])))
                simplex = self.params['x_%s' % x]
                simplex[inx] = max(0,normal(self.params['x_%s' % x][inx], self.step))
            else:
                simplex = np.maximum(0,
                                     mvnormal.rvs(self.params['x_%s' % x],
                                                  self.step * np.eye(len(self.params['x_%s' % x]))))
            simplex = simplex + min(simplex[np.nonzero(simplex)])
            proposal['x_%s'%x] = simplex / np.sum(simplex)
        return proposal

    def compute_prior(self, params=None):
        if params is None:
            params = self.params
        prior = 0
        prior = prior + uniform.logpdf(params['llt'], 0, 2)
        prior = prior + uniform.logpdf(params['alpha'], 0, 1)
        prior = prior + uniform.logpdf(params['beta'], 0, 1)
        for x, c in zip(self.nts, self.cnts):
            prior = prior + dirichlet.logpdf(params['x_%s'%x], np.ones(c))
        return prior

    def compute_likelihood(self, params=None):
        if params is None:
            params = self.params
        pos = 0
        likelihood = 0
        for g in xrange(0, self.N_groups-1):
            priors = np.ones(self.N_hyps) * self.prior_offset
            for x in self.nts:
                priors = priors + np.dot(self.params['count_%s'%x], np.log(params['x_%s'%x]))
            posteriors = (np.array(self.L[g])/params['llt']) + priors.T
            w = np.exp(posteriors - logsumexp(posteriors))

            for _ in xrange(1, self.GroupLength[g]):
                ps = (1 - params['alpha']) * params['beta'] + np.dot(w, self.acc[pos])
                if np.sum(ps) > 1:
                    likelihood = -np.inf
                    break
                likelihood = likelihood + binom.logpmf(self.Nyes[pos], self.Ntrials[pos], ps)
                pos =+ 1

        return likelihood

    def compute_posterior(self, params=None):
        if params is None:
            params = self.params
        return self.compute_prior(params) + self.compute_likelihood(params)

    def update_params(self, params):
        for k in params.keys():
            self.params[k] = params[k]

    def __iter__(self):
        return self

    def next(self):
        if self.samples_yielded >= self.steps:
            raise StopIteration
        else:
            prop = self.propose()
            p_post = self.compute_posterior(params=prop)
            p = max(0, min(1, np.exp(p_post - self.posterior)))
            if p_post > -np.inf and flip(p):
                self.posterior = p_post
                self.likelihood = self.compute_likelihood(prop)
                self.prior = self.compute_prior(prop)
                self.update_params(prop)
                self.acceptance_count =+ 1

            self.samples_yielded = self.samples_yielded + 1
            return self

def run(a):
    hyps = set()
    e = GrammarMH(counts, hypotheses, L, GroupLength, prior_offset, NYes, NTrials, Output, steps=1000000)
    for s, h in enumerate(break_ctrlc(e)):
        if s % 1000:
            hyps.add(h)
            #print h.prior, h.likelihood, h.posterior, \
            #    '\n\t', h.params['llt'], h.params['alpha'], h.params['beta'], \
            #    '\n\t', h.params['x_SET'], '\n'

    with open("Chains/Chain_"+str(a)+".pkl", 'w') as f:
        pickle.dump(hyps, f)

    return hyps

argarray = map(lambda x: [x], np.arange(40))
hypothesis_set = set()
for fs in MPI_map(run, argarray, progress_bar=True):
    hypothesis_set.update(fs)

with open("DidItWork.pkl", 'w') as f:
    pickle.dump(hypothesis_set, f)
