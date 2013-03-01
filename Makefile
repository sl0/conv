FILES= Makefile README.txt conv.py gpl-3-0.txt

testing:
	@more README.txt
	@echo "Now starting tests ..."
	@nosetests -v --with-coverage  conv_tests.py



clean:
	@rm -rf *~ *.pyc .coverage

