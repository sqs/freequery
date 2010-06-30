

def doclinkdemux(doc, params):
    """
    Emits `(doc_uri, (link_destination_uri, ...))` for each link
    in `doc`.
    """
    for link_uri in set(doc.link_uris()):
        yield doc.uri, link_uri
