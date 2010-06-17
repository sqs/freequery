from freequery.document import Document

example = Document('http://example.com', '<h1>Welcome to example</h1>')
apple = Document('http://apple.com', '<h1>Welcome to Apple</h1>')

all_docs = [example, apple]
for doc in all_docs:
    doc.make_typed('text/html')

