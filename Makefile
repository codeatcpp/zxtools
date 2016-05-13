.PHONY: init test clean

test:
	python3 -m unittest discover -v

init:
	pip-3.2 install -r requirements.txt

clean:
	rm -rf test/*.pyc
	rm -rf zxtools/*.pyc
	rm -rf test/__pycache__
	rm -rf zxtools/__pycache__

coverage:
	coverage run --source zxtools setup.py test
	coverage report -m

lint:
	pylint zxtools -f parseable -r n
