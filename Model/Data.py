from collections import defaultdict
from LOTlib.Miscellaneous import flip, sample1, weighted_sample, self_update
from Model.Utilities import zipf

class KinshipData:
    def __init__(self, word, X, Y, context):
        self_update(self, locals())

    def __repr__(self):
        return 'KinshipData('+self.word + ',' + self.X + ',' + self.Y + ')'


class KinshipContext:
    def __init__(self, objects, relations, features=None, ego=None, distance=None):
        self_update(self, locals())
        self.__dict__.pop('relations')

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


def makeTreeLexiconData(lexicon, context, n=100, alpha=0.9, epsilon=0.9, verbose=False):
    '''

    L() --> {(W,S,R)}
    data ~ uniform( L() )

    :param lexicon: the target lexicon
    :param context: the context
    :param n: the number of data points
    :param alpha: the reliability parameter. Noise = 1 - alpha
    :param epsilon: the ego-centric probability.
    :param verbose: print the generated data points
    :return: list of KinshipData objects
    '''
    data = []
    tree_truth = lexicon.make_true_data(context)
    ego_truth  = lexicon.make_true_data(context, fixX=context.ego)
    for s in xrange(n):
        if flip(alpha):
            if flip(epsilon):
                t = sample1(ego_truth)
                if verbose:
                    print "True data:", s, t[0], t[1], t[2]
                data.append(KinshipData(t[0], t[1], t[2], context))
            else:
                t = sample1(tree_truth)
            if verbose:
                print "True data:", s, t[0], t[1], t[2]
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

# Log Childes Frequency of Kinship Terms: Summing counts across referential expression
engFreq = {'mother': 0.19, 'father': 0.16, 'grandpa': 0.10, 'grandma': 0.15, 'brother': 0.07, 'sister': 0.09,
           'uncle': 0.08, 'aunt': 0.09, 'cousin': 0.05}

def makeZipfianLexiconData(lexicon, context, dfreq=None, n=100, s=1.0, alpha=0.9, epsilon=0.8, verbose=False):
    '''

    L() --> P(W) [ eps P(S|W) P(R|W) + 1-eps P(S|W) P(R|SW)]
    P(W) ~ dfreq or defaults to uniform
    P(S|W)  ~ Zipf(s) domain: all speakers that can use that word
    P(R|W)  ~ Zipf(s) domain: all people the learner has a word for
    P(R|SW) ~ Zipf(s) domain: all referents the speaker can use the word to refer to

    :param lexicon: the target lexicon
    :param context: the context
    :param dfreq: dictionary[word] = frequency weight (float)
    :param n: the number of data points
    :param s: the zipfian exponent parameter
    :param alpha: the reliability parameter. Noise = 1 - alpha
    :param epsilon: the ego-centric probability
    :param verbose: print the generated data points
    :return: list of KinshipData objects
    '''
    assert context.distance is not None, "There are no distances in the context!"
    if dfreq is not None:
        assert set(lexicon.all_words()).issubset(set(dfreq.keys())), "Words in lexicon without frequencies"
        freq = lambda w: dfreq[w]
    else:
        freq = None
    data = []
    speakers = dict()
    egoRef   = dict()
    for w in lexicon.all_words():
        speakers[w] = [t[1] for t in lexicon.make_word_data(w, context)]
        egoRef[w] = [t[2] for t in lexicon.make_word_data(w, context, fixX=context.ego)]

    for i in xrange(n):
        if flip(alpha):
            wrd = weighted_sample(lexicon.all_words(), probs=freq)
            speaker = weighted_sample(speakers[wrd], probs=lambda x: zipf(x, s, context, len(context.objects)))
            if flip(epsilon):
                referent = weighted_sample(egoRef[wrd], probs=lambda x: zipf(x, s, context, len(context.objects)))
                eps = 'Ego'
            else:
                referent = weighted_sample(lexicon(wrd, context, set([speaker])),
                                           probs=lambda x: zipf(x, s, context, len(context.objects)))
                eps = 'Speaker'
            if verbose:
                print "True data:", i, wrd, speaker, referent, eps
            data.append(KinshipData(wrd, speaker, referent, context))
        else:
            wrd = weighted_sample(lexicon.all_words(), probs=freq)
            x = weighted_sample(context.objects, probs=lambda x: zipf(x, s, context, len(context.objects)))
            y = weighted_sample(context.objects, probs=lambda x: zipf(x, s, context, len(context.objects)))
            if verbose:
                print "Noise data:", i, wrd, x, y
            data.append(KinshipData(wrd, x, y, context))
    if verbose:
        print lexicon.compute_likelihood(data)
    return data


def makeUniformLexiconData(lexicon, context, n=1000, alpha=0.9, verbose=False):
    '''

    For w in words:
        L(w) --> {(W,S,R)}

    :param lexicon: the target lexicon
    :param context: the context
    :param n: the number of data points
    :param alpha: the reliability parameter. Noise = 1 - alpha
    :param verbose: print the generated data points
    :return: list of KinshipData objects
    '''
    output = []
    data = {w : [] for w in lexicon.all_words()}
    trueset = lexicon.make_true_data(context)
    for dp in trueset:
        data[dp[0]].extend([KinshipData(dp[0], dp[1], dp[2], context)])
    gos = int(n * alpha)
    for w in lexicon.all_words():
        for s in xrange(gos):
            output.append(sample1(data[w]))
            if verbose: print 'True Data:', s, output[-1].word, output[-1].X, output[-1].Y
        for s in xrange(n-gos):
            output.append(KinshipData(w, sample1(context.objects), sample1(context.objects), context))
            if verbose: print 'Noise Data:', s, output[-1].word, output[-1].X, output[-1].Y
    return output


def makeWordData(word, lexicon, context, n=1000, alpha=0.9, epsilon=0.5, verbose=False):
    '''

    L() --> {(W,S,R)}
    data ~ uniform( L() )

    :param lexicon: the target lexicon
    :param context: the context
    :param n: the number of data points
    :param alpha: the reliability parameter. Noise = 1 - alpha
    :param epsilon: the ego-centric probability.
    :param verbose: print the generated data points
    :return: list of KinshipData objects
    '''
    data = []
    tree_truth = lexicon.make_word_data(word, context)
    ego_truth  = lexicon.make_word_data(word, context, fixX=context.ego)
    for s in xrange(n):
        if flip(alpha):
            if flip(epsilon):
                t = sample1(ego_truth)
                if verbose:
                    print "True data:", s, t[0], t[1], t[2]
                data.append(KinshipData(t[0], t[1], t[2], context))
            else:
                t = sample1(tree_truth)
                if verbose:
                    print "True data:", s, t[0], t[1], t[2]
                data.append(KinshipData(t[0], t[1], t[2], context))
        else:
            x = sample1(context.objects)
            y = sample1(context.objects)
            if verbose:
                print "Noise data:", s, word, x, y
            data.append(KinshipData(word, x, y, context))
    if verbose:
        print lexicon.compute_likelihood(data)
    return data


if __name__ == "__main__":
    from Givens import english, four_gen_tree_context

    #makeUniformLexiconData(english,four_gen_tree_context, verbose=True)
    #makeTreeLexiconData(english,four_gen_tree_context,1000,epsilon=0.8,verbose=True)
    #makeZipfianLexiconData(english, four_gen_tree_context,engFreq,n=1000,s=1.0, verbose=True)
