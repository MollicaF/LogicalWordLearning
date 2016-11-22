from collections import defaultdict
from LOTlib.Miscellaneous import flip, sample1, weighted_sample
from Model.Utilities import zipf

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


def makeZipfianLexiconData(lexicon, word, context, n=100, s=1.0, alpha=0.9, verbose=False): # TODO remove word param from Shift files
    data = []
    true_set = lexicon.make_true_data(context)
    all_poss_speakers = [ t[1] for t in true_set ]
    p = [ zipf(t, s, context, len(context.objects)) for t in all_poss_speakers ]

    for i in xrange(n):
        if flip(alpha):
            speaker = weighted_sample(all_poss_speakers, probs=p)

            bagR = {w : lexicon(w, context, set([speaker])) for w in lexicon.all_words()}
            uniqR = []
            for w in lexicon.all_words():
                uniqR.extend(bagR[w])

            p1 = [ zipf(t, s, context, len(context.objects)) for t in uniqR ]
            referent = weighted_sample(uniqR, probs=p1)

            word = sample1([w for w in lexicon.all_words() if referent in bagR[w]])

            if verbose:
                print "True data:", i, word, speaker, referent
            data.append(KinshipData(word, speaker, referent, context))
        else:
            word = sample1(lexicon.all_words())
            x = sample1(context.objects)
            y = sample1(context.objects)
            if verbose:
                print "Noise data:", i, word, x, y
            data.append(KinshipData(word, x, y, context))
    if verbose:
        print lexicon.compute_likelihood(data)
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