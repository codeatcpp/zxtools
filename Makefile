.PHONY: init test clean coverage lint

test:
	python3 -m unittest discover -v

#init:
#	pip install -r requirements.txt

clean:
	rm -rf test/*.pyc
	rm -rf zxtools/*.pyc
	rm -rf test/__pycache__
	rm -rf zxtools/__pycache__
	rm -rf zxtools.egg-info

coverage:
	coverage run --source zxtools setup.py test
	coverage report -m

lint:
	pylint zxtools -f parseable -r n
