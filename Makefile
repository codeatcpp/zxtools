.PHONY: init test clean coverage lint

test:
	python3 -m unittest discover -v -b

clean:
	rm -rf test/*.pyc
	rm -rf zxtools/*.pyc
	rm -rf test/__pycache__
	rm -rf zxtools/__pycache__
	rm -rf zxtools.egg-info
	rm -rf coverage.xml

coverage:
	coverage run --source zxtools setup.py test
	coverage report -m

lint:
	pylint zxtools -f parseable -r n
