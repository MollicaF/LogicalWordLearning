from LOTlib.Miscellaneous import Infinity, log
from LOTlib.Hypotheses.Lexicon.RecursiveLexicon import RecursiveLexicon
from LOTlib.Hypotheses.LOTHypothesis import LOTHypothesis
from LOTlib.Eval import EvaluationException
from Utilities import reachable
from Grammar import makeGrammar

default_grammar = makeGrammar([])


def make_hyps():
    return LOTHypothesis(default_grammar, value=None, display='lambda recurse_, C, X:%s')

class KinshipLexicon(RecursiveLexicon):

    def __init__(self, alpha=0.9, recursive_depth_bound=10, **kwargs):
        self.alpha = alpha
        self.recursive_depth_bound = recursive_depth_bound
        self.point_ll = 0
        RecursiveLexicon.__init__(self, alpha=self.alpha, **kwargs)

    def __call__(self, *args):
        try:
            return RecursiveLexicon.__call__(self, *args)
        except EvaluationException:
            return set()

    def compute_prior(self):
        if reachable(self):
            return -Infinity
        else:
            self.prior = sum([x.compute_prior() for x in self.value.values()]) / self.prior_temperature
            self.update_posterior()
        return self.prior

    def compute_likelihood(self, data, **kwargs):
        constants = dict()
        ll = 0
        for datum in data:
            if datum.context in constants.keys():
                trueset = constants[datum.context][0]
                all_poss = constants[datum.context][1]
            else:
                try:
                    if datum.context.ego is None:
                        trueset = self.make_true_data(datum.context)
                    else:
                        trueset = self.make_true_data(datum.context, fixX=datum.context.ego)

                    all_poss = len(self.all_words())*len(datum.context.objects)**2
                    constants[datum.context] = [trueset, all_poss]
                except RecursionDepthException:
                    self.likelihood = -Infinity
                    self.update_posterior()
                    return self.likelihood

            if (datum.word, datum.X, datum.Y) in trueset:
                ll += log(self.alpha/len(trueset) + ((1.-self.alpha)/all_poss))
            else:
                ll += log((1.-self.alpha)/all_poss)

        self.likelihood = ll / self.likelihood_temperature

        self.update_posterior()
        return self.likelihood


    def compute_posterior(self, data, **kwargs):
        self.compute_likelihood(data)
        self.compute_prior()
        self.update_posterior()
        return self.prior, self.likelihood

    def make_true_data(self, context, fixX=None):
        """
        Return a set of relation tuples that are true
        """

        trueset = set()
        for w in self.all_words():
            if fixX is None:
                for x in context.objects:
                    for y in self(w, context, set([x])):  # x must be a set here
                        trueset.add( (w, x, y) )
            else:
                for y in self(w, context, set([fixX])):  # x must be a set here
                    trueset.add( (w, fixX, y) )
        return trueset



'''
    def compute_likelihood(self, data, **kwargs):
        context = data[0].context # Hack assuming you have the same context for all datapoints
        try:
            if context.ego is None:
                trueset = self.make_true_data(context)
            else:
                trueset = self.make_true_data(context, fixX=context.ego)

            all_poss = len(self.all_words())*len(context.objects)**2

            ll = 0
            for datum in data:
                if (datum.word, datum.X, datum.Y) in trueset:
                    ll += log(self.alpha/len(trueset) + ((1.-self.alpha)/all_poss))
                else:
                    ll += log((1.-self.alpha)/all_poss)

            self.likelihood = ll / self.likelihood_temperature

        except RecursionDepthException:
            self.likelihood = -Infinity

        self.update_posterior()
        return self.likelihood
'''