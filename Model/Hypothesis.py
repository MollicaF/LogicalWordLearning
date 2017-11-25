from LOTlib.Miscellaneous import Infinity, log, q
from LOTlib.Hypotheses.Lexicon.RecursiveLexicon import RecursiveLexicon
from LOTlib.Hypotheses.LOTHypothesis import LOTHypothesis
from LOTlib.Eval import EvaluationException, RecursionDepthException
from Utilities import reachable, zipf
from LOTlib.Inference.GrammarInference.Precompute import create_counts #
from Grammar import makeGrammar
import numpy as np

default_grammar = makeGrammar([])


def make_hyps():
    return LOTHypothesis(default_grammar, value=None, display='lambda recurse_, C, X:%s')

class KinshipLexicon(RecursiveLexicon):

    def __init__(self, alpha=0.9, epsilon=0.0, s=0.0, recursive_depth_bound=10, **kwargs):
        self.alpha = alpha
        self.s = s
        self.epsilon = epsilon
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

    def compute_likelihood(self, data, eval=False, **kwargs):
        constants = dict()
        ll = 0
        for di, datum in enumerate(data):
            # Cache constants
            if datum.context in constants.keys():
                trueset = constants[datum.context][0]
                egoset = constants[datum.context][1]
                egoRef = constants[datum.context][2]
                all_poss = constants[datum.context][3]
            else:
                try:
                    trueset = self.make_true_data(datum.context)
                    egoset = self.make_true_data(datum.context, fixX=datum.context.ego)
                    egoRef = dict()
                    for w in self.all_words():
                        rs = [t[2] for t in self.make_word_data(w, datum.context, fixX=datum.context.ego)]
                        egoRef[w] = sum(map(lambda r: zipf(r, self.s, datum.context, len(datum.context.objects)), rs))
                    all_poss = len(datum.context.objects)

                    constants[datum.context] = [trueset, egoset, egoRef, all_poss]
                except RecursionDepthException:
                    self.likelihood = -Infinity
                    self.update_posterior()
                    return self.likelihood
                    # Make sure recursion is well formed
            if di == 0:
                if not eval and not self.canIrecurse(data, trueset):
                    self.likelihood = -Infinity
                    self.update_posterior()
                    return self.likelihood
            # Calculate the single point likelihood
            p = (1. - self.alpha) / all_poss
            if (datum.word, datum.X, datum.Y) in trueset:
                # Probability it's true and speaker centric
                pT = self.alpha * (1. - self.epsilon)
                # Probability of the speaker
                # pS = zipf(datum.X, self.s, datum.context, len(datum.context.objects))
                # Probability of the referent given the speaker and the word
                pr = zipf(datum.Y, self.s, datum.context, len(datum.context.objects))
                hout = self(datum.word, datum.context, set([datum.X]))
                hout.discard(datum.X)
                Z = sum(map(lambda r: zipf(r, self.s, datum.context, len(datum.context.objects)), hout))
                p += pT * (pr / Z)
            if (datum.word, datum.X, datum.Y) in egoset:
                # Probability it's true and ego-centric
                pT = self.alpha * self.epsilon
                # Probability of the speaker
                # pS = zipf(datum.X, self.s, datum.context, len(datum.context.objects))
                # Probability of the referent
                pR = zipf(datum.Y, self.s, datum.context, len(datum.context.objects)) / egoRef[datum.word]
                p += pT * pR
            ll += log(p)

        self.likelihood = ll / self.likelihood_temperature

        self.update_posterior()
        return self.likelihood

    def compute_L_likelihood(self, data, eval=False, **kwargs):
        constants = dict()
        ll = 0
        for di, datum in enumerate(data):
            # Cache constants
            if datum.context in constants.keys():
                trueset = constants[datum.context][0]
                all_poss = constants[datum.context][3]
            else:
                try:
                    trueset = self.make_true_data(datum.context)
                    all_poss = len(datum.context.objects)

                    constants[datum.context] = [trueset, all_poss]
                except RecursionDepthException:
                    self.likelihood = -Infinity
                    self.update_posterior()
                    return self.likelihood
                    # Make sure recursion is well formed
            if di == 0:
                if not eval and not self.canIrecurse(data, trueset):
                    self.likelihood = -Infinity
                    self.update_posterior()
                    return self.likelihood
            # Calculate the single point likelihood
            p = (1. - self.alpha) / all_poss
            if (datum.word, datum.X, datum.Y) in trueset:
                p += self.alpha * len(trueset)**-1
            ll += log(p)

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
                        if x != y:
                            trueset.add( (w, x, y) )
            else:
                for y in self(w, context, set([fixX])):  # x must be a set here
                    if fixX != y:
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
                    if x != y:
                        trueset.add((word, x, y))
        else:
            for y in self(word, context, set([fixX])):  # x must be a set here
                if fixX != y:
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
        relinx = [(k[2], inx[k]) for k in inx.keys() if k[1] == 'recurse_']
        if len(relinx) == 0:
            return True
        counts = np.sum(counts['SET'], axis=0)


        F1s = []
        for wi, w in enumerate(self.all_words()):
            wd = [dp for dp in d if dp[0] == w] # Word Data
            pw = [dp for dp in trueset if dp[0] == w] # Proposed Word Data
            pId = [dp for dp in wd if dp in pw] # Proposed Word Data Observed
            precision = float(len(set(pId))) / float(len(pw) + 1e-6)
            recall = float(len(pId)) / float(len(wd) + 1e-6)
            f1 = (2.*precision*recall) / (precision + recall + 1e-6)
            i = [ri[1] for ri in relinx if ri[0] == q(w)]
            F1s.append((counts[i], w, f1, precision, recall))
            if counts[i] >= 1 and f1 <= self.alpha * 2./ 3.:
                return False

        return True


def updateLexicon(lexicon, grammar=default_grammar, **kwargs):
    h = KinshipLexicon(**kwargs)
    for w in lexicon.all_words():
        hw = lexicon.value[w]
        hw.grammar = grammar
        h.set_word(w, hw)
    return h


if __name__ == "__main__":

    from Model.Givens import english_words, four_gen_tree_context, english
    from Model.Data import makeTreeLexiconData, makeZipfianLexiconData, engFreq
    from Grammar import makeGrammar
    #rgrammar = makeGrammar(['Mira','Snow','charming','rump','neal','baelfire','Emma','Regina','henry','Maryann','ego'],
    #                         compositional=True, terms=['X','objects','all'], nterms=['Tree', 'Set', 'Gender'],
    #                         recursive=True, words=english_words)
    gramm = makeGrammar(four_gen_tree_context.objects,nterms=['Tree','Set','Gender','Generation'])
    h0 = KinshipLexicon(alpha=0.9, epsilon=0.99, s=0.0)
    for w in english_words:
        h0.set_word(w, LOTHypothesis(gramm, display='lambda recurse_, C, X: %s'))

    for _ in xrange(10):
        dat = makeZipfianLexiconData(english, four_gen_tree_context, engFreq, n=10)
        print h0.compute_posterior(dat)
