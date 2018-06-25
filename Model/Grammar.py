from LOTlib.Grammar import Grammar
from LOTlib.Miscellaneous import q


def makeGrammar(objects,  nterms=['Tree', 'Set', 'Gender', 'Generation', 'Ancestry', 'Paternity', 'English'],
                terms=['X', 'objects', 'all'], recursive=False, words=None, compositional=True, abstractP=10.0):
    """
    Define a uniform PCFG for tree relations
        objects: a python list of strings for each person in the context
        nterms: a python list of primitive families
        terms: a python list of terminals
        recursive: BOOL for should grammar be recursive?
        words: a python list of words to recurse
        compositional: BOOL for if english primitives can be composed
        abstractP: float for non-uniform weight on abstraction, i.e. the speaker, X, primitive

    returns
        a LOTlib Grammar object
    """

    grammar = Grammar()

    grammar.add_rule('START', '', ['SET'], 1.0)

    if 'Tree' in nterms:
        grammar.add_rule('SET', 'parents_of_', ['SET', 'C'], 1.0)
        grammar.add_rule('SET', 'children_of_', ['SET', 'C'], 1.0)
        grammar.add_rule('SET', 'spouses_of_', ['SET', 'C'], 1.0)

    if 'Set' in nterms:
        grammar.add_rule('SET', 'union_', ['SET', 'SET'], 1.0)
        grammar.add_rule('SET', 'complement_', ['SET', 'C'], 1.0)
        grammar.add_rule('SET', 'intersection_', ['SET', 'SET'], 1.0)
        grammar.add_rule('SET', 'setdifference_', ['SET', 'SET'], 1.0)

    if 'Gender' in nterms:
        grammar.add_rule('SET', 'female_', ['SET'], 1.0)
        grammar.add_rule('SET', 'male_', ['SET'], 1.0)
        grammar.add_rule('SET', 'samegender_', ['SET', 'C'], 1.0)

    if 'Generation' in nterms:
        grammar.add_rule('SET', 'generation0_', ['SET', 'C'], 1.0)
        grammar.add_rule('SET', 'generation1_', ['SET', 'C'], 1.0)
        grammar.add_rule('SET', 'generation2_', ['SET', 'C'], 1.0)

    if 'Ancestry' in nterms:
        grammar.add_rule('SET', 'ancestors', ['SET', 'C'], 1.0)
        grammar.add_rule('SET', 'descendants', ['SET', 'C'], 1.0)

    if 'Paternity' in nterms:
        grammar.add_rule('SET', 'maternal_', ['SET', 'C'], 1.0)
        grammar.add_rule('SET', 'paternal_', ['SET', 'C'], 1.0)

    if 'English' in nterms:
        if compositional:
            lhs = 'SET'
        else:
            lhs = 'O'

        grammar.add_rule('SET', 'brothers_', [lhs, 'C'], 1.0)
        grammar.add_rule('SET', 'sisters_', [lhs, 'C'], 1.0)
        grammar.add_rule('SET', 'moms_', [lhs, 'C'], 1.0)
        grammar.add_rule('SET', 'dads_', [lhs, 'C'], 1.0)
        grammar.add_rule('SET', 'childz_', [lhs, 'C'], 1.0)
        grammar.add_rule('SET', 'uncles_', [lhs, 'C'], 1.0)
        grammar.add_rule('SET', 'aunts_', [lhs, 'C'], 1.0)
        grammar.add_rule('SET', 'grandpas_', [lhs, 'C'], 1.0)
        grammar.add_rule('SET', 'grandmas_', [lhs, 'C'], 1.0)
        grammar.add_rule('SET', 'cousins_', [lhs, 'C'], 1.0)

    if recursive and words is not None:
        for w in words:
            grammar.add_rule('SET', 'recurse_', [q(w), 'C', 'SET'], 1.0)

    if 'objects' in terms:
        if compositional:
            for o in objects:
                grammar.add_rule('SET', 'set', ["[\'%s\']" % o], abstractP/len(objects))
        else:
            for o in objects:
                grammar.add_rule('O', 'set', ["[\'%s\']" % o], abstractP/len(objects))

    if 'all' in terms:
        grammar.add_rule('SET', 'all_', ['C'], 1.0)

    if 'X' in terms:
        if compositional:
            grammar.add_rule('SET', 'X', None, 10.0) # Had to give high prob to make pcfg well-defined
        else:
            grammar.add_rule('O', 'X', None, 10.0) # Had to give high prob to make pcfg well-defined

    return grammar

def makeBiasedGrammar(objects, bias, nterms=['Tree', 'Set', 'Gender', 'Generation', 'Ancestry', 'Paternity', 'English'],
                    terms=['X', 'objects', 'all'], recursive=False, words=None, compositional=True):
    """
    Define a weighted PCFG for tree relations
        objects: a python list of strings for each person in the context
        bias: a python dictionary, bias[primitive] = weight (float)
        nterms: a python list of primitive families
        terms: a python list of terminals
        recursive: BOOL for should grammar be recursive?
        words: a python list of words to recurse
        compositional: BOOL for if english primitives can be composed

    returns
        a LOTlib Grammar object
    """

    grammar = Grammar()

    grammar.add_rule('START', '', ['SET'], 1.0)

    if 'Tree' in nterms:
        grammar.add_rule('SET', 'parents_of_', ['SET', 'C'], bias['parents_of_'])
        grammar.add_rule('SET', 'children_of_', ['SET', 'C'], bias['children_of_'])
        grammar.add_rule('SET', 'spouses_of_', ['SET', 'C'], bias['spouses_of_'])

    if 'Set' in nterms:
        grammar.add_rule('SET', 'union_', ['SET', 'SET'], bias['union_'])
        grammar.add_rule('SET', 'complement_', ['SET', 'C'], bias['complement_'])
        grammar.add_rule('SET', 'intersection_', ['SET', 'SET'], bias['intersection_'])
        grammar.add_rule('SET', 'setdifference_', ['SET', 'SET'], bias['setdifference_'])

    if 'Gender' in nterms:
        grammar.add_rule('SET', 'female_', ['SET'], bias['female_'])
        grammar.add_rule('SET', 'male_', ['SET'], bias['male_'])

    if 'Generation' in nterms:
        grammar.add_rule('SET', 'generation0_', ['SET', 'C'], bias['generation0_'])
        grammar.add_rule('SET', 'generation1_', ['SET', 'C'], bias['generation1_'])
        grammar.add_rule('SET', 'generation2_', ['SET', 'C'], bias['generation2_'])

    if 'Ancestry' in nterms:
        grammar.add_rule('SET', 'ancestors', ['SET', 'C'], bias['ancestors'])
        grammar.add_rule('SET', 'descendants', ['SET', 'C'], bias['descendants'])

    if 'Paternity' in nterms:
        grammar.add_rule('SET', 'maternal_', ['SET', 'C'], bias['maternal_'])
        grammar.add_rule('SET', 'paternal_', ['SET', 'C'], bias['paternal_'])

    if 'English' in nterms:
        if compositional:
            lhs = 'SET'
        else:
            lhs = 'O'

        grammar.add_rule('SET', 'brothers_', [lhs, 'C'], bias['brothers_'])
        grammar.add_rule('SET', 'sisters_', [lhs, 'C'], bias['sisters_'])
        grammar.add_rule('SET', 'moms_', [lhs, 'C'], bias['moms_'])
        grammar.add_rule('SET', 'dads_', [lhs, 'C'], bias['dads_'])
        grammar.add_rule('SET', 'childz_', [lhs, 'C'], bias['children_'])
        grammar.add_rule('SET', 'uncles_', [lhs, 'C'], bias['uncles_'])
        grammar.add_rule('SET', 'aunts_', [lhs, 'C'], bias['aunts_'])
        grammar.add_rule('SET', 'grandpas_', [lhs, 'C'], bias['grandpas_'])
        grammar.add_rule('SET', 'grandmas_', [lhs, 'C'], bias['grandmas_'])
        grammar.add_rule('SET', 'cousins_', [lhs, 'C'], bias['cousins_'])

    if recursive and words is not None:
        for w in words:
            grammar.add_rule('SET', 'recurse_', [q(w), 'C', 'SET'], bias['recurse_' + w])

    if 'objects' in terms:
        if compositional:
            for o in objects:
                grammar.add_rule('SET', 'set', ["[\'%s\']" % o], bias['terminal_' + o])
        else:
            for o in objects:
                grammar.add_rule('O', 'set', ["[\'%s\']" % o], bias['terminal_' + o])

    if 'all' in terms:
        grammar.add_rule('SET', 'all_', ['C'], bias['all_'])

    if 'X' in terms:
        if compositional:
            grammar.add_rule('SET', 'X', None, bias['terminal_X'])  # Had to give high prob to make pcfg well-defined
        else:
            grammar.add_rule('O', 'X', None, bias['terminal_X'])  # Had to give high prob to make pcfg well-defined

    return grammar

def makeCharGrammar(context):
    '''
    Defines a PCFG for characteristic hypotheses, specific to the context

        context: a Kinship context object

    returns
        a LOTlib Grammar object
    '''

    char_grammar = Grammar()

    char_grammar.add_rule('START', '', ['CHAR'], 1.0)

    char_grammar.add_rule('CHAR', 'union_', ['CHAR', 'CHAR'], 1.0)
    char_grammar.add_rule('CHAR', 'complement_', ['CHAR', 'C'], 1.0)
    char_grammar.add_rule('CHAR', 'intersection_', ['CHAR', 'CHAR'], 1.0)
    char_grammar.add_rule('CHAR', 'setdifference_', ['CHAR', 'CHAR'], 1.0)

    char_grammar.add_rule('CHAR', 'feature_', ['KEY', 'NUM', 'C'], float(len(context.features[0]) - 1))

    for f in xrange(len(context.features[0]) - 1):
        char_grammar.add_rule('KEY', str(f + 1), None, 1.0)

    char_grammar.add_rule('NUM', '1', None, 1.0)
    char_grammar.add_rule('NUM', '0', None, 1.0)

    return char_grammar


if __name__ == "__main__":

    uniform = makeGrammar(['Mira','Snow','charming','rump','neal','baelfire','Emma','Regina','henry','Maryann','ego'],
                             compositional=True, terms=['X','objects','all'], nterms=['Tree', 'Set', 'Gender'],
                             recursive=True, words=['mother','father','brother'])

    print uniform

