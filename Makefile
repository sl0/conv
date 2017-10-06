FILES= Makefile README.txt LICENSE.txt iptables_converter.py iptables_converter_tests.py 


doc:
	$(MAKE) -C docs html

clean:
	@python setup.py clean --bdist-base build
	@rm -rf *~ *.pyc .pybuild/ .coverage build docs/build/* .tox
	@rm -rf iptables_converter.egg-info
	@rm -rf dist __pycache__ *.py3
	$(MAKE) -C docs clean
	@dh_clean

