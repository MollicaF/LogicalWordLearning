"""
    Utilities for kinship
"""
import re
import numpy as np

def self_check(g):
    for e in g.keys():
        if e in g[e]:
            return True
    return False


def reachable(lexicon):
    g = dict()
    switch = False
    rec = re.compile("recurse_\('(.{1,12})', C")
    for e in lexicon.all_words():
        g[e] = rec.findall(str(lexicon.value[e]))
    if self_check(g):
        switch = True
    if len(strongly_connected_components(g)) < len(lexicon.all_words()):
        switch = True
    return switch


def strongly_connected_components(graph):
    """
    Tarjan's Algorithm (named for its discoverer, Robert Tarjan) is a graph theory algorithm
    for finding the strongly connected components of a graph.

    Based on: http://en.wikipedia.org/wiki/Tarjan%27s_strongly_connected_components_algorithm
    """

    index_counter = [0]
    stack = []
    lowlinks = {}
    index = {}
    result = []

    def strongconnect(node):
        # set the depth index for this node to the smallest unused index
        index[node] = index_counter[0]
        lowlinks[node] = index_counter[0]
        index_counter[0] += 1
        stack.append(node)

        # Consider successors of `node`
        try:
            successors = graph[node]
        except:
            successors = []
        for successor in successors:
            if successor not in lowlinks:
                # Successor has not yet been visited; recurse on it
                strongconnect(successor)
                lowlinks[node] = min(lowlinks[node],lowlinks[successor])
            elif successor in stack:
                # the successor is in the stack and hence in the current strongly connected component (SCC)
                lowlinks[node] = min(lowlinks[node],index[successor])

        # If `node` is a root node, pop the stack and generate an SCC
        if lowlinks[node] == index[node]:
            connected_component = []

            while True:
                successor = stack.pop()
                connected_component.append(successor)
                if successor == node: break
            component = tuple(connected_component)
            # storing the result
            result.append(component)

    for node in graph:
        if node not in lowlinks:
            strongconnect(node)

    return result


from fractions import Fraction

harmonic_number = lambda n, s: float(sum(Fraction(1, d) ** s for d in xrange(1, n + 1)))


def zipf(obj, s, C, N):
    margin = harmonic_number(N, s)
    return 1 / (C.distance[obj] ** s * margin)
