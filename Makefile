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
	python setup.py sdist bdist_wheel
	twine check dist/*

clean:
	find . -type f -name *.pyc -delete
	find . -type d -name __pycache__ -delete