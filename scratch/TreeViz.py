from Model.Givens import english, turkish, pukapuka, four_gen_tree_context
import numpy as np

####################################################################################
# SVG FUNCTIONS
####################################################################################
class Path(object):
    def __init__(self, d='', attr={'stroke':'#000000', 'fill':'none'}, id=''):
        self.d = d
        self.id = id
        self.attributes = attr

    def compile(self):
        head = '<path d='
        ats = '\nstyle="'
        id = '\nid="' + self.id
        for k in self.attributes.keys():
            ats += k + ':' + self.attributes[k] + ';'
        foot = '/>'
        return '"'.join([head, self.d, ats, id, foot])


def woman(x, y, fill='none', stroke='#000000', ide=''):
    build = Path(attr={'fill': fill, 'stroke': stroke}, id=ide)
    rel1 = "c -1.222, -2.208, -2.718, -3.996, -4.218, -5.246c -1.75, 1.282, -3.882, 2.062, -6.206, 2.062c -2.328, 0, -4.462, -0.782, -6.21, -2.062c -1.5, 1.25, -2.996, 3.038, -4.222, 5.246c -2.844, 5.126, -3.156, 10.384, -0.7, 11.748c 1.1, 0.614, 2.254, 0.156, 3.446, -0.992c -0.21, 1.164, -0.332, 2.426, -0.332, 3.746c 0, 5.864, 2.278, 10.614, 5.086, 10.614c 1.692, 0, 2.53, -1.73, 2.932, -4.378c 0.402, 2.648, 1.24, 4.378, 2.926, 4.378c 2.812, 0, 5.09, -4.75, 5.09, -10.614c 0, -1.32, -0.122, -2.582, -0.336, -3.746c 1.196, 1.148, 2.348, 1.606, 3.45, 0.992 C"
    rel2 = "c 4.724, 0, 8.556, -3.832, 8.556, -8.558s, -3.832, -8.558, -8.556, -8.558,c -4.726, 0, -8.56, 3.832, -8.56, 8.558S"
    build.d = "M" + str(x) + ',' + str(y) + rel1 + str(3.162 + x) + ',' + str(10.384 + y) + ',' + str(2.844 + x) + ',' + str(5.126 + y) + ',' + str(x) + ',' + str(y) + "z M "+ str(x - 10.426) + ',' + str(y - 5.184) + rel2 + str(x - 15.152) + ',' + str(y - 5.19) + ',' + str(x - 10.426) + ','+ str(y - 5.184) +'z'
    return build

def man(x, y, fill='none', stroke='#000000', ide=''):
    build = Path(attr={'fill': fill, 'stroke': stroke}, id=ide)
    rel1 = "c -1.222, -2.208, -2.718, -3.996, -4.218, -5.246c -1.75, 1.282, -3.882, 2.062, -6.206, 2.062c -2.328, 0, -4.462, -0.782, -6.21, -2.062c -1.5, 1.25, -2.996, 3.038, -4.222, 5.246c -2.844, 5.126, -3.156, 10.384, -0.7, 11.748c 1.1, 0.614, 2.254, 0.156, 3.446, -0.992c -0.21, 1.164, -0.332, 2.426, -0.332, 3.746c 0, 5.864, 2.278, 10.614, 5.086, 10.614c 1.692, 0, 2.53, -1.73, 2.932, -4.378c 0.402, 2.648, 1.24, 4.378, 2.926, 4.378c 2.812, 0, 5.09, -4.75, 5.09, -10.614c 0, -1.32, -0.122, -2.582, -0.336, -3.746c 1.196, 1.148, 2.348, 1.606, 3.45, 0.992 C"
    rel2 = "c 4.724, 0, 8.556, -3.832, 8.556, -8.558s, -3.832, -8.558, -8.556, -8.558,c -4.726, 0, -8.56, 3.832, -8.56, 8.558S"
    rel3a = "c -1.25263,-0.857 -1.165126,-1.57 -3.071842,-0.857 -6.000867,0.435 -1.215967,0.406 -7.362043,-0.192 -2.652934,-0.982 -3.476467,6.411 -4.170964,6.984 -0.859266,0.711 -8.78406,0.04 -8.236533,4.966 0.123941,1.107 2.340895,0.859 6.834971,-0.804 4.933575,-1.829 9.084606,-1.713 15.144156,0.268 2.468825,0.806 7.507602,1.808 8.153982,1.593 1.597335,-0.532 -3.633937,-2.753 -5.210645,-3.36 -0.859531,-6.57 -0.864314,-7.328 -2.081082,-8.598 z"
    rel3 = "c -0.7515780,-0.5142000 -0.6990756,-0.9420000 -1.8431052,-0.5142000 -3.6005202,0.2610000 -0.7295802,0.2436000 -4.4172258,-0.1152000 -1.5917604,-0.5892000 -2.0858802,3.8466000 -2.5025784,4.1904000 -0.5155596,0.4266000 -5.2704360,0.0240000 -4.9419198,2.9796000 0.0743646,0.6642000 1.4045370,0.5154000 4.1009826,-0.4824000 2.9601450,-1.0974000 5.4507636,-1.0278000 9.0864936,0.1608000 1.4812950,0.4836000 4.5045612,1.0848000 4.8923892,0.9558000 0.9584010,-0.3192000 -2.1803622,-1.6518000 -3.1263870,-2.0160000 -0.5157186,-3.9420000 -0.5185884,-4.3968000 -1.2486492,-5.1588000 z"
    path1 = "M" + str(x) + ',' + str(y) + rel1 + str(3.162 + x) + ',' + str(10.384 + y) + ',' + str(2.844 + x) + ',' + str(5.126 + y) + ',' + str(x) + ',' + str(y) + "z M "+ str(x - 10.426) + ',' + str(y - 5.184) + rel2 + str(x - 15.152) + ',' + str(y - 5.19) + ',' + str(x - 10.426) + ','+ str(y - 5.184) +'z'
    path2 = " M" + str(x-5) +','+str(y-29) + rel3
    build.d = path1 + path2
    return build

def bow(x, y, fill='none', stroke='#000000', ide=''):
    build = Path(attr={'fill': fill, 'stroke': stroke}, id=ide)
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

    Amanda = woman(430, 410, color(p[0]), ide='Amanda')
    Anne = woman(550, 50, color(p[1]), ide='Anne')
    Aragorn = man(910, 170, color(p[2]), ide='aragorn')
    Arwen = woman(1030, 170, color(p[3]), ide='Arwen')
    Brandy = woman(1030, 290, color(p[4]), ide='Brandy')
    Celebrindal = woman(1150, 50, color(p[5]), ide='Celebrindal')
    Clarice = woman(190, 410, color(p[6]), ide='Clarice')
    Elrond = man(1030, 50, color(p[7]), ide='elrond')
    Eowyn = woman(790, 170, color(p[8]), ide='Eowyn')
    Fabio = man(70, 410, color(p[9]), ide='fabio')
    Fred = man(430, 50, color(p[10]), ide='fred')
    Frodo = man(730, 290, color(p[11]), ide='frodo')
    Galadriel = woman(910, 50, color(p[12]), ide='Galadriel')
    Gandalf = man(790, 50, color(p[13]), ide='gandalf')
    Han = man(1150, 290, color(p[14]), ide='han')
    Harry = man(310, 170, color(p[15]), ide='harry')
    Hermione = woman(430, 170, color(p[16]), ide='Hermione')
    Hilda = man(310, 410, color(p[17]), ide='gary') # might be gary ugh
    James = man(190, 50, color(p[18]), ide='james')
    Joey = man(70, 290, color(p[19]), ide='joey')
    Katniss = woman(550, 410, color(p[20]), ide='Katniss')
    Legolas = man(1150, 170, color(p[21]), ide='legolas')
    Leia = woman(1270, 290, color(p[22]), ide='Leia')
    Lily = woman(310, 50, color(p[23]), ide='Lily')
    Luke = man(1150, 410, color(p[24]), ide='luke')
    Luna = woman(190, 170, color(p[25]), ide='Luna')
    Mellissa = woman(190, 290, color(p[26]), ide='Mellissa')
    Merry = man(910, 290, color(p[27]), ide='merry')
    Padme = woman(1270, 410, color(p[28]), ide='Padme')
    Peeta = man(790, 410, color(p[29]), ide='peeta')
    Prue = woman(670, 410, fill='black', stroke='black', ide='Prue') #color(p[30]))
    Ron = man(550, 170, color(p[31]), ide='ron')
    Rose = woman(910, 410, color(p[32]), ide='Rose')
    Sabrina = woman(610, 290, color(p[33]), ide='Sabrina')
    Salem = man(310, 290, color(p[34]), ide='salem')
    Sam = man(1030, 410, color(p[35]), ide='sam')
    Zelda = woman(430, 290, color(p[36]), ide='Zelda')

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

if False:
    files = ['Reuse_aunt', 'Reuse_father', 'Reuse_cousin', 'Reuse_uncle', 'Reuse_grandma', 'Reuse_grandpa', 'Reuse_mother',
             'Reuse_sister','Simplicity_aunt', 'Simplicity_father', 'Simplicity_cousin', 'Simplicity_uncle',
             'Simplicity_grandma', 'Simplicity_grandpa', 'Simplicity_mother', 'Simplicity_sister']

    files = ['Simplicity_uncle']

    for fyle in files:
        probs = np.loadtxt('PaperFigs/' + fyle + '.csv', delimiter=',')
        for n, p in enumerate(probs):
            if n < 200:
                plot_fulltree(fyle+'_'+"%03d"%n, p, n)


if True:
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
