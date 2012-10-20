FILES= Makefile README.txt conv.py gpl-3-0.txt

testing:
	python -m doctest README.txt -v

clean:
	@rm -f *~ *.pyc

