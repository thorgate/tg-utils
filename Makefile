.PHONY: help clean clean-build clean-pyc lint black test test-all test-full coverage docs

help:
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "test-all - run tests on every Python version with tox"
	@echo "test-full - shorthand for test lint coverage"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"

clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

lint:
	prospector

black:
	black tg_utils

test:
	pytest

test-all:
	tox

test-full: test lint coverage

coverage:
	pytest --cov-config .coveragerc --cov=tg_utils --cov-report html --cov-report term-missing

docs:
	mkdir -p docs/_static
	sphinx-apidoc -o docs/ tg_utils
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
