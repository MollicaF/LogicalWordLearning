from LOTlib.Hypotheses.Hypothesis import *
import numpy as np
from scipy.misc import logsumexp
from scipy.stats import dirichlet, binom

class AlphaBetaGrammarMH(Hypothesis):
    def __init__(self, Counts, Hypotheses, L, GroupLength, prior_offset, Nyes, Ntrials, ModelResponse, value=None,  scale=600):
        """
            Counts - nonterminal -> #h x #rules counts
            Hypotheses - #h
            L          - group -> #h x 1 array
            GroupLength   - #groups (vector)  - contains the number of trials per group
            Nyes          - #item ( #item = sum(GroupLength))
            Ntrials       - #item
            ModelResponse - #h x #item - each hypothesis' response to the i'th item (1 or 0)
        """
        assert sum(GroupLength) == len(Nyes) == len(Ntrials)

        self.__dict__.update(locals())

        self.N_hyps = len(Hypotheses)
        self.N_groups = len(GroupLength)

        self.nts    = Counts.keys() # all nonterminals
        self.nrules = { nt: Counts[nt].shape[1] for nt in self.nts} # number of rules for each nonterminal

        # the dirichlet prior on parameters
        self.value_prior = { nt: np.ones(self.nrules[nt]) for nt in self.nts }
        self.set_value(value)
        Hypothesis.__init__(self)

    def set_value(self, value):
        if value is None:
            self.value = dict()
            for nt in self.nts:
                self.value[nt] = dirichlet.rvs(np.ones(self.nrules[nt]))[0] ## TODO: Check [0] here
        else:
            self.value = value

    def compute_likelihood(self, data, **kwargs):
        # The likelihood of the human data
        assert len(data) == 0

        # compute each hypothesis' prior, fixed over all data
        priors = np.ones(self.N_hyps) * self.prior_offset #   #h x 1 vector
        for nt in self.nts: # sum over all nonterminals
            priors = priors + np.dot(np.log(self.value[nt]), self.Counts[nt].T) # TODO: Check .T

        pos = 0 # what response are we on?
        likelihood = 0.0
        for g in xrange(self.N_groups): ## TODO: Check offset
            posteriors =  self.L[g] + priors # posterior score
            posteriors = np.exp(posteriors - logsumexp(posteriors)) # posterior probability

            # Now compute the probability of the human data
            for _ in xrange(1, self.GroupLength[g]):
                # ps = (1 - params['alpha']) * params['beta'] + params['alpha'] * np.dot(w, self.acc[pos])
                ps = np.dot(posteriors, self.ModelResponse[pos]) # model probabiltiy of saying yes # TODO: Check matrix multiply

                likelihood += binom.logpmf(self.Nyes[pos], self.Ntrials[pos], ps)
                pos = pos + 1

        self.likelihood = likelihood
        return likelihood

    def compute_prior(self):
        # prior = prior + norm.logcdf(params['llt'], 0.3, 0.003)
        # prior = prior + uniform.logcdf(params['alpha'], 0, 1)
        # prior = prior + uniform.logcdf(params['beta'], 0, 1)
        self.prior = -1*sum([np.sum(dirichlet.logpdf(self.value[nt], self.value_prior[nt])) for nt in self.nts])
        return self.prior


    def propose(self, epsilon=1e-5):
        # should return is f-b, proposal
        # uses epsilon smoothing to keep away from 0,1

        fb = 0.0

        # change value
        newvalue = dict()
        for nt in self.nts:
            a = dirichlet.rvs(self.value[nt] * self.scale)[0] + epsilon
            newvalue[nt] = a / np.sum(a)
            #newvalue[nt] = dirichlet.rvs(self.value[nt] * self.scale)[0]*(1.0-epsilon) + epsilon/2.0
            # This doesn't guarantee a simplex
            fb += dirichlet.logpdf(newvalue[nt],self.value[nt]) - dirichlet.logpdf(self.value[nt],newvalue[nt])

        # make a new proposal. DON'T copy the matrices, but make a new value
        prop = AlphaBetaGrammarMH(self.Counts, self.Hypotheses, self.L, self.GroupLength, self.prior_offset, self.Nyes, \
                                  self.Ntrials, self.ModelResponse, value=newvalue, scale=self.scale)

        return prop, fb
