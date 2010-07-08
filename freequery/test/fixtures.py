from freequery.document import Document

example = Document('http://example.com', '<h1>Welcome to example</h1>')
apple = Document('http://apple.com', '<h1>Welcome to Apple</h1>')
stanford = Document('http://stanford.edu', '<h1>Stanford</h1>' \
                    '<p><a href="http://cs.stanford.edu">' \
                    'Stanford Computer Science</a></p>')
examplez = Document('http://example.com/z.html', '<h1>Example z</h1>')

all_docs = [example, apple, stanford]
for doc in all_docs:
    doc.make_typed('text/html')

qtable_file1 = """http://example.com
a:b=c
x:y=z

<h1>Welcome to example</h1>
@@@==-$$123456789-QTABLE-DELIMITER-12345679$$-==@@@
http://apple.com

<h1>Welcome to Apple</h1>"""

qtable_file2 = """http://example.com/m.html

<h1>Example m</h1>
@@@==-$$123456789-QTABLE-DELIMITER-12345679$$-==@@@
http://example.com/z.html

<h1>Example z</h1>"""
