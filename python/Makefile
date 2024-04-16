###############
# Build Tools #
###############
prebuild:
	# doesnt like symlinks
	cp ../LICENSE .
	cp ../README.md .

build: prebuild  ## build python/javascript
	python -m build .

develop: prebuild  ## install to site-packages in editable mode
	python -m pip install --upgrade build pip setuptools twine wheel
	python -m pip install -e .[develop]

install: prebuild  ## install to site-packages
	python -m pip install .

###########
# Testing #
###########
test: ## Clean and Make unit tests
	python -m pytest -v daggre/tests --junitxml=junit.xml --cov=daggre --cov-branch --cov-fail-under=75 --cov-report term-missing --cov-report xml

tests: test

###########
# Linting #
###########
lint:  ## Black/flake8 python
	python -m ruff check daggre setup.py
	python -m ruff check ../examples/*/*.py
	python -m isort daggre setup.py --check
	python -m isort ../examples/*/*.py --check


fix:  ## Black python
	python -m ruff format daggre setup.py
	python -m ruff format ../examples/*/*.py
	python -m isort daggre setup.py
	python -m isort ../examples/*/*.py

format: fix

#################
# Other Checks #
#################
check: checks

checks: annotate  ## run security, packaging, and other checks

annotate:  ## run mypy type annotation
	mypy daggre/

################
# Distribution #
################
dist: clean build  ## create dists
	python -m twine check dist/*

publish: dist  ## dist to pypi
	python -m twine upload dist/* --skip-existing

############
# Cleaning #
############
clean: ## clean the repository
	find . -name "__pycache__" | xargs  rm -rf
	find . -name "*.pyc" | xargs rm -rf
	find . -name ".ipynb_checkpoints" | xargs  rm -rf
	rm -rf .coverage coverage *.xml build dist *.egg-info lib node_modules .pytest_cache *.egg-info
	rm -rf daggre/labextension daggre/nbextension/static/index*
	git clean -fd

###########
# Helpers #
###########
# Thanks to Francoise at marmelab.com for this
.DEFAULT_GOAL := help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

print-%:
	@echo '$*=$($*)'

.PHONY: tests test lint fix format checks check check-manifest semgrep build develop install dist publish docs clean
