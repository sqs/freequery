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

def __pagerank(H, debug=False, alpha=0.85):
    """
    Computes and returns the stationary row vector of :math:`G`, which is also the
    eigenvector associated with eigenvalue 1. This vector contains the
    pageranks of the documents whose link structure is represented in
    :math:`H`.

    In Python terms, `H` is a 2-D list whose rows correspond to documents and
    with `H[i][j]=1/C(i)` if `C(i) > 0` and 0 otherwise.
    """
    # TODO(sqs): This does not work, but I'm leaving it in anyway for one
    # revision.
    import numpy
    from numpy import array, matrix, ones

    H = matrix(H)
    if debug: print "H = %r" % H
    
    n = H.shape[0]
    e = ones(n)
    E = (1.0/n) * (e * e.T)
    if debug: print "E = %r" % E

    a = array([int(not e) for e in H.any(axis=0).getA1()])
    if debug: print "a = %r" % a
    
    S = H + a * ((1.0/n) * e.T)
    if debug: print "S = %r" % S

    G = alpha*S + (1-alpha)*E
    if debug: print "G = %r" % G

    Gp = alpha*H + (alpha*a + (1-alpha)*e)*(1.0/n)*e.T
    if debug: print "Gp = %r" % Gp

    w, v = numpy.linalg.eig(G)
    piT = v[0].T
    if debug: print "w = %r" % w
    if debug: print "pi^T = %r" % piT

    return piT
    
    
