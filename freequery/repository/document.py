

class Document(object):

    """
    Represents a document and associated metadata.
    """

    def __init__(self, uri, data):
        self.uri = uri
        self.data = data

    def __eq__(self, other):
        return isinstance(other, Document) and self.__dict__ == other.__dict__
    
    def __str__(self):
        return "<Document uri='%s'>" % self.uri

