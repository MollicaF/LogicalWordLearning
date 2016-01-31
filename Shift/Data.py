from collections import defaultdict
from random import shuffle
from LOTlib.Miscellaneous import flip, sample1, weighted_sample

class KinshipData:
    def __init__(self, word, X, Y, context):
        self.__dict__.update(locals())
        self.X = X
        self.Y = Y
        self.word = word
        self.context = context

    def __repr__(self):
        return 'KinshipData('+self.word + ',' + self.X + ',' + self.Y + ')'


class KinshipContext:
    def __init__(self, objects, relations, features, ego=None, distance=None):

        self.__dict__.update(locals())
        self.ego = ego
        self.distance = distance
        self.features = features
        self.objects = objects

        self.parents = defaultdict(set)
        self.spouses = defaultdict(set)
        self.children = defaultdict(set)

        for r, x, z in relations:
            if r == 'parent':

                self.parents[z].add(x)
                self.children[x].add(z)
            elif r == 'spouse':
                self.spouses[x].add(z)
            else:
                assert False, '\t'.join([r, x, z])

    def __repr__(self):
        return self.objects[0]

from Model.Utilities import zipf


def makeVariableLexiconData(lexicon, word, context, n=100, s=1.0, alpha=0.9, verbose=False):
    data = []
    true_set = lexicon.make_true_data(context)
    all_poss_speakers = [ t[1] for t in true_set ]
    p = [ zipf(t, s, context, len(context.objects)) for t in all_poss_speakers ]

    for i in xrange(n):
        if flip(alpha):
            speaker = weighted_sample(all_poss_speakers, probs=p)
            referents = lexicon(word, context, set([speaker]))
            p1 = [ zipf(t, s, context, len(context.objects)) for t in referents ]
            referent = weighted_sample(referents, probs=p1)
            if verbose:
                print "True data:", i, word, speaker, referent
            data.append(KinshipData(word, speaker, referent, context))
        else:
            x = sample1(context.objects)
            y = sample1(context.objects)
            if verbose:
                print "Noise data:", i, word, x, y
            data.append(KinshipData(word, x, y, context))
    if verbose:
        print lexicon.compute_likelihood(data)
    return data


if __name__ == "__main__":
    from Model.Givens import grandma, uncle, mother, brother
    from FeatureGiven import original_tree_context

    d = makeVariableLexiconData(grandma, 'grandma',  original_tree_context, n=250, s=1, verbose=True)
    for pt in d:
        print pt

