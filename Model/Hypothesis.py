from LOTlib.Miscellaneous import Infinity, log
from LOTlib.Hypotheses.Lexicon.RecursiveLexicon import RecursiveLexicon
from LOTlib.Hypotheses.LOTHypothesis import LOTHypothesis
from LOTlib.Eval import EvaluationException, RecursionDepthException
from Utilities import reachable
from LOTlib.Miscellaneous import q, Infinity
from LOTlib.Inference.GrammarInference.Precompute import create_counts
from Grammar import makeGrammar
import numpy as np

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

    def compute_word_likelihood(self, data, word):
        data = [dp for dp in data if dp.word == word]
        assert len(data) > 0
        constants = dict()
        ll = 0
        for datum in data:
            if datum.context in constants.keys():
                trueset = constants[datum.context][0]
                all_poss = constants[datum.context][1]
            else:
                try:
                    if datum.context.ego is None:
                        trueset = self.make_word_data(word, datum.context)
                    else:
                        trueset = self.make_word_data(word, datum.context, fixX=datum.context.ego)

                    all_poss = len(datum.context.objects) ** 2
                    constants[datum.context] = [trueset, all_poss]
                except RecursionDepthException:
                    self.likelihood = -Infinity
                    self.update_posterior()
                    return self.likelihood

            if (datum.word, datum.X, datum.Y) in trueset:
                ll += log(self.alpha / len(trueset) + ((1. - self.alpha) / all_poss))
            else:
                ll += log((1. - self.alpha) / all_poss)

        self.likelihood = ll / self.likelihood_temperature

        self.update_posterior()
        return self.likelihood

    def compute_likelihood(self, data, **kwargs):
        constants = dict()
        ll = 0
        for di, datum in enumerate(data):
            if datum.context in constants.keys():
                trueset = constants[datum.context][0]
                all_poss = constants[datum.context][1]
            else:
                try:
                    if datum.context.ego is None:
                        trueset = self.make_true_data(datum.context)
                        #trueset = {w: self.make_word_data(w, datum.context) for w in self.all_words()}
                        all_poss = len(self.all_words()) * len(datum.context.objects) ** 2
                    else:
                        trueset = self.make_true_data(datum.context, fixX=datum.context.ego)
                        #trueset = {w: self.make_word_data(w, datum.context, fixX=datum.context.ego)
                        #           for w in self.all_words()}
                        all_poss = len(self.all_words())*len(datum.context.objects)

                    constants[datum.context] = [trueset, all_poss]
                except RecursionDepthException:
                    self.likelihood = -Infinity
                    self.update_posterior()
                    return self.likelihood

            # Check to see if you can recurse and if that matters
            if di == 0:
                if not self.canIrecurse(data, trueset):
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


    def make_word_data(self, word, context, fixX=None):
        """
        Return a set of relation tuples that are true for a single word
        """
        trueset = set()
        if fixX is None:
            for x in context.objects:
                for y in self(word, context, set([x])):  # x must be a set here
                    trueset.add((word, x, y))
        else:
            for y in self(word, context, set([fixX])):  # x must be a set here
                trueset.add((word, fixX, y))
        return trueset

    def canIrecurse(self, data, trueset):
        d = [(datum.word, datum.X, datum.Y) for datum in data]

        hyps = [self.value[w] for w in self.all_words()]
        try:
            grammar = hyps[0].grammar
        except:
            return True # Because if it doesn't have a grammar it's a force function
        counts, inx, _ = create_counts(grammar, hyps)
        counts = np.sum(counts['SET'], axis=0)
        relinx = [(k[2], inx[k]) for k in inx.keys() if k[1] == 'recurse_']

        F1s = []
        for wi, w in enumerate(self.all_words()):
            wd = [dp for dp in d if dp[0] == w] # Word Data
            pw = [dp for dp in trueset if dp[0] == w] # Proposed Word Data
            pId = [dp for dp in pw if dp in wd] # Proposed Word Data Observed
            precision = float(len(pId)) / float(len(pw) + 1e-6)
            recall = float(len(pId)) / float(len(wd) + 1e-6)
            f1 = (2.*precision*recall) / (precision + recall + 1e-6)
            i = [ri[1] for ri in relinx if ri[0] == q(w)]
            F1s.append((counts[i], w, f1))
            if counts[i] >= 1 and f1 <= self.alpha:
                return False
        print F1s

        return True

if __name__ == "__main__":

    from Model.Givens import english_words, four_gen_tree_context, english
    from Model.Data import makeLexiconData
    from Grammar import makeGrammar
    rgrammar = makeGrammar(['Mira','Snow','charming','rump','neal','baelfire','Emma','Regina','henry','Maryann','ego'],
                             compositional=True, terms=['X','objects','all'], nterms=['Tree', 'Set', 'Gender'],
                             recursive=True, words=english_words)
    data = makeLexiconData(english, four_gen_tree_context)
    h0 = KinshipLexicon(alpha=0.9)
    for w in english_words:
        h0.set_word(w, LOTHypothesis(rgrammar, display='lambda recurse_, C, X: %s'))

    tru = h0.make_true_data(four_gen_tree_context)
    print h0.canIrecurse(data, tru)
