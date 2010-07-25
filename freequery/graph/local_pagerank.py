"""
Pagerank functions
========================

Functions for computing Pagerank locally, instead of the
MapReduce approach of :mod:`freequery.graph.pagerank`.

Further reading
---------------

Notation from Langville, Amy N., and Meyer, Carl D., Google's PageRank and
Beyond: The Science of Search Engine Rankings. Princeton University
Press. 2006.

"""


def pagerank(edges, alpha=0.85):
    import networkx as nx
    H = nx.DiGraph()
    weights = dict()
    for e in edges:
        weights[e] = weights.get(e, 0.0) + 1
    for e,weight in weights.items():
        H.add_edge(e[0], e[1], weight=weight)
    return nx.pagerank(H, alpha=alpha)
