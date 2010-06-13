import Stemmer

english_stemmer = None

def load_stemmer():
    """Lazily load the stemmer."""
    global english_stemmer
    if english_stemmer is None:
        english_stemmer = Stemmer.Stemmer('english')

def stem_word(w):
    load_stemmer()
    return english_stemmer.stemWord(w)

def stem_words(ws):
    load_stemmer()
    return english_stemmer.stemWords(ws)

