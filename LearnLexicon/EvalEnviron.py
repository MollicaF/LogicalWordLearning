import pickle
import numpy as np
from Model import *
from Model.Givens import *
from Model.FeatureGiven import *
from scipy.special import beta
from optparse import OptionParser
from LOTlib.Inference.GrammarInference.Precompute import create_counts
from LOTlib.Miscellaneous import attrmem,Infinity
from LOTlib.Grammar import pack_string
from LOTlib.Hypotheses.Priors.LZutil.IntegerCodes import to_fibonacci as integer2bits # Use Mackay's Fibonacci code
from LOTlib.Hypotheses.Priors.LZutil.LZ2 import encode


#############################################################################################
#    Option Parser
#############################################################################################
parser = OptionParser()
parser.add_option("--read", dest="filename", type="string", help="Pickled results",
                  default="PKL/fsENG.pkl")
parser.add_option("--write", dest="out_path", type="string", help="Results csv",
                  default="results.csv")
parser.add_option("--recurse", dest='recurse', action='store_true', help='Should we allow recursion?', default=False)
parser.add_option("--grammar", dest='grammar', action='store_true', help='Use the default grammar?', default=False)
parser.add_option("--zipf", dest='zipf', action='store_true', help='Return distance instead of binary', default=False)
parser.add_option("--family", dest="family", type="string", help="Family", default='english')
parser.add_option("--context", dest='context', type='string', help="What is the context",
                  default='four_gen_tree_context')
parser.add_option("--data", dest="N", type="int", default=10000,
                  help="If > 0, recomputes the likelihood on a sample of data this size")
parser.add_option("--alpha", dest="alpha", type="float", default=0.90, help="Noise value")
parser.add_option("--epsilon", dest="epsilon", type="float", default=0.0, help="Ego-centricity")
parser.add_option("--s", dest="s", type="float", default=0., help="zipf parameter")
parser.add_option("--datafile", dest="datafile", type='str', default=None, help="Where is the data?")

(options, args) = parser.parse_args()

#############################################################################################
#    Functions and Things
#############################################################################################
target = eval(options.family)
the_context = eval(options.context)
ground_truth = target.make_true_data(the_context)

print "Loading the data"
with open(options.filename, 'r') as f:
    hyps = pickle.load(f)

print "Loaded %s hypotheses" % (len(hyps))


if options.recurse:
    grammar = makeGrammar(four_gen_tree_objs, nterms=['Tree', 'Set', 'Gender', 'Generation'],
                          recursive=True, words=target.all_words())
elif options.grammar:
    grammar = list(hyps)[0].value[list(hyps)[0].all_words()[0]].grammar
else:
    grammar = makeGrammar(four_gen_tree_objs, nterms=['Tree', 'Set', 'Gender', 'GenerationS', 'Taboo'])

if options.datafile is None:
    if options.family=='english':
        huge_data = makeZipfianLexiconData(target, the_context,
                                           dfreq=engFreq,
                                           n=options.N,
                                           alpha=options.alpha,
                                           s=options.s,
                                           epsilon=options.epsilon)
    else:
        huge_data = makeZipfianLexiconData(target, the_context,
                                           n=options.N,
                                           alpha=options.alpha,
                                           s=options.s,
                                           epsilon=options.epsilon)
else:
    with open(options.datafile, 'r') as f:
        huge_data = pickle.load(f)


def multdir(counts, alpha):
    n = np.sum(counts, axis=1)
    a0 = np.sum(alpha)
    numerator = np.log(n * beta(a0, n))
    denominator = [np.sum([np.log(x * beta(a, x)) for x, a in zip(c, alpha) if x > 0]) for c in counts]
    return numerator - denominator


def compute_reuse_prior(lex):
    counts = create_counts(grammar, [lex.value[w] for w in lex.all_words()])[0]
    prior = 0.0
    for k in counts.keys():
        c = np.sum(counts[k], axis=0)
        prior += multdir([c], np.ones(len(c))/float(len(c)))[0]

    return prior

def compute_recursive_prior(lex):
    s = ''
    for tree in [lex.value[w] for w in lex.all_words()]:
        if tree.value.count_subnodes() > getattr(tree, 'maxnodes', Infinity):
            return -Infinity

        s = s + tree.grammar.pack_ascii(tree.value)

    # 1+ since it must be positive
    bits = ''.join([ integer2bits(1+pack_string.index(x)) for x in s ])
    c = encode(bits, pretty=0)

    return -len(c)

def do_I_abstract(h):
    return int( 'X' in [x.name for x in h.value.subnodes()])


def do_I_recurse(h):
    return int( 'recurse_' in [x.name for x in h.value.subnodes()])


def do_I_reuse(lex):
    counts = create_counts(grammar, [lex.value[w] for w in lex.all_words()])[0]
    return bool([ 1 for x in counts.values() if np.any(x > 1)])


def assess_inv_hyp(hypothesis, target_lexicon, context):
    findings = []
    hypothesized_lexicon_data = hypothesis.make_true_data(context)
    for w in target_lexicon.all_words():
        data = [dp for dp in huge_data if dp.word == w]
        hypothesized_word_data = set()
        for dp in hypothesized_lexicon_data:
            if dp[0] == w:
                hypothesized_word_data.add(dp)
        true_word_data = set()
        for dp in ground_truth:
            if dp[0] == w:
                true_word_data.add(dp)
        correct_count = 0
        for dp in hypothesized_word_data:
            if dp in true_word_data:
                correct_count += 1
        findings.append([w,  # Word
                         hypothesis.value[w].compute_prior(),  # Hypothesis Prior
                         hypothesis.compute_likelihood(data, eval=True)/float(len(data)),  # Hypothesis Likelihood
                         hypothesis.compute_prior(),  # Lexicon Prior
                         compute_reuse_prior(hypothesis),  # Recursive Prior
                         hypothesis.point_ll,  # Lexicon Likelihood
                         correct_count,  # No. Correct Objects
                         len(hypothesized_word_data),  # No. Proposed Objects
                         len(true_word_data),  # No. True Objects
                         do_I_abstract(hypothesis.value[w]),  # Abstraction?
                         do_I_recurse(hypothesis.value[w]),  # Recursion?
                         '"' + str(h.value[w]) + '"'])  # Hypothesis
        print findings[-1]
    return findings

def cheap_assess_inv_hyp(hypothesis, target_lexicon, context):
    findings = []
    for w in target_lexicon.all_words():
        findings.append([w,  # Word
                         hypothesis.value[w].compute_prior(),  # Hypothesis Prior
                         hypothesis.compute_prior(),  # Lexicon Prior
                         compute_recursive_prior(hypothesis),  # Recursive Prior
                         do_I_abstract(hypothesis.value[w]),  # Abstraction?
                         do_I_reuse(hypothesis),
                         do_I_recurse(hypothesis.value[w]),  # Recursion?
                         '"' + str(h.value[w]) + '"', 'WORLD'] +
                        [int(o in hypothesis(w, context, set([ego]))) for ego in context.objects for o in context.objects if ego != o] +
                        ['EGO'] + [int(o in hypothesis(w, context, set([context.ego]))) for o in context.objects])  # Hypothesis
        print findings[-1]
    return findings


def full_assess_inv_hyp(hypothesis, target_lexicon, context):
    findings = []
    lex_prior = hypothesis.compute_prior()
    reuse_prior = compute_reuse_prior(hypothesis)
    recursive_prior = compute_recursive_prior(hypothesis)
    reuse_bool = do_I_reuse(hypothesis)
    for w in target_lexicon.all_words():
        findings.append([w,  # Word
                         hypothesis.value[w].compute_prior(),  # Hypothesis Prior
                         lex_prior,  # Lexicon Prior
                         reuse_prior,  # Reuse Prior
                         recursive_prior,  # Recursive Prior
                         do_I_abstract(hypothesis.value[w]),  # Abstraction?
                         reuse_bool,
                         do_I_recurse(hypothesis.value[w]),  # Recursion?
                         '"' + str(h.value[w]) + '"', 'WORLD'] +
                        [int(o in hypothesis(w, context, set([ego]))) for ego in context.objects for o in context.objects if ego != o])  # Hypothesis
        print findings[-1]
    return findings


def Zcheap_assess_inv_hyp(hypothesis, target_lexicon, context):
    findings = []
    for w in target_lexicon.all_words():
        findings.append([w,  # Word
                         hypothesis.value[w].compute_prior(),  # Hypothesis Prior
                         hypothesis.compute_prior(),  # Lexicon Prior
                         compute_recursive_prior(hypothesis),  # Recursive Prior
                         do_I_abstract(hypothesis.value[w]),  # Abstraction?
                         do_I_reuse(hypothesis),
                         do_I_recurse(hypothesis.value[w]),  # Recursion?
                         '"' + str(h.value[w]) + '"', 'WORLD'] +
                        [context.distance[o]*int(o in hypothesis(w, context, set([ego]))) for ego in context.objects for o in context.objects if ego != o] +
                        ['EGO'] + [context.distance[o]*int(o in hypothesis(w, context, set([context.ego]))) for o in context.objects])  # Hypothesis
        print findings[-1]
    return findings

#############################################################################################
#    Evaluation Loop
#############################################################################################
results = []
result_strings = []

for s, h0 in enumerate(hyps):
    h = KinshipLexicon(alpha=options.alpha, epsilon=options.epsilon, s=options.s)
    # sourceWord = h0.all_words()[0]
    for w in h0.all_words():
        h0.value[w].grammar = grammar
        # h.set_word(w, h0.value[sourceWord])
    # h.compute_likelihood(huge_data, eval=True)
    # h.point_ll = h.likelihood / len(huge_data)
    if options.zipf:
        for wrd in Zcheap_assess_inv_hyp(h, target, the_context):
            result = [s] + wrd
            result_strings.append(', '.join(str(i) for i in result))
            results.append(result)
    else:
        for wrd in full_assess_inv_hyp(h, target, the_context):
            result = [s] + wrd
            result_strings.append(', '.join(str(i) for i in result))
            results.append(result)


print "Writing csv file . . ."
with open(options.out_path, 'w') as f:
    f.write('\n'.join(result_strings))
