.PHONY: clean clean-build clean-pyc clean-test coverage dist docs help install lint lint/flake8
.DEFAULT_GOAL := help

# This tries to grab the currently defined Python path based on the
# `PGT_VENV_PATH` environment variable. If not set, it will grab
# the current Python via pipenv.
get-venv:
ifdef PGT_VENV_PATH
	@echo "PGT_VENV_PATH is defined as $(PGT_VENV_PATH)"
else
	PGT_VENV_PATH := $(shell pipenv --py)
	@echo "PGT_VENV_PATH is not defined, defaulting to the current Python: $(PGT_VENV_PATH)"
endif

define BROWSER_PYSCRIPT
import os, webbrowser, sys

from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

lint/flake8: ## check style with flake8
	flake8 pygradethis tests

lint: lint/flake8 ## check style

test: ## run tests quickly with the default Python
	pytest

test-all: ## run tests on every Python version with tox
	tox

coverage: ## check code coverage quickly with the default Python
	coverage run --source pygradethis -m pytest
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/pygradethis.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ pygradethis
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

servedocs: docs ## compile the docs watching for changes
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

release: dist ## package and upload a release
	twine upload dist/*

dist: clean ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: clean ## install the package to the active Python's site-packages
	python setup.py install

install-dev: ## install the dev dependencies
	python -m pip install -e .[dev]

install-extras: ## install extra dependencies
	python -m pip install -e .[extras]

$(PGT_VENV_PATH)/bin/activate: get-venv setup.cfg 
	python3 -m venv $(PGT_VENV_PATH)
	source $(PGT_VENV_PATH)/bin/activate

# venv is a shortcut target
venv: $(PGT_VENV_PATH)/bin/activate ## activate a virtual environment in PGT_VENV_PATH

dev-install: get-venv ## install project locally with editable mode for development
	@echo "virtual env path: $(PGT_VENV_PATH)"
	$(PGT_VENV_PATH)/bin/pip install -e .
