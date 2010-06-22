

def doclinks(doc, params):
    """
    Emits a `(doc_uri, link_destination_uri)` tuple for each link in `doc`.
    """
    yield doc.uri, list(doc.link_uris())
    
