all: coverage

.PHONY: lint
lint:
	flake8

.PHONY: coverage
coverage:
	coverage run runtests.py
	coverage html

.PHONY: release
release:
	python3 setup.py bdist

clean:
	find . -type f -name *.pyc -delete
	find . -type d -name __pycache__ -delete