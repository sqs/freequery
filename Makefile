.PHONY: clean install test

clean:
	find . -name '*~' -delete
	find . -name '*.pyc' -delete

install:
	aptitude install -y python-pip python-flup python-django erlang python-dev python-nose lighttpd python-networkx
	pip install PyStemmer

test:
	disco restart > /dev/null && discodex restart > /dev/null && \
	nosetests test/unit && \
	nosetests -x --processes=4 test/integration

restart:
	disco restart && discodex restart