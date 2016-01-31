from LOTlib.Hypotheses.GrammarHypothesisVectorized import GrammarHypothesisVectorized
from LOTlib.GrammarRule import BVUseGrammarRule
from LOTlib.MCMCSummary.VectorSummary import *
from LOTlib.Inference.Samplers.MetropolisHastings import MHSampler
from LOTlib.DataAndObjects import FunctionData, HumanData
from Model.Grammar import makeGrammar
from Model.Data import KinshipData
from Model.Givens import simple_tree_context, simple_tree_objs
from LOTlib.Miscellaneous import logsumexp, log1mexp, gammaln, Infinity, attrmem, log
from optparse import OptionParser
from random import random, sample
from copy import copy

######################################################################################################
#   Option Parser
######################################################################################################
parser = OptionParser()
parser.add_option("--load", dest="LOAD_PATH", type="string", help="Where is the hypothesis space?",
                  default="Tooth/2dp_HypothesisSpace.pkl")
parser.add_option("--data", dest="DATA_PATH", type="string", help="Where is the data?",
                  default="human.data")

parser.add_option("--top", dest="TOP_COUNT", type="int", default=1000, help="Top number of hypotheses to store")
parser.add_option("--steps", dest="STEPS", type="int", default=100000, help="Number of samples to run")
parser.add_option("--skip", dest="SKIP", type="int", default=100, help="Proposals to thin by")

parser.add_option("--out", dest="OUT_PATH", type="string", help="Where to save results",
                  default="Results/GrammarInference")

(options, args) = parser.parse_args()
######################################################################################################

my_grammar = makeGrammar(simple_tree_objs, nterms=['Tree', 'Set', 'Gender', 'Generation', 'Ancestry', 'Paternity'])

class KinshipGrammarHyp(GrammarHypothesisVectorized):
    def init_H(self):
        self.H = [h.make_true_data(simple_tree_context, fixX='ego') for h in self.hypotheses]

    def init_C(self):
        self.C = np.zeros((len(self.hypotheses), len(self.rules)))
        rule_idxs = {str([r.name, r.nt, r.to]): i for i, r in enumerate(self.rules)}

        for j, h in enumerate(self.hypotheses):
            grammar_rules = [self.grammar.get_matching_rule(fn) for fn in
                             h.value['Word'].value.iterate_subnodes(self.grammar)]
            for rule in grammar_rules:
                try:
                    self.C[j, rule_idxs[str([rule.name, rule.nt, rule.to])]] += 1
                except Exception as e:
                    if isinstance(rule, BVUseGrammarRule):
                        pass
                    else:
                        print str(h)
                        raise e

    def init_L(self, d, d_index):
        """Initialize `self.L` dictionary."""
        self.L[d_index] = np.array([h.compute_likelihood(d.data.input) for h in self.hypotheses])

    def init_R(self, d, d_index):
        """Initialize `self.R` dictionary."""
        self.R[d_index] = np.zeros((len(self.hypotheses), d.q_n))

        for q, r, m in d.get_queries():
            self.R[d_index][:, m] = [int(('Word', 'ego', q.Y) in h_concept) for h_concept in self.H]

    def propose(self):
        """New value is sampled from a normal centered @ old values, w/ proposal as covariance."""
        if random() > 0.05:
            step = np.random.multivariate_normal(self.value, self.proposal)

            new_value = copy(self.value)
            for i in sample(self.proposal.nonzero()[0], self.propose_n):
                new_value[i] = step[i]

            c = self.__copy__(value=new_value)
            return c, 0.0
        else:
            new_temp = np.random.normal(self.likelihood_temperature, 0.1)

            c = self.__copy__(temp=new_temp)
            return c, 0.0

    def __copy__(self, value=None, temp=None):
        """Copy this GH; shallow copies of value & proposal so we don't have sampling issues."""

        c = type(self)(self.grammar, self.hypotheses)  # don't copy the cached matrices
        c.__dict__.update(self.__dict__)

        if value is None:
            value = copy.copy(self.value)
        c.set_value(value)

        if temp is not None:
            c.likelihood_temperature = temp

        return c


class KinshipVectorSummary(VectorSummary):
    def csv_initfiles(self, filename):
        """
        Initialize new csv files.

        """
        with open(filename + '_values_recent.csv', 'a') as w:
            writer = csv.writer(w)
            writer.writerow(['i', 'nt', 'name', 'to', 'p', 'temp'])
        with open(filename + '_bayes_recent.csv', 'a') as w:
            writer = csv.writer(w)
            writer.writerow(['i', 'Prior', 'Likelihood', 'Posterior Score', 'temp'])
        with open(filename + '_values_map.csv', 'a') as w:
            writer = csv.writer(w)
            writer.writerow(['i', 'nt', 'name', 'to', 'p', 'temp'])
        with open(filename + '_bayes_map.csv', 'a') as w:
            writer = csv.writer(w)
            writer.writerow(['i', 'Prior', 'Likelihood', 'Posterior Score', 'temp'])

    def csv_appendfiles(self, filename, data):
        """
        Append Bayes data to `_bayes` file, values to `_values` file, and MAP hypothesis human
        correlation data to `_data_MAP` file.

        """
        i = self.count
        gh_recent = self.samples[-1]
        gh_map = self.get_top_samples(1)[0]

        with open(filename + '_values_recent.csv', 'a') as w:
            writer = csv.writer(w)
            writer.writerows([[i, r.nt, r.name, str(r.to), gh_recent.value[j], gh_recent.likelihood_temperature]
                              for j, r in enumerate(gh_recent.rules)])
        with open(filename + '_bayes_recent.csv', 'a') as w:
            writer = csv.writer(w)
            if self.sample_count:
                writer.writerow([i, gh_recent.prior, gh_recent.likelihood, gh_recent.posterior_score,
                                 gh_recent.likelihood_temperature])
        with open(filename + '_values_map.csv', 'a') as w:
            writer = csv.writer(w)
            writer.writerows([[i, r.nt, r.name, str(r.to), gh_map.value[j], gh_recent.likelihood_temperature]
                              for j, r in enumerate(gh_map.rules)])
        with open(filename + '_bayes_map.csv', 'a') as w:
            writer = csv.writer(w)
            if self.sample_count:
                writer.writerow(
                    [i, gh_map.prior, gh_map.likelihood, gh_map.posterior_score, gh_recent.likelihood_temperature])


def run(data, load_hyps, grammar=my_grammar, iters=options.STEPS, skip=options.SKIP, cap=options.TOP_COUNT,
        print_stuff='gr', save_file='', pickle_summary=False):
    grammar_h0 = KinshipGrammarHyp(grammar, hypotheses=[], load=load_hyps, propose_step=.1, propose_n=1)
    mh_grammar_sampler = MHSampler(grammar_h0, data, iters)
    mh_grammar_summary = KinshipVectorSummary(skip=skip, cap=cap)

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
        quer = []
        resps = []
        entry = line.split(',')
        if i > 0:
            for j in xrange(3, len(entry)):
                if entry[j] not in ('NA', 'NA\n'):
                    dp = entry[j].strip('\n').split('_')
                    quer.append(KinshipData('Word', 'ego', dp[0], simple_tree_context))
                    resps.append((float(dp[1]), float(dp[2]) - float(dp[1])))
            inp = [KinshipData('Word', 'ego', entry[1], simple_tree_context),
                   KinshipData('Word', 'ego', entry[2], simple_tree_context)]
            my_data.append(HumanData(FunctionData(input=inp, output=[]), queries=quer, responses=resps))

run(my_data, load_hyps=options.LOAD_PATH, save_file=options.OUT_PATH, pickle_summary=False)
