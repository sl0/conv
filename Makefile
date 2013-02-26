FILES= Makefile README.txt conv.py gpl-3-0.txt

testing:
	#python -m doctest README.txt -v
	@nosetests -v --with-coverage  conv_tests.py


clean:
	@rm -rf *~ *.pyc .coverage

