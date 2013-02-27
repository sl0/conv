FILES= Makefile README.txt conv.py gpl-3-0.txt

testing:
	@nosetests -v --with-coverage  conv_tests.py

t:
	python -m doctest README.txt -v


clean:
	@rm -rf *~ *.pyc .coverage

