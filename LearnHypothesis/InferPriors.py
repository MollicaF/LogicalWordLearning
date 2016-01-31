from LOTlib.Hypotheses.GrammarHypothesis import GrammarHypothesis
from LOTlib.MCMCSummary.VectorSummary import *
from LOTlib.Inference.Samplers.MetropolisHastings import MHSampler
from LOTlib.DataAndObjects import FunctionData
from Model.Grammar import makeGrammar
from Model.Data import KinshipData
from Model.Givens import simple_tree_context, simple_tree_objs
from LOTlib.Miscellaneous import logsumexp, log1mexp, gammaln, Infinity, attrmem
from optparse import OptionParser

######################################################################################################
#   Option Parser
######################################################################################################
parser = OptionParser()
parser.add_option("--load", dest="LOAD_PATH", type="string", help="Where is the hypothesis space?",
                  default="Results/2dp_HypothesisSpace.pkl")
parser.add_option("--data", dest="DATA_PATH", type="string", help="Where is the data?",
                  default="human.data")

parser.add_option("--top", dest="TOP_COUNT", type="int", default=1000, help="Top number of hypotheses to store")
parser.add_option("--steps", dest="STEPS", type="int", default=100000, help="Number of samples to run")
parser.add_option("--skip", dest="SKIP", type="int", default=100, help="Proposals to thin by")

parser.add_option("--out", dest="OUT_PATH", type="string", help="Where to save results",
                  default="Results/GrammarInference")

(options, args) = parser.parse_args()
######################################################################################################

my_grammar = makeGrammar(simple_tree_objs)


class KinshipGrammarHyp(GrammarHypothesis):
    @attrmem('likelihood')
    def compute_likelihood(self, data, **kwargs):
        self.update()
        hypotheses = self.hypotheses
        likelihood = 0.0

        for d in data:
            posteriors = [h.compute_posterior(d.input)[0] + h.compute_posterior(d.input)[1] for h in hypotheses]
            zo = logsumexp(posteriors)
            weights = [(post - zo) for post in posteriors]

            for o in d.output.keys():
                # probability for yes on output `o` is sum of posteriors for hypos that contain `o`
                p = logsumexp(
                    [w if o.Y in h(o.word, o.context, set([o.Y])) else -Infinity for h, w in zip(hypotheses, weights)])
                p = -1e-10 if p >= 0 else p
                k = d.output[o][0]  # num. yes responses
                n = k + d.output[o][1]  # num. trials
                bc = gammaln(n + 1) - (gammaln(k + 1) + gammaln(n - k + 1))  # binomial coefficient
                likelihood += bc + (k * p) + (n - k) * log1mexp(p)  # likelihood we got human output

        return likelihood


def run(data, load_hyps, grammar=my_grammar, iters=options.STEPS, skip=options.SKIP, cap=options.TOP_COUNT,
        print_stuff='gr', save_file='', pickle_summary=False):
    grammar_h0 = KinshipGrammarHyp(grammar, hypotheses=[], load=load_hyps, propose_step=.1, propose_n=1)
    mh_grammar_sampler = MHSampler(grammar_h0, data, iters)
    mh_grammar_summary = VectorSummary(skip=skip, cap=cap)

    # Print all GrammarRules in grammar with corresponding value index
    if 'r' in print_stuff:
        print '=' * 100, '\nGrammarRules:'
        for idx, r in enumerate(grammar_h0.rules):
            print idx, '\t|  ', r

    # Initialize csv file
    if save_file:
        mh_grammar_summary.csv_initfiles(save_file)

    # Sample GrammarHypotheses!
    for i, gh in enumerate(mh_grammar_summary(mh_grammar_sampler)):

        if save_file and (i < iters and i % skip == 0):
            print '***********************', i, '***********************'
            mh_grammar_summary.csv_appendfiles(save_file, data)

    # Save summary & print top samples
    if pickle_summary:
        mh_grammar_summary.pickle_summary(filename=save_file + '_summary.p')
    if 'g' in print_stuff:
        mh_grammar_summary.print_top_samples()

##############################################################################################
#   Main
##############################################################################################

my_data = []
with open(options.DATA_PATH, 'r') as f:
    for i, line in enumerate(f.readlines()):
        output = dict()
        entry = line.split(',')
        if i > 0:
            for j in xrange(3, len(entry)):
                if entry[j] not in ('NA', 'NA\n'):
                    dp = entry[j].strip('\n').split('_')
                    output[KinshipData('Word', 'ego', dp[0] , simple_tree_context)] = (float(dp[1]), float(dp[2]))
            inp = [KinshipData('Word', 'ego', entry[1], simple_tree_context),
                     KinshipData('Word', 'ego', entry[2], simple_tree_context)]
            my_data.append(FunctionData(input=inp, output=output))

run(my_data, load_hyps=options.LOAD_PATH, save_file=options.OUT_PATH, pickle_summary=False)
