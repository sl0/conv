FILES= Makefile README.txt LICENSE.txt iptables_converter.py iptables_converter_tests.py 

testing:
	@cat README.txt
	@echo "Now starting tests ..."
	/usr/local/bin/tox
	@#nosetests -v --with-coverage  iptables_converter_tests.py


rpm:
	python setup.py bdist_rpm

deb:
	gbp buildpackage

doc:
	(cd docs; make html )

clean:
	@python setup.py clean --bdist-base build
	@rm -rf *~ *.pyc .coverage build docs/build/*
	@rm -rf iptables_converter.egg-info
	@rm -rf dist __pycache__ *.py3
	@(cd docs; make clean)
	@dh_clean

