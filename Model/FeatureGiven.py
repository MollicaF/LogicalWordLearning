from Data import KinshipContext
from Model.Hypothesis import KinshipLexicon
from Model.Primitives import *
from LOTlib.Evaluation.Eval import primitive

# Info1's Family Tree

Info1_obj = ['Info1', 'A1', 'a2', 'a3', 'A4', 'A5', 'a6', 'a7', 'a8', 'a9',
               'A10', 'A11', 'A12', 'a13', 'A14', 'a15', 'A16', 'A17', 'a18', 'A19', 'A20',
               'a21', 'a22', 'A23', 'a24', 'a25', 'a26', 'A27', 'A28', 'a29', 'A30']

FM_Info1 = [
    ['Info1', 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,
     1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0,
     0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1],
    ['A1', 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1,
     0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0,
     1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0],
    ['a2', 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0,
     1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
     1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1],
    ['a3', 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0,
     1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0,
     1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
    ['A4', 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0,
     0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0,
     0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    ['A5', 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0,
     1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1,
     0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
    ['a6', 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1,
     0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0],
    ['a7', 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1,
     1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0],
    ['a8', 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0,
     0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0],
    ['a9', 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0,
     0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0,
     0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0],
    ['A10', 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1,
     0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1],
    ['A11', 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0,
     0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    ['A12', 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1],
    ['a13', 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0,
     0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1],
    ['A14', 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0,
     0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0,
     0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
    ['a15', 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1,
     0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1,
     0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0],
    ['A16', 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0,
     0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0,
     0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    ['A17', 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0,
     1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0,
     0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    ['a18', 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0,
     0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0],
    ['A19', 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0,
     1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1,
     0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    ['A20', 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1,
     0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0,
     0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1],
    ['a21', 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    ['a22', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
     1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1],
    ['A23', 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0,
     1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1],
    ['a24', 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,
     0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1],
    ['a25', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0,
     0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0],
    ['a26', 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0,
     0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0],
    ['A27', 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0,
     0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0],
    ['A28', 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1],
    ['a29', 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
    ['A30', 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,
     1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1]]

distance2 = {'Info1': 1, 'A1': 2, 'a2': 3, 'a3': 4, 'A4': 5, 'A5': 6, 'a6': 7, 'a7': 8,
             'a8': 9, 'a9': 10, 'A10': 11, 'A11': 12, 'A12': 13, 'a13': 14, 'A14': 15, 'a15': 16,
             'A16': 17, 'A17': 18, 'a18': 19, 'A19': 20, 'A20': 21, 'a21': 22, 'a22': 23, 'A23': 24,
             'a24': 25, 'a25': 26, 'a26': 27, 'A27': 28, 'A28': 29, 'a29': 30, 'A30': 31}

Info1_tree_context = KinshipContext(Info1_obj,
                                      [('parent', 'a7', 'a29'),
                                       ('parent', 'A4', 'A1'),
                                       ('parent', 'A4', 'a9'),
                                       ('parent', 'A4', 'a8'),
                                       ('parent', 'a8', 'A10'),
                                       ('parent', 'a8', 'A11'),
                                       ('parent', 'a8', 'A12'),
                                       ('parent', 'A1', 'Info1'),
                                       ('parent', 'A1', 'a2'),
                                       ('parent', 'a3', 'Info1'),
                                       ('parent', 'a3', 'a2'),
                                       ('parent', 'A5', 'A17'),
                                       ('parent', 'A5', 'A16'),
                                       ('parent', 'A5', 'A27'),
                                       ('parent', 'A5', 'A14'),
                                       ('parent', 'A5', 'a3'),
                                       ('parent', 'a6', 'A17'),
                                       ('parent', 'a6', 'A16'),
                                       ('parent', 'a6', 'A27'),
                                       ('parent', 'a6', 'A14'),
                                       ('parent', 'a6', 'a3'),
                                       ('parent', 'a25', 'a26'),
                                       ('parent', 'A17', 'a26'),
                                       ('parent', 'a18', 'A19'),
                                       ('parent', 'a18', 'A20'),
                                       ('parent', 'A16', 'A19'),
                                       ('parent', 'A16', 'A20'),
                                       ('parent', 'a22', 'a24'),
                                       ('parent', 'A19', 'a24'),
                                       ('parent', 'A20', 'A23'),
                                       ('parent', 'a21', 'A23'),
                                       ('parent', 'a21', 'A28'),
                                       ('parent', 'a15', 'A30'),
                                       ('parent', 'A14', 'a13'),
                                       ('spouse', 'A4', 'a7'),
                                       ('spouse', 'a7', 'A4'),
                                       ('spouse', 'a6', 'A5'),
                                       ('spouse', 'A5', 'a6'),
                                       ('spouse', 'a25', 'A17'),
                                       ('spouse', 'A17', 'a25'),
                                       ('spouse', 'a18', 'A16'),
                                       ('spouse', 'A16', 'a18'),
                                       ('spouse', 'a22', 'A19'),
                                       ('spouse', 'A19', 'a22'),
                                       ('spouse', 'A20', 'a21'),
                                       ('spouse', 'a21', 'A20'),
                                       ('spouse', 'a15', 'A14'),
                                       ('spouse', 'A14', 'a15')], FM_Info1, distance=distance2, ego='Info1')


# Info2 Family Tree
Info2_obj = ['B1', 'b2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'b9', 'B10', 'B11',
              'b12', 'B13', 'B14', 'B15', 'b16', 'B17', 'b18', 'b19', 'b20', 'b21',
              'Info2', 'B22', 'B23']

FM_Info2 = [['B1', 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0],
             ['b2', 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1],
             ['B3', 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1],
             ['B4', 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
             ['B5', 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0],
             ['B6', 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0],
             ['B7', 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1],
             ['B8', 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1],
             ['b9', 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
             ['B10', 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0],
             ['B11', 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
             ['b12', 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1],
             ['B13', 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0],
             ['B14', 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0],
             ['B15', 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
             ['b16', 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
             ['B17', 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
             ['b18', 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             ['b19', 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
             ['b20', 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0],
             ['b21', 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
             ['Info2', 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1],
             ['B22', 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1],
             ['B23', 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1]]

distance = {'Info2': 1, 'B1': 2, 'b2': 3, 'B3': 4, 'B4': 5, 'B5': 6, 'B6': 7, 'B7': 8,
            'B8': 9, 'b9': 10, 'B10': 11, 'B11': 12, 'b12': 13, 'B13': 14, 'B14': 15, 'B15': 16,
            'b16': 17, 'B17': 18, 'b18': 19, 'b19': 20, 'b20': 21, 'b21': 22, 'B22':24, 'B23':23}

Info2_tree_context = KinshipContext(Info2_obj,
                                       [('parent', 'B5', 'B8'),
                                        ('parent', 'B5', 'B7'),
                                        ('parent', 'B1', 'B3'),
                                        ('parent', 'B1', 'Info2'),
                                        ('parent', 'B1', 'b2'),
                                        ('parent', 'B13', 'B15'),
                                        ('parent', 'B13', 'B14'),
                                        ('parent', 'b16', 'b18'),
                                        ('parent', 'b16', 'B17'),
                                        ('parent', 'B4', 'B5'),
                                        ('parent', 'B4', 'B1'),
                                        ('parent', 'B4', 'B13'),
                                        ('parent', 'B4', 'b16'),
                                        ('parent', 'b9', 'B3'),
                                        ('parent', 'b9', 'Info2'),
                                        ('parent', 'b9', 'b2'),
                                        ('parent', 'B10', 'B11'),
                                        ('parent', 'B10', 'b12'),
                                        ('parent', 'b19', 'B11'),
                                        ('parent', 'b19', 'b12'),
                                        ('parent', 'B6', 'b9'),
                                        ('parent', 'B6', 'B10'),
                                        ('parent', 'B22', 'B4'),
                                        ('parent', 'B22', 'B23'),
                                        ('parent', 'B23', 'b20'),
                                        ('spouse', 'B14', 'b21'),
                                        ('spouse', 'b21', 'B14'),
                                        ('spouse', 'b19', 'B10'),
                                        ('spouse', 'B10', 'b19')],FM_Info2, distance=distance, ego='Info2')

# Informant Three Family Tree

Info3_obj = ['info3', 'c1', 'C2', 'C3', 'c4', 'C5', 'c6', 'C7', 'c8', 'c9', 'c10', 'C11', 'c12']

FM_Info3 = [['info3',1,0,0,0,0,1,1,0,1,0,1,0,0,1,1,1,0,0,1,1,1,1,0,1,1,0,0,1,0,1,0,0,1,1,0,1,1,1,0,1,0,1,0,0,1,1,1,1,1,1,0,0,0,0,1,0,0,0,1,1,1,0,1,0,0,0,0,0,1,0,1,0,1,1,1,1,0,1,1,1,1,0,1,0,0,0,1,1,0,0,1,0],
            ['c1',0,1,1,0,0,0,1,1,1,0,1,0,0,1,1,1,0,1,1,1,1,0,1,0,1,0,0,1,0,0,1,0,1,1,1,0,1,1,0,1,1,0,0,1,1,0,1,1,0,1,0,0,0,0,1,1,1,0,1,1,0,0,1,0,1,1,1,0,1,1,0,0,1,1,1,1,0,1,1,1,0,0,1,0,0,0,1,1,0,1,1,0],
            ['C2',0,1,0,1,0,0,0,0,1,1,1,0,0,1,0,1,0,0,1,1,0,1,1,0,1,0,0,1,1,0,0,0,1,0,1,0,1,1,1,0,0,0,1,0,0,1,1,1,1,1,1,0,0,1,0,0,0,0,1,1,0,1,0,0,0,1,0,1,0,1,0,0,0,1,1,1,0,0,0,0,1,1,1,1,1,0,1,1,0,0,0,1],
            ['C3',1,0,1,0,0,0,1,0,0,1,1,0,0,0,1,1,1,0,0,1,1,1,0,0,1,1,0,0,0,1,0,0,1,1,0,1,1,0,1,1,0,1,0,1,1,0,1,1,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,1,0,0,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,0,0,0,0,0,0,1,0,0,0,1],
            ['c4',0,1,0,0,0,0,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,0,1,0,1,1,0,1,1,1,1,0,1,1,1,0,1,1,0,1,1,0,0,0,1,0,0,0,1,1,1,0,0,0,1,0,1,0,1,1,1,0,1,0,1,1,0,0,1,1,0,0,1,1,1,1,0,1,1,1,0,1,1,0,0,0,1,1,0,1,1,0],
            ['C5',0,1,1,0,1,0,1,0,1,0,0,0,0,0,0,0,0,1,1,0,0,0,1,0,1,1,0,0,0,0,0,0,0,0,1,0,1,1,0,0,1,0,0,0,1,1,0,1,0,1,1,1,1,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,1,1,1,1,1,1,1,1,0,1,0,1,0,0,0,0,0,0,0,1,1,0,0,1],
            ['c6',1,1,0,0,0,0,1,0,1,1,0,0,0,1,1,1,1,0,1,1,0,1,1,0,1,1,0,0,1,0,1,0,1,1,1,1,1,1,1,1,0,0,0,0,1,0,1,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1,1,1,0,0,0,1,1,1,0,1,0,1,1,0,0,0,0,0,1,0,1,0,1,0],
            ['C7',0,1,0,0,1,1,1,0,1,1,1,0,1,1,1,1,0,1,1,1,1,0,1,0,1,1,0,1,0,1,0,0,1,1,1,1,1,1,0,1,1,0,0,1,1,1,1,1,1,1,0,0,0,1,0,1,0,0,0,1,0,0,0,1,1,0,1,0,1,1,1,1,1,1,1,1,0,1,1,0,0,1,1,0,0,0,1,1,0,0,0,1],
            ['c8',0,0,1,0,0,1,1,0,1,0,0,1,0,0,1,1,0,0,1,1,1,1,0,0,0,0,0,0,1,1,1,0,1,0,0,0,1,1,1,0,0,1,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,1,1,0,1,0,0,0,1,1,1,0,1,1,1,1,0,0,0,1,0,0,1,0,0,1,0],
            ['c9',0,1,0,0,0,1,1,0,1,0,1,1,0,0,0,0,0,1,1,1,0,0,1,1,1,0,1,0,0,1,0,0,1,0,1,0,1,1,0,0,1,0,0,1,1,1,1,1,0,1,0,1,1,0,1,1,0,0,0,0,0,0,1,0,1,0,0,0,1,1,0,0,1,1,1,1,0,1,0,0,1,1,1,0,0,0,0,0,0,0,1,0],
            ['c10',1,0,0,1,0,1,1,1,1,0,1,1,0,0,1,0,0,1,0,1,0,0,0,0,1,0,1,0,1,1,0,1,1,1,0,1,1,1,0,1,1,0,0,1,1,1,1,1,0,1,0,1,1,0,1,1,0,0,0,0,1,0,1,0,0,0,0,0,1,0,0,0,1,0,1,1,0,1,1,0,1,1,0,0,0,0,0,0,1,0,1,0],
            ['C11',0,1,0,1,0,0,1,0,1,0,1,1,0,1,0,0,0,0,1,0,0,1,1,0,0,0,0,1,1,0,0,1,1,0,1,0,0,1,0,0,0,0,0,0,1,0,1,1,0,1,0,0,1,1,0,0,1,1,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,1,1,1,1,1,1,0,0,1,0,1,1,0,0,1],
            ['c12',1,1,0,0,1,0,1,0,1,1,1,0,0,1,1,1,1,1,1,1,0,0,1,0,1,1,0,0,0,1,1,0,1,1,1,1,1,1,0,1,1,0,1,0,1,0,1,1,0,1,1,0,0,0,0,0,1,0,0,1,0,0,0,0,1,1,0,0,1,1,0,0,1,1,1,1,0,1,1,1,1,0,1,0,0,0,1,1,0,0,1,0]]

distance3 = {'info3': 1, 'c1': 2, 'C2': 3, 'C3': 4, 'c4': 5, 'C5': 6, 'c6': 7, 'C7': 8, 'c8': 9, 'c9': 10, 'c10': 11,
             'C11': 12, 'c12': 13}

Info3_tree_context = KinshipContext(Info3_obj,
                                    [('parent', 'C2', 'info3'),
                                     ('parent', 'c1', 'info3'),
                                     ('parent', 'C2', 'C3'),
                                     ('parent', 'c1', 'C3'),
                                     ('parent', 'C7', 'c9'),
                                     ('parent', 'c8', 'c9'),
                                     ('parent', 'C7', 'c10'),
                                     ('parent', 'c8', 'c10'),
                                     ('parent', 'C11', 'c6'),
                                     ('parent', 'c12', 'c6'),
                                     ('parent', 'C11', 'C2'),
                                     ('parent', 'c12', 'C2'),
                                     ('parent', 'c4', 'c1'),
                                     ('parent', 'c4', 'C5'),
                                     ('parent', 'c4', 'C7'),
                                     ('spouse', 'C7', 'c8'),
                                     ('spouse', 'c8', 'C7'),
                                     ('spouse', 'c1', 'C2'),
                                     ('spouse', 'C2', 'c1'),
                                     ('spouse', 'c12', 'C11'),
                                     ('spouse', 'C11', 'c12')], FM_Info3, distance=distance3, ego='info3')


# Original Tree

original_obj = ['Amanda', 'Anne', 'aragorn', 'Arwen', 'Brandy', 'Celebrindal', 'Clarice', 'elrond', 'Eowyn', 'fabio',
                'fred', 'frodo', 'Galadriel', 'gandalf', 'han', 'harry', 'Hermione', 'gary', 'james', 'joey', 'Katniss',
                'legolas', 'Leia', 'Lily', 'luke', 'Luna', 'Mellissa', 'merry', 'Padme', 'peeta', 'Prue', 'ron', 'Rose',
                'Sabrina', 'salem', 'sam', 'Zelda']

# Skin, Hair, Facial, Height, Weight, Age, BRF, F0, HairLength
#  3	 6	 2	3	3      3    2 	 2      4
FM_original = [['Amanda', 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0],
               ['Anne', 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0],
               ['aragorn', 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0],
               ['Arwen', 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0],
               ['Brandy', 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
               ['Celebrindal', 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0],
               ['Clarice', 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0],
               ['elrond', 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0],
               ['Eowyn', 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0],
               ['fabio', 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0],
               ['fred', 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0],
               ['frodo', 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0],
               ['Galadriel', 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0],
               ['gandalf', 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0],
               ['han', 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0],
               ['harry', 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0],
               ['Hermione', 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0],
               ['gary', 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0],
               ['james', 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0],
               ['joey', 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0],
               ['Katniss', 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
               ['legolas', 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0],
               ['Leia', 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
               ['Lily', 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0],
               ['luke', 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0],
               ['Luna', 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0],
               ['Mellissa', 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0],
               ['merry', 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0],
               ['Padme', 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
               ['peeta', 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0],
               ['Prue', 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0],
               ['ron', 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0],
               ['Rose', 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0],
               ['Sabrina', 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0],
               ['salem', 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0],
               ['sam', 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0],
               ['Zelda', 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0]]

distance3 = {'Amanda': 6,
            'Anne': 33,
            'aragorn': 9,
            'Arwen': 14,
            'Brandy': 13,
            'Celebrindal': 37,
            'Clarice': 18,
            'elrond': 36,
            'Eowyn': 21,
            'fabio': 29,
            'fred': 32,
            'frodo': 4,
            'Galadriel': 35,
            'gandalf': 34,
            'han': 22,
            'harry': 15,
            'Hermione': 8,
            'gary': 17,
            'james': 30,
            'joey': 28,
            'Katniss': 2,
            'legolas': 26,
            'Leia': 25,
            'Lily': 31,
            'luke': 23,
            'Luna': 27,
            'Mellissa': 19,
            'merry': 10,
            'Padme': 24,
            'peeta': 1,
            'Prue': 5,
            'ron': 20,
            'Rose': 11,
            'Sabrina': 3,
            'salem': 16,
            'sam': 12,
            'Zelda': 7}

original_tree_context = KinshipContext(original_obj,
                                       [('parent', 'james', 'Luna'), ('parent', 'james', 'harry'),
                                        ('parent', 'Lily', 'Luna'),
                                        ('parent', 'Lily', 'harry'), ('parent', 'harry', 'Mellissa'),
                                        ('parent', 'harry', 'salem'),
                                        ('parent', 'harry', 'Sabrina'), ('parent', 'Hermione', 'Mellissa'),
                                        ('parent', 'Hermione', 'salem'), ('parent', 'Hermione', 'Sabrina'),
                                        ('parent', 'Mellissa', 'fabio'), ('parent', 'Mellissa', 'Clarice'),
                                        ('parent', 'joey', 'fabio'),
                                        ('parent', 'joey', 'Clarice'), ('parent', 'salem', 'gary'),
                                        ('parent', 'salem', 'Amanda'),
                                        ('parent', 'Zelda', 'gary'), ('parent', 'Zelda', 'Amanda'),
                                        ('parent', 'Sabrina', 'Katniss'),
                                        ('parent', 'Sabrina', 'peeta'), ('parent', 'Sabrina', 'Prue'),
                                        ('parent', 'frodo', 'Katniss'),
                                        ('parent', 'frodo', 'peeta'), ('parent', 'frodo', 'Prue'),
                                        ('parent', 'fred', 'ron'),
                                        ('parent', 'fred', 'Hermione'), ('parent', 'Anne', 'ron'),
                                        ('parent', 'Anne', 'Hermione'),
                                        ('parent', 'gandalf', 'Eowyn'), ('parent', 'gandalf', 'aragorn'),
                                        ('parent', 'Galadriel', 'Eowyn'), ('parent', 'Galadriel', 'aragorn'),
                                        ('parent', 'aragorn', 'merry'), ('parent', 'aragorn', 'Leia'),
                                        ('parent', 'aragorn', 'frodo'),
                                        ('parent', 'Arwen', 'merry'), ('parent', 'Arwen', 'Leia'),
                                        ('parent', 'Arwen', 'frodo'),
                                        ('parent', 'merry', 'Rose'), ('parent', 'merry', 'sam'),
                                        ('parent', 'Brandy', 'Rose'),
                                        ('parent', 'Brandy', 'sam'), ('parent', 'Leia', 'luke'),
                                        ('parent', 'Leia', 'Padme'),
                                        ('parent', 'han', 'luke'), ('parent', 'han', 'Padme'),
                                        ('parent', 'elrond', 'legolas'),
                                        ('parent', 'elrond', 'Arwen'), ('parent', 'Celebrindal', 'legolas'),
                                        ('parent', 'Celebrindal', 'Arwen'), ('spouse', 'james', 'Lily'),
                                        ('spouse', 'Lily', 'james'),
                                        ('spouse', 'harry', 'Hermione'), ('spouse', 'Hermione', 'harry'),
                                        ('spouse', 'Mellissa', 'joey'), ('spouse', 'joey', 'Mellissa'),
                                        ('spouse', 'salem', 'Zelda'),
                                        ('spouse', 'Zelda', 'salem'), ('spouse', 'Sabrina', 'frodo'),
                                        ('spouse', 'frodo', 'Sabrina'),
                                        ('spouse', 'fred', 'Anne'), ('spouse', 'Anne', 'fred'),
                                        ('spouse', 'gandalf', 'Galadriel'),
                                        ('spouse', 'Galadriel', 'gandalf'), ('spouse', 'aragorn', 'Arwen'),
                                        ('spouse', 'Arwen', 'aragorn'), ('spouse', 'merry', 'Brandy'),
                                        ('spouse', 'Brandy', 'merry'),
                                        ('spouse', 'Leia', 'han'), ('spouse', 'han', 'Leia'),
                                        ('spouse', 'elrond', 'Celebrindal'),
                                        ('spouse', 'Celebrindal', 'elrond')], FM_original, distance=distance3,
                                       ego='peeta')

the_context = Info3_tree_context

@primitive
def feature_(key, num, context):
    do = set()
    for person in context.features:
        if num == int(person[key]):
            do.add(person[0])
    return do


from LOTlib.Grammar import Grammar

char_grammar = Grammar()

char_grammar.add_rule('START', '', ['CHAR'], 1.0)

# SET THEORETIC
char_grammar.add_rule('CHAR', 'union_', ['CHAR', 'CHAR'], 1.0)
char_grammar.add_rule('CHAR', 'complement_', ['CHAR', 'C'], 1.0)
char_grammar.add_rule('CHAR', 'intersection_', ['CHAR', 'CHAR'], 1.0)
char_grammar.add_rule('CHAR', 'setdifference_', ['CHAR', 'CHAR'], 1.0)

char_grammar.add_rule('CHAR', 'feature_', ['KEY', 'NUM', 'C'], float(len(the_context.features[0])-1))

for f in xrange(len(the_context.features[0])-1):
    char_grammar.add_rule('KEY', str(f+1), None, 1.0)

char_grammar.add_rule('NUM', '1', None, 1.0)
char_grammar.add_rule('NUM', '0', None, 1.0)



# DEFINING GRAMMAR
def_grammar = Grammar()

def_grammar.add_rule('START', '', ['DEF'], 1.0)

# TREE
def_grammar.add_rule('DEF', 'parents_of_', ['DEF', 'C'], 1.0)
def_grammar.add_rule('DEF', 'children_of_', ['DEF', 'C'], 1.0)
def_grammar.add_rule('DEF', 'spouses_of_', ['DEF', 'C'], 1.0)

# SET THEORETIC
def_grammar.add_rule('DEF', 'union_', ['DEF', 'DEF'], 1.0)
def_grammar.add_rule('DEF', 'complement_', ['DEF', 'C'], 1.0)
def_grammar.add_rule('DEF', 'intersection_', ['DEF', 'DEF'], 1.0)
def_grammar.add_rule('DEF', 'setdifference_', ['DEF', 'DEF'], 1.0)

# GENDER
def_grammar.add_rule('DEF', 'female_', ['DEF'], 1.0)
def_grammar.add_rule('DEF', 'male_', ['DEF'], 1.0)

def_grammar.add_rule('DEF', 'X', None, 100.0)