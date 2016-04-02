from Data import KinshipContext
from Hypothesis import KinshipLexicon
from Primitives import *
####################################################################################
#   Word Sets
####################################################################################

genderless_english_words = ['parents', 'children', 'spouses', 'uncles/aunts', 'siblings', 'grandparents', 'cousins']
hawaiian_words = ['pat', 'mat', 'frat', 'sor']
eskimo_words = ['father', 'mother', 'brother', 'sister', 'uncle', 'aunt', 'cuz_m', 'cuz_f']
omaha_words = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
crow_words = omaha_words
sudanese_words = ['mother', 'father', 'brother', 'sister', 'f_bro', 'f_sis', 'm_bro', 'm_sis', 'fb_son', 'fb_dir', 'fs_son', 'fs_dir', 'mb_son', 'mb_dir', 'ms_son', 'ms_dir']
iroquois_words = ['frat', 'sor', 'sor_m', 'frat_s', 'in_bro', 'in_sis', 'out_bro', 'out_sis']
english_words = ['mother', 'father', 'brother', 'sister', 'uncle', 'aunt', 'grandma', 'grandpa', 'cousin']
turkish_words = ['anne', 'baba', 'abi', 'abla', 'amca', 'hala', 'dayi', 'teyze', 'yenge', 'eniste', 'kuzen', 'anneanne', 'babaanne', 'dede']
pukapuka_words = ['kainga', 'taina', 'matua-tane', 'matua-wawine', 'tapuna-tane', 'tapuna-wawine']

####################################################################################
#   Objects Sets
####################################################################################

four_gen_tree_objs = ['Amanda', 'Anne', 'aragorn', 'Arwen', 'Brandy', 'Celebrindal', 'Clarice', 'elrond', 'Eowyn', 'fabio', 'fred', 'frodo', 'Galadriel', 'gandalf', 'han', 'harry', 'Hermione', 'gary', 'james', 'joey', 'Katniss', 'legolas', 'Leia', 'Lily', 'luke', 'Luna', 'Mellissa', 'merry', 'Padme', 'peeta', 'Prue', 'ron', 'Rose', 'Sabrina', 'salem', 'sam', 'Zelda']
simple_tree_objs = ['Snow', 'charming', 'Emma', 'Mira', 'rump', 'Regina', 'henry', 'neal', 'baelfire', 'Maryann', 'ego']

####################################################################################
#   Contexts
####################################################################################

simple_tree_context = KinshipContext(simple_tree_objs,
                     [  ('spouse', 'Snow', 'charming'), ('spouse', 'charming', 'Snow'), ('parent', 'Snow', 'Emma'),
                        ('parent', 'charming', 'Emma'), ('parent', 'Snow', 'neal'), ('parent', 'charming','neal'),
                        ('spouse', 'Mira', 'rump'), ('spouse', 'rump', 'Mira'), ('parent', 'Mira', 'baelfire'),
                        ('parent', 'Mira', 'Regina'), ('parent', 'rump', 'baelfire'), ('parent', 'rump', 'Regina'),
                        ('spouse', 'baelfire', 'Emma'), ('spouse', 'Emma', 'baelfire'), ('parent', 'Emma', 'Maryann'),
                        ('parent', 'baelfire', 'Maryann'), ('parent', 'Emma', 'ego'), ('parent', 'baelfire', 'ego'), 
                        ('parent', 'Regina', 'henry')], ego='ego')

four_gen_tree_context = KinshipContext(four_gen_tree_objs,
                     [  ('parent', 'james', 'Luna'), ('parent', 'james', 'harry'), ('parent', 'Lily', 'Luna'),
                        ('parent', 'Lily', 'harry'), ('parent', 'harry', 'Mellissa'), ('parent', 'harry', 'salem'),
                        ('parent', 'harry', 'Sabrina'), ('parent', 'Hermione', 'Mellissa'), 
                        ('parent', 'Hermione', 'salem'), ('parent', 'Hermione', 'Sabrina'), 
                        ('parent', 'Mellissa', 'fabio'), ('parent', 'Mellissa', 'Clarice'), ('parent', 'joey', 'fabio'),
                        ('parent', 'joey', 'Clarice'), ('parent', 'salem', 'gary'), ('parent', 'salem', 'Amanda'),
                        ('parent', 'Zelda', 'gary'), ('parent', 'Zelda', 'Amanda'), ('parent', 'Sabrina', 'Katniss'),
                        ('parent', 'Sabrina', 'peeta'), ('parent', 'Sabrina', 'Prue'), ('parent', 'frodo', 'Katniss'), 
                        ('parent', 'frodo', 'peeta'), ('parent', 'frodo', 'Prue'), ('parent', 'fred', 'ron'),
                        ('parent', 'fred', 'Hermione'), ('parent', 'Anne', 'ron'), ('parent', 'Anne', 'Hermione'),
                        ('parent', 'gandalf', 'Eowyn'), ('parent', 'gandalf', 'aragorn'),
                        ('parent', 'Galadriel', 'Eowyn'), ('parent', 'Galadriel', 'aragorn'),
                        ('parent', 'aragorn', 'merry'), ('parent', 'aragorn', 'Leia'), ('parent', 'aragorn', 'frodo'),
                        ('parent', 'Arwen', 'merry'), ('parent', 'Arwen', 'Leia'), ('parent', 'Arwen', 'frodo'),
                        ('parent', 'merry', 'Rose'), ('parent', 'merry', 'sam'), ('parent', 'Brandy', 'Rose'),
                        ('parent', 'Brandy', 'sam'), ('parent', 'Leia', 'luke'), ('parent', 'Leia', 'Padme'),
                        ('parent', 'han', 'luke'), ('parent', 'han', 'Padme'), ('parent', 'elrond', 'legolas'),
                        ('parent', 'elrond', 'Arwen'), ('parent', 'Celebrindal', 'legolas'),
                        ('parent', 'Celebrindal', 'Arwen'), ('spouse', 'james', 'Lily'), ('spouse', 'Lily', 'james'),
                        ('spouse', 'harry', 'Hermione'), ('spouse', 'Hermione', 'harry'),
                        ('spouse', 'Mellissa', 'joey'), ('spouse', 'joey', 'Mellissa'), ('spouse', 'salem', 'Zelda'),
                        ('spouse', 'Zelda', 'salem'), ('spouse', 'Sabrina', 'frodo'), ('spouse', 'frodo', 'Sabrina'),
                        ('spouse', 'fred', 'Anne'), ('spouse', 'Anne', 'fred'), ('spouse', 'gandalf', 'Galadriel'),
                        ('spouse', 'Galadriel', 'gandalf'), ('spouse', 'aragorn', 'Arwen'),
                        ('spouse', 'Arwen', 'aragorn'), ('spouse', 'merry', 'Brandy'), ('spouse', 'Brandy', 'merry'),
                        ('spouse', 'Leia', 'han'), ('spouse', 'han', 'Leia'), ('spouse', 'elrond', 'Celebrindal'),
                        ('spouse', 'Celebrindal', 'elrond')])

####################################################################################
#   Target Lexicons
####################################################################################

# Genderless English Lexicon

target = KinshipLexicon(words=genderless_english_words)
target.force_function('siblings', lambda recurse_, C, X: setdifference_(children_of_(parents_of_(X, C), C), X))
target.force_function('spouses', lambda recurse_, C, X: spouses_of_(X, C))
target.force_function('parents', lambda recurse_, C, X: parents_of_(X, C))
target.force_function('children', lambda recurse_, C, X: children_of_(X, C))
target.force_function('uncles/aunts', lambda recurse_, C, X: union_(
    setdifference_(children_of_(parents_of_(parents_of_(X, C), C), C), parents_of_(X, C)),
    spouses_of_(setdifference_(children_of_(parents_of_(parents_of_(X, C), C), C), parents_of_(X, C)), C)))
target.force_function('grandparents', lambda recurse_, C, X: parents_of_(parents_of_(X, C), C))
target.force_function('cousins', lambda recurse_, C, X: children_of_(recurse_('siblings', C, parents_of_(X, C)), C))

uncle = KinshipLexicon(words=['uncle'])
uncle.force_function('uncle', lambda recurse_, C, X: male_(union_(
    setdifference_(children_of_(parents_of_(parents_of_(X, C), C), C), parents_of_(X, C)),
    spouses_of_(setdifference_(children_of_(parents_of_(parents_of_(X, C), C), C), parents_of_(X, C)), C))))

mother = KinshipLexicon(words=['mother'])
mother.force_function('mother', lambda recurse_, C, X: female_(parents_of_(X, C)))

brother = KinshipLexicon(words=['brother'])
brother.force_function('brother', lambda recurse_, C, X: male_(setdifference_(children_of_(parents_of_(X, C), C), X)))

grandma = KinshipLexicon(words=['grandma'])
grandma.force_function('grandma', lambda recurse_, C, X: female_(parents_of_(parents_of_(X, C), C)))

#   Hawaiian Lexicon

hawaiian = KinshipLexicon(words=hawaiian_words)
hawaiian.force_function('pat', lambda recurse_, C, X: male_(children_of_(parents_of_(parents_of_(X, C), C), C)))
hawaiian.force_function('mat', lambda recurse_, C, X: female_(children_of_(parents_of_(parents_of_(X, C), C), C)))
hawaiian.force_function('frat', lambda recurse_, C, X: male_(
    children_of_(children_of_(parents_of_(parents_of_(X, C), C), C), C)))
hawaiian.force_function('sor', lambda recurse_, C, X: female_(
    children_of_(children_of_(parents_of_(parents_of_(X, C), C), C), C)))

#   Pukapuka Lexicon

pukapuka = KinshipLexicon(words=pukapuka_words)
#Cross-sex my gen
pukapuka.force_function('kainga', lambda recurse_, C, X: if_(issubset_(X, male_(all_(C))),
                                    female_(children_of_(children_of_(parents_of_(parents_of_(X, C), C), C),C)),
                                    male_(children_of_(children_of_(parents_of_(parents_of_(X, C), C), C),C))))
#Same-sex my gen
pukapuka.force_function('taina', lambda recurse_, C, X: if_(issubset_(X, male_(all_(C))),
                                    male_(children_of_(children_of_(parents_of_(parents_of_(X, C), C), C), C)),
                                    female_(children_of_(children_of_(parents_of_(parents_of_(X, C), C), C), C))))
# Father-Uncle
pukapuka.force_function('matua-tane', lambda recurse_, C, X: male_(
    children_of_(parents_of_(parents_of_(X, C), C), C)))
# Mother-Aunt
pukapuka.force_function('matua-wawine', lambda recurse_, C, X: female_(
    children_of_(parents_of_(parents_of_(X, C), C), C)))
# Grandpa-GreatUncle
pukapuka.force_function('tupuna-tane', lambda recurse_, C, X: male_(
    children_of_(parents_of_(parents_of_(parents_of_(X, C), C), C), C)))
# Granma-GreatAunt
pukapuka.force_function('tupuna-wawine', lambda recurse_, C, X: female_(
    children_of_(parents_of_(parents_of_(parents_of_(X, C), C), C), C)))


#   Sudanese Lexicon

sudanese = KinshipLexicon(words=sudanese_words)
sudanese.force_function('mother', lambda recurse_, C, X: female_(parents_of_(X, C)))
sudanese.force_function('father', lambda recurse_, C, X: male_(parents_of_(X, C)))
sudanese.force_function('brother', lambda recurse_, C, X: setdifference_(X, male_(children_of_(parents_of_(X, C), C))))
sudanese.force_function('sister', lambda recurse_, C, X: setdifference_(X, female_(children_of_(parents_of_(X, C), C))))
sudanese.force_function('f_bro', lambda recurse_, C, X: recurse_('brother', C, recurse_('father', C, X)))
sudanese.force_function('f_sis', lambda recurse_, C, X: recurse_('sister', C, recurse_('father', C, X)))
sudanese.force_function('m_bro', lambda recurse_, C, X: recurse_('brother', C, recurse_('mother', C, X)))
sudanese.force_function('m_sis', lambda recurse_, C, X: recurse_('sister', C, recurse_('mother', C, X)))
sudanese.force_function('fb_son', lambda recurse_, C, X: male_(children_of_(recurse_('f_bro', C, X), C)))
sudanese.force_function('fb_dir', lambda recurse_, C, X: female_(children_of_(recurse_('f_bro', C, X), C)))
sudanese.force_function('fs_son', lambda recurse_, C, X: male_(children_of_(recurse_('f_sis', C, X), C)))
sudanese.force_function('fs_dir', lambda recurse_, C, X: female_(children_of_(recurse_('f_sis', C, X), C)))
sudanese.force_function('mb_son', lambda recurse_, C, X: male_(children_of_(recurse_('m_bro', C, X), C)))
sudanese.force_function('mb_dir', lambda recurse_, C, X: female_(children_of_(recurse_('m_bro', C, X), C)))
sudanese.force_function('ms_son', lambda recurse_, C, X: male_(children_of_(recurse_('m_sis', C, X), C)))
sudanese.force_function('ms_dir', lambda recurse_, C, X: female_(children_of_(recurse_('m_sis', C, X), C)))

# Turkish Lexicon
turkish = KinshipLexicon(words=turkish_words)
turkish.force_function('anne', lambda recurse_, C, X: female_(parents_of_(X, C)))
turkish.force_function('baba', lambda recurse_, C, X: male_(parents_of_(X, C)))
turkish.force_function('abi', lambda recurse_, C, X: setdifference_(X, male_(children_of_(parents_of_(X, C), C))))
turkish.force_function('abla', lambda recurse_, C, X: setdifference_(X, female_(children_of_(parents_of_(X, C), C))))
turkish.force_function('amca', lambda recurse_, C, X: recurse_('abi', C, recurse_('baba', C, X)))
turkish.force_function('hala', lambda recurse_, C, X: recurse_('abla', C, recurse_('baba', C, X)))
turkish.force_function('dayi', lambda recurse_, C, X: recurse_('abi', C, recurse_('anne', C, X)))
turkish.force_function('teyze', lambda recurse_, C, X: recurse_('abla', C, recurse_('anne', C, X)))
turkish.force_function('yenge', lambda recurse_, C, X: female_(spouses_of_(
    setdifference_(children_of_(parents_of_(parents_of_(X,C),C),C), parents_of_(X,C)), C)))
turkish.force_function('eniste', lambda recurse_, C, X: female_(spouses_of_(
    setdifference_(children_of_(parents_of_(parents_of_(X, C), C), C), parents_of_(X, C)), C)))
turkish.force_function('kuzen', lambda recurse_, C, X: children_of_(setdifference_(parents_of_(X, C),
                                                            children_of_(parents_of_(parents_of_(X, C), C), C)),C))
turkish.force_function('anneanne', lambda recurse_, C, X: female_(parents_of_(recurse_('anne', C, X), C)))
turkish.force_function('babaanne', lambda recurse_, C, X: female_(parents_of_(recurse_('baba', C, X), C)))
turkish.force_function('dede', lambda recurse_, C, X: male_(parents_of_(parents_of_(X, C), C)))

#   Eskimo Lexicon

eskimo = KinshipLexicon(words=eskimo_words)
eskimo.force_function('father', lambda recurse_, C, X: male_(parents_of_(X, C)))
eskimo.force_function('mother', lambda recurse_, C, X: female_(parents_of_(X, C)))
eskimo.force_function('brother', lambda recurse_, C, X: setdifference(X, male_(children_of_(parents_of_(X, C), C))))
eskimo.force_function('sister', lambda recurse_, C, X: setdifference(X, female_(children_of_(parents_of_(X, C), C))))
eskimo.force_function('uncle', lambda recurse_, C, X: male_(setdifference(parents_of_(X, C),
                                                                          children_of_(parents_of_(parents_of(X, C), C),
                                                                                       C))))
eskimo.force_function('aunt', lambda recurse_, C, X: female_(setdifference(parents_of_(X, C),
                                                                           children_of_(
                                                                               parents_of_(parents_of(X, C), C), C))))
eskimo.force_function('cuz_m', lambda recurse_, C, X: male_(children_of_(setdifference_(parents_of_(X, C),
                                                                                        children_of_(parents_of_(
                                                                                            parents_of_(X, C), C), C)),
                                                                         C)))
eskimo.force_function('cuz_f', lambda recurse_, C, X: female_(children_of_(setdifference_(parents_of_(X, C),
                                                                                          children_of_(parents_of_(
                                                                                              parents_of_(X, C), C),
                                                                                              C)), C)))

#   Iroquois Lexicon

iroquois = KinshipLexicon(words=iroquois_words)
iroquois.force_function('frat', lambda recurse_, C, X: male_(children_of_(parents_of_(male_(parents_of_(X, C)), C), C)))
iroquois.force_function('sor',
                        lambda recurse_, C, X: female_(children_of_(parents_of_(female_(parents_of_(X, C)), C), C)))
iroquois.force_function('sor_m', lambda recurse_, C, X: female_(
    setdifference_(children_of_(parents_of_(parents_of_(X, C), C), C),
                   union_(recurse_('frat', C, X), recurse_('sor', C, X)))))
iroquois.force_function('frat_s',
                        lambda recurse_, C, X: male_(setdifference_(children_of_(parents_of_(parents_of_(X, C), C), C),
                                                                    union_(recurse_('frat', C, X),
                                                                           recurse_('sor', C, X)))))
iroquois.force_function('in_bro', lambda recurse_, C, X: male_(setdifference_(X,
                                                                              children_of_(
                                                                                  union_(recurse_('frat', C, X),
                                                                                         recurse_('sor', C, X)), C))))
iroquois.force_function('in_sis', lambda recurse_, C, X: female_(setdifference_(X,
                                                                                children_of_(
                                                                                    union_(recurse_('frat', C, X),
                                                                                           recurse_('sor', C, X)), C))))
iroquois.force_function('out_bro', lambda recurse_, C, X: male_(children_of_(union_(recurse_('frat_s', C, X),
                                                                                    recurse_('sor_m', C, X)), C)))
iroquois.force_function('out_sis', lambda recurse_, C, X: female_(children_of_(union_(recurse_('frat_s', C, X),
                                                                                      recurse_('sor_m', C, X)), C)))

#   Omaha Lexicon

omaha = KinshipLexicon(words=omaha_words)
omaha.force_function('A', lambda recurse_, C, X: male_(children_of_(parents_of_(male_(parents_of_(X, C)), C), C)))
omaha.force_function('B', lambda recurse_, C, X: union_(
    female_(children_of_(parents_of_(female_(parents_of_(X, C)), C), C)),
    female_(children_of_(male_(children_of_(parents_of_(female_(parents_of_(X, C)), C), C)), C))))
omaha.force_function('C', lambda recurse_, C, X:
male_(children_of_(union_(
    female_(children_of_(parents_of_(female_(parents_of(X, C)), C), C)),
    recurse_('A', C, X)), C)))
omaha.force_function('D', lambda recurse_, C, X:
female_(children_of_(union_(
    female_(children_of_(parents_of_(female_(parents_of(X, C)), C), C)),
    recurse_('A', C, X)), C)))
omaha.force_function('E', lambda recurse_, C, X: female_(children_of_(parents_of_(male_(parents_of_(X, C)), C), C)))
omaha.force_function('F', lambda recurse_, C, X: union_(
    male_(children_of_(male_(children_of_(parents_of_(female_(parents_of_(X, C)), C), C)), C)),
    male_(children_of_(parents_of_(female_(parents_of_(X, C)), C), C))))
omaha.force_function('G', lambda recurse_, C, X: female_(children_of_(recurse_('E', C, X), C)))
omaha.force_function('H', lambda recurse_, C, X: male_(children_of_(recurse_('E', C, X), C)))


#   Crow Lexicon

crow = KinshipLexicon(words=crow_words)
crow.force_function('B', lambda recurse_, C, X: female_(children_of_(parents_of_(female_(parents_of_(X, C)), C), C)))
crow.force_function('A', lambda recurse_, C, X: union_(
    male_(children_of_(parents_of_(male_(parents_of_(X, C)), C), C)),
    male_(children_of_(female_(children_of_(parents_of_(male_(parents_of_(X, C)), C), C)), C))))
crow.force_function('C', lambda recurse_, C, X:
male_(children_of_(union_(
    male_(children_of_(parents_of_(male_(parents_of_(X, C)), C), C)),
    recurse_('B', C, X)), C)))
crow.force_function('D', lambda recurse_, C, X:
setdifference_(female_(children_of_(union_(
    male_(children_of_(parents_of_(male_(parents_of_(X, C)), C), C)),
    recurse_('B', C, X)), C)), X))
crow.force_function('F', lambda recurse_, C, X: male_(children_of_(parents_of_(female_(parents_of_(X, C)), C), C)))
crow.force_function('E', lambda recurse_, C, X: union_(
    female_(children_of_(female_(children_of_(parents_of_(male_(parents_of_(X, C)), C), C)), C)),
    female_(children_of_(parents_of_(male_(parents_of_(X, C)), C), C))))
crow.force_function('G', lambda recurse_, C, X: female_(children_of_(recurse_('F', C, X), C)))
crow.force_function('H', lambda recurse_, C, X: male_(children_of_(recurse_('F', C, X), C)))
