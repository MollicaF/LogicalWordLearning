from LOTlib.Grammar import Grammar
from LOTlib.Miscellaneous import q


def makeGrammar(objects,  nterms=['Tree', 'Set', 'Gender', 'Generation', 'Ancestry', 'Paternity', 'English'],
                terms=['X', 'objects', 'all'], recursive=False, words=None, compositional=True):
    """
    Define a grammar for tree relations
    """

    grammar = Grammar()

    grammar.add_rule('START', '', ['SET'], 1.0)

    if 'Tree' in nterms:
        # TREE
        grammar.add_rule('SET', 'parents_of_', ['SET', 'C'], 1.0)
        grammar.add_rule('SET', 'children_of_', ['SET', 'C'], 1.0)
        grammar.add_rule('SET', 'spouses_of_', ['SET', 'C'], 1.0)

    if 'Set' in nterms:
        # SET THEORETIC
        grammar.add_rule('SET', 'union_', ['SET', 'SET'], 1.0)
        grammar.add_rule('SET', 'complement_', ['SET', 'C'], 1.0)
        grammar.add_rule('SET', 'intersection_', ['SET', 'SET'], 1.0)
        grammar.add_rule('SET', 'setdifference_', ['SET', 'SET'], 1.0)

    if 'Gender' in nterms:
        # GENDER
        grammar.add_rule('SET', 'female_', ['SET'], 1.0 / 2)
        grammar.add_rule('SET', 'male_', ['SET'], 1.0 / 2)
        grammar.add_rule('SET', 'samegender_', ['SET', 'C'], 1.0)

    if 'Generation' in nterms:
        # GENERATION
        grammar.add_rule('SET', 'generation0_', ['SET', 'C'], 1.0/3)
        grammar.add_rule('SET', 'generation1_', ['SET', 'C'], 1.0/3)
        grammar.add_rule('SET', 'generation2_', ['SET', 'C'], 1.0/3)

    if 'Ancestry' in nterms:
        # CEST
        grammar.add_rule('SET', 'ancestors', ['SET', 'C'], 1.0)
        grammar.add_rule('SET', 'descendants', ['SET', 'C'], 1.0)

    if 'Paternity' in nterms:
        # TERNAL
        grammar.add_rule('SET', 'maternal_', ['SET', 'C'], 1.0)
        grammar.add_rule('SET', 'paternal_', ['SET', 'C'], 1.0)

    if 'English' in nterms:
        if compositional:
            lhs = 'SET'
        else:
            lhs = 'O'

        # ENGLISH
        grammar.add_rule('SET', 'brothers_', [lhs, 'C'], 1.0)
        grammar.add_rule('SET', 'sisters_', [lhs, 'C'], 1.0)
        grammar.add_rule('SET', 'moms_', [lhs, 'C'], 1.0)
        grammar.add_rule('SET', 'dads_', [lhs, 'C'], 1.0)
        grammar.add_rule('SET', 'children_', [lhs, 'C'], 1.0)
        grammar.add_rule('SET', 'uncles_', [lhs, 'C'], 1.0)
        grammar.add_rule('SET', 'aunts_', [lhs, 'C'], 1.0)
        grammar.add_rule('SET', 'grandpas_', [lhs, 'C'], 1.0)
        grammar.add_rule('SET', 'grandmas_', [lhs, 'C'], 1.0)
        grammar.add_rule('SET', 'cousins_', [lhs, 'C'], 1.0)

    if recursive and words is not None:
        for w in words:
            grammar.add_rule('SET', 'recurse_', [q(w), 'C', 'SET'], 1.0/len(words))

    if 'objects' in terms:
        if compositional:
            for o in objects:
                grammar.add_rule('SET', 'set', ["[\'%s\']" % o], 1.00/len(objects))
        else:
            for o in objects:
                grammar.add_rule('O', 'set', ["[\'%s\']" % o], 1.00/len(objects))

    if 'all' in terms:
        grammar.add_rule('SET', 'all_', ['C'], 1.0)

    if 'X' in terms:
        if compositional:
            grammar.add_rule('SET', 'X', None, 10.0) # Had to give high prob to make pcfg well-defined
        else:
            grammar.add_rule('O', 'X', None, 10.0) # Had to give high prob to make pcfg well-defined

    return grammar

def makeBiasedGrammar(objects, nterms=['Tree', 'Set', 'Gender', 'Generation', 'Ancestry', 'Paternity', 'English'],
                    terms=['X', 'objects', 'all'], recursive=False, words=None, compositional=True):


    """
    Define a grammar for tree relations
    """

    grammar = Grammar()

    grammar.add_rule('START', '', ['SET'], 1.0)

    if 'Tree' in nterms:
        # TREE
        grammar.add_rule('SET', 'parents_of_', ['SET', 'C'], 1.0)
        grammar.add_rule('SET', 'children_of_', ['SET', 'C'], 2.6118861522)
        grammar.add_rule('SET', 'spouses_of_', ['SET', 'C'], 46.1592503413)

    if 'Set' in nterms:
        # SET THEORETIC
        grammar.add_rule('SET', 'union_', ['SET', 'SET'], 82.6253980731)
        grammar.add_rule('SET', 'complement_', ['SET', 'C'], 4.134794019)
        grammar.add_rule('SET', 'intersection_', ['SET', 'SET'], 13.6030444971)
        grammar.add_rule('SET', 'setdifference_', ['SET', 'SET'], 12.1666763444)

    if 'Gender' in nterms:
        # GENDER
        grammar.add_rule('SET', 'female_', ['SET'], 209.5667590174)
        grammar.add_rule('SET', 'male_', ['SET'], 266.749332462)

    if 'Generation' in nterms:
        # GENERATION
        grammar.add_rule('SET', 'generation0_', ['SET', 'C'], 4.9008668098)
        grammar.add_rule('SET', 'generation1_', ['SET', 'C'], 1.3398224552)
        grammar.add_rule('SET', 'generation2_', ['SET', 'C'], 1.165400777)

    if 'Ancestry' in nterms:
        # CEST
        grammar.add_rule('SET', 'ancestors', ['SET', 'C'], 8.0872979353)
        grammar.add_rule('SET', 'descendants', ['SET', 'C'], 3.1124377558)

    if 'Paternity' in nterms:
        # TERNAL
        grammar.add_rule('SET', 'maternal_', ['SET', 'C'], 2.2192339232)
        grammar.add_rule('SET', 'paternal_', ['SET', 'C'], 1.3887916971)

    if 'English' in nterms:
        if compositional:
            lhs = 'SET'
        else:
            lhs = 'O'

        # ENGLISH
        grammar.add_rule('SET', 'brothers_', [lhs, 'C'], 1.0)
        grammar.add_rule('SET', 'sisters_', [lhs, 'C'], 1.0)
        grammar.add_rule('SET', 'moms_', [lhs, 'C'], 1.0)
        grammar.add_rule('SET', 'dads_', [lhs, 'C'], 1.0)
        grammar.add_rule('SET', 'children_', [lhs, 'C'], 1.0)
        grammar.add_rule('SET', 'uncles_', [lhs, 'C'], 1.0)
        grammar.add_rule('SET', 'aunts_', [lhs, 'C'], 1.0)
        grammar.add_rule('SET', 'grandpas_', [lhs, 'C'], 1.0)
        grammar.add_rule('SET', 'grandmas_', [lhs, 'C'], 1.0)
        grammar.add_rule('SET', 'cousins_', [lhs, 'C'], 1.0)

    if recursive and words is not None:
        for w in words:
            grammar.add_rule('SET', 'recurse_', [q(w), 'C', 'SET'], 1.0 / len(words))

    if 'objects' in terms:
        if compositional:
            for o in objects:
                grammar.add_rule('SET', 'set', ["[\'%s\']" % o], 123.5304511982 / len(objects))
        else:
            for o in objects:
                grammar.add_rule('O', 'set', ["[\'%s\']" % o], 123.5304511982 / len(objects))

    if 'all' in terms:
        grammar.add_rule('SET', 'all_', ['C'], 3.8903782136)

    if 'X' in terms:
        if compositional:
            grammar.add_rule('SET', 'X', None, 69.8908794494)  # Had to give high prob to make pcfg well-defined
        else:
            grammar.add_rule('O', 'X', None, 69.8908794494)  # Had to give high prob to make pcfg well-defined

    return grammar

if __name__ == "__main__":

    my_grammar = makeGrammar(['Mira','Snow','charming','rump','neal','baelfire','Emma','Regina','henry','Maryann','ego'],
                             compositional=False, terms=['X','objects'])

    for _ in xrange(10):
        print my_grammar.generate()
