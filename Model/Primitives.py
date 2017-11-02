from LOTlib.Eval import primitive

@primitive
def parents_of_(x, context):
    if isinstance(x, set):
        do = set()
        for y in x:
            do.update(context.parents[y])
        return do
    else:
        return context.parents[x]

@primitive
def spouses_of_(x, context):
    if isinstance(x, set):
        do = set()
        for y in x:
            do.update(context.spouses[y])
        return do
    else:
        return context.spouses[x]

@primitive
def children_of_(x, context):
    if isinstance(x, set):
        do = set()
        for y in x:
            do.update(context.children[y])
        return do
    else:
        return context.children[x]

@primitive
def complement_(x, context):
    do = set()
    for y in context.objects:
        if y not in set(x):
            do.add(y)
    return do

@primitive
def all_(context):
    do = set()
    for y in context.objects:
        do.add(y)
    return do

@primitive
def ancestors(x, c):
    if len(parents_of_(x, c)) > 0:
        out = parents_of_(x, c)
        new = out
        while len(parents_of_(new, c)) > 0:
            out.update(parents_of_(new, c))
            out.update(children_of_(parents_of_(new, c), c))
            out.update(spouses_of_(children_of_(parents_of_(new, c), c), c))
            new = parents_of_(new, c)
    else:
        out = set()
    return out

@primitive
def descendants(x, c):
    if len(children_of_(x, c)) > 0:
        out = children_of_(x, c)
        out.update(spouses_of_(children_of_(x, c), c))
        new = out
        while len(children_of_(new, c)) > 0:
            out.update(children_of_(new, c))
            out.update(spouses_of_(children_of_(new, c), c))
            new = children_of_(new, c)
    else:
        out = set()
    return out

@primitive
def male_(x):
    do = set()
    for y in x:
        if y.islower():
            do.add(y)
    return do

@primitive
def female_(x):
    do = set()
    for y in x:
        if not y.islower():
            do.add(y)
    return do

@primitive
def samegender_(x, c):
    men = male_(all_(c))
    if len(x) != 1:
        return set()
    elif x.issubset(men):
        return men
    else:
        return female_(all_(c))

@primitive
def brothers_(X, C):
    return male_(setdifference_(children_of_(parents_of_(X, C), C), X))

@primitive
def sisters_(X, C):
    return female_(setdifference_(children_of_(parents_of_(X, C), C), X))

@primitive
def moms_(X, C):
    return female_(parents_of_(X, C))

@primitive
def dads_(X, C):
    return male_(parents_of_(X, C))

@primitive
def childz(X, C):
    return children_of_(X, C)

@primitive
def uncles_(X, C):
    return male_(union_(setdifference_(children_of_(parents_of_(parents_of_(X, C), C), C), parents_of_(X, C)),
                spouses_of_(setdifference_(children_of_(parents_of_(parents_of_(X, C), C), C), parents_of_(X, C)), C)))

@primitive
def aunts_(X, C):
    return female_(union_(setdifference_(children_of_(parents_of_(parents_of_(X, C), C), C), parents_of_(X, C)),
                spouses_of_(setdifference_(children_of_(parents_of_(parents_of_(X, C), C), C), parents_of_(X, C)), C)))

@primitive
def grandpas_(X, C):
    return male_(parents_of_(parents_of_(X, C), C))

@primitive
def grandmas_(X, C):
    return female_(parents_of_(parents_of_(X, C), C))

@primitive
def cousins_(X, C):
    return children_of_(union_(aunts_(X, C), uncles_(X, C)), C)

@primitive
def maternal_(X, C):
    return setdifference_(union_(union_(union_(union_(descendants(X, C), moms_(X, C)),
                       descendants(moms_(X, C), C)),
                       ancestors(moms_(X, C), C)), descendants(ancestors(moms_(X, C), C), C)), dads_(X, C))

@primitive
def paternal_(X, C):
    return setdifference_(union_(union_(union_(union_(descendants(X, C), dads_(X, C)),
                       descendants(dads_(X, C), C)),
                       ancestors(dads_(X, C), C)), descendants(ancestors(dads_(X, C), C), C)), moms_(X, C))

@primitive
def generation0_(X, C):
    if len(X) != 1:
        return set()
    return children_of_(children_of_(parents_of_(parents_of_(X, C), C), C), C)

@primitive
def generation1_(X, C):
    if len(X) != 1:
        return set()
    return union_(children_of_(parents_of_(parents_of_(X, C), C), C), spouses_of_(children_of_(parents_of_(parents_of_(X, C), C), C),C))

@primitive
def generation2_(X, C):
    if len(X) != 1:
        return set()
    return parents_of_(generation1_(X, C), C)

@primitive
def feature_(key, num, context):
    do = set()
    for person in context.features:
        if num == int(person[key]):
            do.add(person[0])
    return do
