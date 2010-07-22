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
    H.add_edges_from(edges)
    return nx.pagerank(H, alpha=alpha)
