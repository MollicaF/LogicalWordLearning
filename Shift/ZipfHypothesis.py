from LOTlib.Miscellaneous import Infinity, log
from LOTlib.Hypotheses.Lexicon.RecursiveLexicon import RecursiveLexicon
from LOTlib.Hypotheses.LOTHypothesis import LOTHypothesis
from LOTlib.Eval import EvaluationException
from Model.Utilities import reachable, zipf
from Model.Grammar import makeGrammar
from fractions import Fraction

default_grammar = makeGrammar([])


def make_hyps():
    return LOTHypothesis(default_grammar, value=None, display='lambda recurse_, C, X:%s')


class KinshipLexicon(RecursiveLexicon):
    def __init__(self, alpha=0.9, s=1.0, recursive_depth_bound=10, **kwargs):
        self.alpha = alpha
        self.s = s
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
        ll = 0
        context = data[0].context # Hack same context for all likelihood
        trueset = self.make_true_data(context)
        all_poss = len(self.all_words()) * len(context.objects) ** 2
        all_poss_speakers = set([t[1] for t in trueset])
        margin = float(sum(Fraction(1, d) ** self.s for d in xrange(1, len(all_poss_speakers) + 1)))

        for datum in data:
            if (datum.word, datum.X, datum.Y) in trueset:
                pS = (context.distance[datum.Y] ** -self.s) / margin
                pRgS = (context.distance[datum.Y] ** -self.s) / sum(
                    [(context.distance[ref] ** -self.s) for ref in self(self.words[0], context, set([datum.X]))])
                ll += log( self.alpha*pS*pRgS + ((1. - self.alpha) / all_poss))
            else:
                ll += log((1. - self.alpha) / all_poss)

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
                        trueset.add((w, x, y))
            else:
                for y in self(w, context, set([fixX])):  # x must be a set here
                    trueset.add((w, fixX, y))
        return trueset
