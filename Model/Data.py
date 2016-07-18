from collections import defaultdict
from LOTlib.Miscellaneous import flip, sample1

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
    def __init__(self, objects, relations, ego=None):

        self.__dict__.update(locals())
        self.ego = ego
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


def makeLexiconData(lexicon, context, n=100, alpha=0.9, verbose=False):
    data = []
    if context.ego is None:
        tree_truth = lexicon.make_true_data(context)
    else:
        tree_truth = lexicon.make_true_data(context, fixX=context.ego)
    for s in xrange(n):
        if flip(alpha):
            t = sample1(tree_truth)
            if verbose:
                print "True data:", s, t
            data.append(KinshipData(t[0], t[1], t[2], context))
        else:
            x = sample1(context.objects)
            y = sample1(context.objects)
            word = sample1(lexicon.all_words())
            if verbose:
                print "Noise data:", s, word, x, y
            data.append(KinshipData(word, x, y, context))
    if verbose:
        print lexicon.compute_likelihood(data)
    return data


def makeRandomData(context, word='Word', n=3, ego=None, verbose=False):
    data = []
    for i in xrange(n):
        if isinstance(word, list):
            w = sample1(word)
        else:
            w = word
        if ego is not None:
            data.append(KinshipData(w, ego, sample1(context.objects), context))
            if verbose:
                print 'Data: ', i, data[-1]
        else:
            data.append(KinshipData(w, sample1(context.objects), sample1(context.objects), context))
            if verbose:
                print 'Data: ', i, data[-1]
    return data

def makeUniformData(lexicon, context, n=1000, alpha=0.9):
    output = []
    data = {w : [] for w in lexicon.all_words()}
    trueset = lexicon.make_true_data(context)
    for dp in trueset:
        data[dp[0]].extend([KinshipData(dp[0], dp[1], dp[2], context)])
    gos = int(n * alpha)
    for w in lexicon.all_words():
        for _ in xrange(gos):
            output.append(sample1(data[w]))
        for _ in xrange(n-gos):
            output.append(KinshipData(w, sample1(context.objects), sample1(context.objects), context))
    return output