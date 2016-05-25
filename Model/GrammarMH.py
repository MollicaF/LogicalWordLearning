import numpy as np
from copy import copy
from numpy.random import normal
from scipy.misc import logsumexp
from scipy.stats import uniform, dirichlet, binom, gamma, norm
from Model import *

class GrammarMH(object):
    def __init__(self, Counts, Hypotheses, L, GroupLength, prior_offset, Nyes, Ntrials, acc, step=0.005, scale=600, steps=np.inf):
        ##MCMC
        self.scale = scale
        self.samples_yielded = 0
        self.steps = steps
        self.acceptance_count = 0
        self.proposal_count = 0
        self.step = step
        self.params = dict()
        self.posterior = -np.inf
        self.likelihood = 0
        self.prior = 0
        self.forward = 1
        self.backward = 1
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
            #self.params['alpha'] = np.random.random()
            #self.params['beta'] = np.random.random()
            self.params['llt'] = 1 #np.random.random()
            for x, c in zip(self.nts, self.cnts):
                self.params['x_%s' % x] = dirichlet.rvs(np.ones(c))[0]
            self.prior = self.compute_prior()
            self.likelihood = self.compute_likelihood()
            self.posterior = self.prior + self.likelihood

    def propose(self):
        self.forward = 0
        self.backward = 0
        self.proposal_count = self.proposal_count + 1
        proposal = dict()
        #proposal['alpha'] = normal(self.params['alpha'], self.step)
        #proposal['beta'] = normal(self.params['beta'], self.step)
        proposal['llt'] = 1 #min(max(0, normal(self.params['llt'], self.step)), 1)
        for x in self.nts:
            simplex = dirichlet.rvs(self.params['x_%s' % x].flatten()* self.scale) + \
                      0.0000000001 * np.ones(self.params['x_%s' % x].flatten().shape)
            self.forward += np.sum(gamma.logcdf(simplex, self.params['x_%s' % x] * self.scale))
            self.backward += np.sum(gamma.logcdf(self.params['x_%s' % x], simplex * self.scale))
            proposal['x_%s' % x] = simplex #/ np.sum(simplex)
        return proposal

    def compute_prior(self, params=None):
        if params is None:
            params = self.params
        prior = 0
        prior = prior + norm.logcdf(params['llt'], 0.3, 0.003)
        #prior = prior + uniform.logcdf(params['alpha'], 0, 1)
        #prior = prior + uniform.logcdf(params['beta'], 0, 1)
        for x, c in zip(self.nts, self.cnts):
            prior = prior + np.sum(gamma.logcdf(params['x_%s' % x], np.ones(self.params['x_%s' % x].shape)))
        return prior

    def compute_likelihood(self, params=None):
        if params is None:
            params = self.params
        pos = 0
        likelihood = 0
        for g in xrange(0, self.N_groups - 1):
            priors = np.ones(self.N_hyps) * self.prior_offset
            for x in self.nts:
                priors = priors + np.dot(np.log(params['x_%s' % x]), self.params['count_%s' % x].T)
            posteriors = (np.array(self.L[g]) / params['llt']) + priors.flatten()
            #print np.array(self.L[g]).shape, priors.flatten().shape, posteriors.shape
            w = np.exp(posteriors - logsumexp(posteriors))

            for _ in xrange(1, self.GroupLength[g]):
                #ps = (1 - params['alpha']) * params['beta'] + params['alpha'] * np.dot(w, self.acc[pos])
                ps = min(1, np.dot(w, self.acc[pos]))
                likelihood = likelihood + binom.logcdf(self.Nyes[pos], self.Ntrials[pos], ps)
                pos = pos + 1

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
            p = max(0, min(1, np.exp(p_post - self.posterior + self.backward - self.forward)))
            if p_post > -np.inf and flip(p):
                self.posterior = p_post
                self.likelihood = self.compute_likelihood(prop)
                self.prior = self.compute_prior(prop)
                self.update_params(prop)
                self.acceptance_count = self.acceptance_count + 1
            self.samples_yielded = self.samples_yielded + 1
            if self.acceptance_count / float(self.samples_yielded) < 0.1:
                self.scale = 2000
            print self.acceptance_count/float(self.samples_yielded), p_post, self.posterior
            return self

