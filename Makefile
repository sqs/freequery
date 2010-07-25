.PHONY: clean install test

clean:
	find . -name '*~' -delete
	find . -name '*.pyc' -delete

install:
	aptitude install python-flup python-django erlang python-dev python-nose lighttpd python-networkx
	pip install PyStemmer

test:
	nosetests test/unit && \
	nosetests --processes=4 test/integration