from Model.Givens import english, turkish, pukapuka, four_gen_tree_context
import numpy as np

####################################################################################
# SVG FUNCTIONS
####################################################################################
class Path(object):
    def __init__(self, d='', attr={'stroke':'#000000', 'fill':'none'}):
        self.d = d
        self.attributes = attr

    def compile(self):
        head = '<path d='
        ats = '\nstyle="'
        for k in self.attributes.keys():
            ats += k + ':' + self.attributes[k] + ';'
        foot = '/>'
        return '"'.join([head, self.d, ats, foot])


def man(x, y, fill='none', stroke='#000000'):
    build = Path(attr={'fill': fill, 'stroke': stroke})
    rel1 = "c -1.222, -2.208, -2.718, -3.996, -4.218, -5.246c -1.75, 1.282, -3.882, 2.062, -6.206, 2.062c -2.328, 0, -4.462, -0.782, -6.21, -2.062c -1.5, 1.25, -2.996, 3.038, -4.222, 5.246c -2.844, 5.126, -3.156, 10.384, -0.7, 11.748c 1.1, 0.614, 2.254, 0.156, 3.446, -0.992c -0.21, 1.164, -0.332, 2.426, -0.332, 3.746c 0, 5.864, 2.278, 10.614, 5.086, 10.614c 1.692, 0, 2.53, -1.73, 2.932, -4.378c 0.402, 2.648, 1.24, 4.378, 2.926, 4.378c 2.812, 0, 5.09, -4.75, 5.09, -10.614c 0, -1.32, -0.122, -2.582, -0.336, -3.746c 1.196, 1.148, 2.348, 1.606, 3.45, 0.992 C"
    rel2 = "c 4.724, 0, 8.556, -3.832, 8.556, -8.558s, -3.832, -8.558, -8.556, -8.558,c -4.726, 0, -8.56, 3.832, -8.56, 8.558S"
    build.d = "M" + str(x) + ',' + str(y) + rel1 + str(3.162 + x) + ',' + str(10.384 + y) + ',' + str(2.844 + x) + ',' + str(5.126 + y) + ',' + str(x) + ',' + str(y) + "z M "+ str(x - 10.426) + ',' + str(y - 5.184) + rel2 + str(x - 15.152) + ',' + str(y - 5.19) + ',' + str(x - 10.426) + ','+ str(y - 5.184) +'z'
    return build


def woman(x, y, fill='none', stroke='#000000'):
    build = Path(attr={'fill': fill, 'stroke': stroke})
    rel1 = "c -1.222, -2.208, -2.718, -3.996, -4.218, -5.246 c -1.75, 1.282, -3.882, 2.062, -6.208, 2.062 c -2.328, 0, -4.462, -0.782, -6.21, -2.062 c -1.5, 1.25, -2.996, 3.038, -4.222, 5.246 c -2.844, 5.126, -3.158, 10.384, -0.702, 11.748 c 1.1, 0.614, 2.254, 0.156, 3.446, -0.992 c -0.21, 1.164, -0.334, 2.426, -0.334, 3.746 c 0, 5.864, 2.278, 10.614, 5.086, 10.614 c 1.692, 0, 2.53, -1.73, 2.932, -4.378 c 0.402, 2.648, 1.24, 4.378, 2.928, 4.378 c 2.812, 0, 5.09, -4.75, 5.09, -10.614 c 0, -1.32, -0.122, -2.582, -0.336, -3.746 c 1.196, 1.148, 2.348, 1.606, 3.45, 0.992 C" + str(x + 3.164) + ',' + str(y + 10.384) + ',' + str(x + 2.846) + ',' + str(y + 5.126) + ',' + str(x) + ',' + str(y) + "z M"
    rel2 = "c 4.726, 0, 8.558, -3.832, 8.558, -8.558s -3.832, -8.558, -8.558, -8.558 c -4.726, 0, -8.56, 3.832, -8.56, 8.558 S "
    rel4 = "c 2.47, 0.91, 0.984, -1.45, 0.984, -3.062 s 1.524, -3.584, -0.984, -2.782 c -2.632, 0.844, -4.766, 1.308, -4.766, 2.922 S"
    rel6 = "c 1.564, 0, 0.69, -0.792, 0.69, -1.768 c 0, -0.976, 0.876, -1.766, -0.69, -1.766 s -0.748, 0.792, -0.748, 1.766, C"
    rel7 = "c 2.632, -0.968, 4.766, -1.308, 4.766, -2.922 S"
    rel8 = "c -2.508, -0.804, -0.984, 1.168, -0.984, 2.782 S" # 15.152
    path0 = "M" + str(x) + ',' + str(y) + rel1 + str(x - 10.426) + ',' + str(y - 5.184) + rel2 + str(x - 15.152) + ','
    path1 = str(y - 5.184) + ',' + str(x - 10.426) + ',' + str(y - 5.184) + "z M" + str(x - 4.58) + ',' + str(y - 22.75)
    path2 = rel4 + str(x - 7.212) + ',' + str(y - 23.72) + ',' + str(x - 4.58) + ',' + str(y - 22.75) + 'z M'
    path3 = str(x - 10.41) + ',' + str(y - 23.898) + rel6 + str(x - 11.158) + ',' + str(y - 24.688) + ','
    path4 = str(x - 11.974) + ',' + str(y - 23.898) + ',' + str(x - 10.41) + ',' + str(y - 23.898) + "z M"
    path5 = str(x - 16.274) + ',' + str(y - 22.75) + rel7 + str(x - 13.64) + ',' + str(y - 27.75) + ','
    path6 = str(x - 16.274) + ',' + str(y - 28.594) +rel8 + str(x - 18.746) + ',' + str(y - 21.842) + ','
    path7 = str(x - 16.274) + ',' + str(y - 22.75) + 'z'
    path = path0 + path1 + path2 + path3 + path4 + path5 + path6 + path7
    build.d = path
    return build


def compileSVG(paths, w=480, h=340,
                   header=None, text=None,
                   footer='</svg>'):
    if header is None:
        header0 = '<svg  xmlns="http://www.w3.org/2000/svg"\nxmlns:xlink="http://www.w3.org/1999/xlink"\n'
        header1 = 'viewBox="0 0 ' + str(w) + ' ' + str(h) + '"\n'
        header2 = 'width="' + str(w*2) + 'px"\n'
        header3 = 'height="' + str(h*2) + 'px">'
        header = header0 + header1 + header2 + header3

    out = [header]
    for p in paths:
        out.append(p.compile())

    if text is not None:
        out.append('<text x="20" y="115" font-family="sans-serif" font-size="40px" fill="black">'+text+'</text>')

    out.append(footer)
    return '\n'.join(out)

####################################################################################
# Probability Function
####################################################################################
def color(value, minimum=0, maximum=1):
    minimum, maximum = float(minimum), float(maximum)
    ratio = 2 * (value-minimum) / (maximum - minimum)
    b = int(max(0, 255*(1 - ratio)))
    r = int(max(0, 255*(ratio - 1)))
    g = 255 - b - r
    return '#%02x%02x%02x' % (r, g, b)

def color2(s):
    return 'white'

def plot_svg(filename, p):
    Snow = woman(70, 50, color(p[0]))
    charming = man(190, 50, color(p[1]))
    Emma = woman(190, 170, color(p[2]))
    Mira = woman(310, 50, color(p[3]))
    rump = man(430, 50, color(p[4]))
    henry = man(430, 290, color(p[5]))
    Regina = woman(430, 170, color(p[6]))
    neal = man(70, 170, color(p[7]))
    baelfire = man(310, 170, color(p[8]))
    Maryann = woman(190, 290, color(p[9]))
    ego = man(310, 290, fill='black', stroke='black')

    pa = Path(d="M 60,80 v 20, h 60, v 20, h -60, v 20")
    pf = Path(d="M 180,80 v 20, h -60, v 20, h 60, v 20")
    pb = Path(d="M 300,80 v 20, h 60, v 20, h -60, v 20")
    pg = Path(d="M 420,80 v 20, h -60, v 20, h 60, v 20")
    pc = Path(d="M 180,200 v 20, h 60, v 20, h -60, v 20")
    pi = Path(d="M 300,200 v 20, h -60, v 20, h 60, v 20")
    pd = Path(d="M 420,200 v 60")

    svg = compileSVG([charming, rump, neal, baelfire, ego, henry, Snow, Maryann, Mira, Emma, Regina, pa, pf, pb, pg, pc, pi, pd])

    with open('SVGs/' + filename + '.svg', 'w') as f:
        f.write(svg)


def plot_fulltree(fylename, p, n=None):

    Amanda = woman(430, 410, color(p[0]))
    Anne = woman(550, 50, color(p[1]))
    Aragorn = man(910, 170, color(p[2]))
    Arwen = woman(1030, 170, color(p[3]))
    Brandy = woman(1030, 290, color(p[4]))
    Celebrindal = woman(1150, 50, color(p[5]))
    Clarice = woman(190, 410, color(p[6]))
    Elrond = man(1030, 50, color(p[7]))
    Eowyn = woman(790, 170, color(p[8]))
    Fabio = man(70, 410, color(p[9]))
    Fred = man(430, 50, color(p[10]))
    Frodo = man(730, 290, color(p[11]))
    Galadriel = woman(910, 50, color(p[12]))
    Gandalf = man(790, 50, color(p[13]))
    Han = man(1150, 290, color(p[14]))
    Harry = man(310, 170, color(p[15]))
    Hermione = woman(430, 170, color(p[16]))
    Hilda = man(310, 410, color(p[17])) # might be gary ugh
    James = man(190, 50, color(p[18]))
    Joey = man(70, 290, color(p[19]))
    Katniss = woman(550, 410, color(p[20]))
    Legolas = man(1150, 170, color(p[21]))
    Leia = woman(1270, 290, color(p[22]))
    Lily = woman(310, 50, color(p[23]))
    Luke = man(1150, 410, color(p[24]))
    Luna = woman(190, 170, color(p[25]))
    Mellissa = woman(190, 290, color(p[26]))
    Merry = man(910, 290, color(p[27]))
    Padme = woman(1270, 410, color(p[28]))
    Peeta = man(790, 410, color(p[29]))
    Prue = woman(670, 410, fill='black', stroke='black') #color(p[30]))
    Ron = man(550, 170, color(p[31]))
    Rose = woman(910, 410, color(p[32]))
    Sabrina = woman(610, 290, color(p[33]))
    Salem = man(310, 290, color(p[34]))
    Sam = man(1030, 410, color(p[35]))
    Zelda = woman(430, 290, color(p[36]))

    gen0 = [Fabio, Clarice, Hilda, Amanda, Katniss, Prue, Peeta, Rose, Sam, Luke, Padme]
    gen1 = [Joey, Mellissa, Salem, Zelda, Sabrina, Frodo, Merry, Brandy, Han, Leia]
    gen2 = [Luna, Harry, Hermione, Ron, Eowyn, Aragorn, Arwen, Legolas]
    gen3 = [James, Lily, Fred, Anne, Gandalf, Galadriel, Elrond, Celebrindal]
    pa = Path(d="M 180,80 v 20, h 60, v 20, h -60, v 20")
    pf = Path(d="M 300,80 v 20, h -60, v 20, h 60, v 20")
    pb = Path(d="M 420,80 v 20, h 60, v 20, h -60, v 20")
    pg = Path(d="M 540,80 v 20, h -60, v 20, h 60, v 20")
    net1 = [pa, pf, pb, pg]
    pa2 = Path(d="M 780,80 v 20, h 60, v 20, h -60, v 20")
    pf2 = Path(d="M 900,80 v 20, h -60, v 20, h 60, v 20")
    pb2 = Path(d="M 1020,80 v 20, h 60, v 20, h -60, v 20")
    pg2 = Path(d="M 1140,80 v 20, h -60, v 20, h 60, v 20")
    net2 = [pa2, pf2, pb2, pg2]
    pa3 = Path(d="M 60,320 v 20, h 60, v 20, h -60, v 20")
    pf3 = Path(d="M 180,320 v 20, h -60, v 20, h 60, v 20")
    pb3 = Path(d="M 300,320 v 20, h 60, v 20, h -60, v 20")
    pg3 = Path(d="M 420,320 v 20, h -60, v 20, h 60, v 20")
    net3 = [pa3, pf3, pg3, pb3]
    pa4 = Path(d="M 900,320 v 20, h 60, v 20, h -60, v 20")
    pf4 = Path(d="M 1020,320 v 20, h -60, v 20, h 60, v 20")
    pb4 = Path(d="M 1140,320 v 20, h 60, v 20, h -60, v 20")
    pg4 = Path(d="M 1260,320 v 20, h -60, v 20, h 60, v 20")
    net4 = [pa4, pf4, pg4, pb4]
    pb5 = Path(d="M 300,200 v 20, h 60, v 20, h 240, v 20")
    pg5 = Path(d="M 420,200 v 20, h -60, v 20, h -180, v 20")
    pv5 = Path(d="M 300,240 v 20")
    pf5 = Path(d="M 1020,200 v 20, h -60, v 20, h -240, v 20")
    pe5 = Path(d="M 900,200 v 20, h 60, v 20, h 300, v 20")
    pw5 = Path(d="M 900,240 v 20")
    net5 = [pb5, pg5, pv5, pf5, pe5, pw5]
    pf6 = Path(d="M 720,320 v 20, h -60, v 20, h 120, v 20")
    pb6 = Path(d="M 600,320 v 20, h 60, v 20, h -120, v 20")
    pw6 = Path(d="M 660,360 v 20")
    net6 = [pf6, pb6, pw6]
    path = gen0 + gen1 + gen2 + gen3 + net1 + net2 + net3 + net4 + net5 + net6
    if n is not None:
        svg = compileSVG(path, w=1320, h=510, text="N:" + "%03d"%n)
    else:
        svg = compileSVG(path, w=1320, h=510)
    with open('PaperFigs/SVGs/' + fylename + '.svg', 'w') as f:
        f.write(svg)

if True:
    files = ['Reuse_aunt', 'Reuse_father', 'Reuse_cousin', 'Reuse_uncle', 'Reuse_grandma', 'Reuse_grandpa', 'Reuse_mother',
             'Reuse_sister','Simplicity_aunt', 'Simplicity_father', 'Simplicity_cousin', 'Simplicity_uncle',
             'Simplicity_grandma', 'Simplicity_grandpa', 'Simplicity_mother', 'Simplicity_sister']

    files = ['Simplicity_uncle']

    for fyle in files:
        probs = np.loadtxt('PaperFigs/' + fyle + '.csv', delimiter=',')
        for n, p in enumerate(probs):
            if n < 200:
                plot_fulltree(fyle+'_'+"%03d"%n, p, n)


if False:
    probs = [float(o in ['']) for o in four_gen_tree_context.objects]
    print probs
    plot_fulltree('Context',probs,0)

if False:
    target_p = ['white' for o in four_gen_tree_context.objects]
    target = english

    col = ['darkred', 'goldenrod', 'lightgreen', 'blue', 'green', 'yellow', 'orange', 'orchid', 'seagreen', 'skyblue', 'fuchsia', 'chocolate', 'moccasin', 'silver']
    colors = {w: col[i] for i,w in enumerate(target.all_words())}

    for wi, w in enumerate(target.all_words()):
        for oi, o in enumerate(four_gen_tree_context.objects):
            if o in target.value[w](target, four_gen_tree_context, set(['Prue'])):
                target_p[oi] = colors[w]

    print target_p
    plot_fulltree('AA_English_', target_p)
