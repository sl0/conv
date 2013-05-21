FILES= Makefile README.txt LICENSE.txt iptables_converter.py iptables_converter_tests.py 

testing:
	@more README.txt
	@echo "Now starting tests ..."
	@nosetests -v --with-coverage  iptables_converter_tests.py



clean:
	@rm -rf *~ *.pyc .coverage

