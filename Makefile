FILES= Makefile README.txt LICENSE.txt iptables_converter.py iptables_converter_tests.py 


doc:
	(cd docs; make html )

clean:
	@python setup.py clean --bdist-base build
	@rm -rf *~ *.pyc .coverage build docs/build/*
	@rm -rf iptables_converter.egg-info
	@rm -rf dist __pycache__ *.py3
	@(cd docs; make clean)
	@dh_clean

