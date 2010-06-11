

class Repository(object):
    
    """
    Repository for storing documents and associated metadata.
    """
    
    def __init__(self, path):
        """
        Creates a new `Repository` at `path`.
        """
        self.path = path
