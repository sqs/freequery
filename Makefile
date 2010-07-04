clean:
	find . -name '*~' -delete
	find . -name '*.pyc' -delete

install:
	aptitude install python-flup python-django erlang python-dev python-nose lighttpd 
	pip install PyStemmer
