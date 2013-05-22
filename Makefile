FILES= Makefile README.txt LICENSE.txt iptables_converter.py iptables_converter_tests.py 

testing:
	@more README.txt
	@echo "Now starting tests ..."
	/usr/local/bin/tox
	#@nosetests -v --with-coverage  iptables_converter_tests.py



clean:
	@python setup.py clean --bdist-base build
	@rm -rf *~ *.pyc .coverage .tox build

