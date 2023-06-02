PYTHON=$(shell which python)
ifeq (, $PYTHON)
  $(error "PYTHON=$(PYTHON) not found in $(PATH)")
endif

PYTHON_VERSION_MIN=3.10
PYTHON_VERSION=$(shell $(PYTHON) -c 'import sys; print("%d.%d"% sys.version_info[0:2])' )
PYTHON_VERSION_OK=$(shell $(PYTHON) -c 'import sys;\
  print(int(float("%d.%d"% sys.version_info[0:2]) >= $(PYTHON_VERSION_MIN)))' )

ifeq ($(PYTHON_VERSION_OK),0)
  $(error "Need python $(PYTHON_VERSION) >= $(PYTHON_VERSION_MIN)")
endif

VENV_NAME?=venv
VENV_ACTIVATE=. $(VENV_NAME)/bin/activate
VPYTHON=${VENV_NAME}/bin/python3

.DEFAULT: help
help:
	@echo "make prepare-dev"
	@echo "    prepare development environment, use only once"
	@echo "make tests"
	@echo "    run tests"
	@echo "make lint"
	@echo "    run lint with pylint"
	@echo "make typechecks"
	@echo "    run type checking with mypy"
	@echo "make codestyle"
	@echo "    check code style with flake8"
	@echo "make dev-install"
	@echo "    install the current folder in develoment mode"
	@echo "make snapshot"
	@echo "    build a snapshot"
	@echo "make dist"
	@echo "    build a distribution package"


.PHONY: clean
clean:
	test -d dist && rm -rf dist/ || true
	test -d build && rm -rf build/ || true
	test -d adsa.egg-info && rm -rf adsa.egg-info || true
	test -d src/adsa.egg-info && rm -rf src/adsa.egg-info || true
	find . -type d -name "__pycache__" -mindepth 1 -exec rm -rf {} \; -prune
	find . -type f -name "*.pyc" -exec rm {} \;

.PHONY: clean-all
clean-all:
	@+make clean
	test -d venv && rm -rf venv/ || true

prepare-dev: venv
	${PYTHON} -m pip install --upgrade pip setuptools setuptools_scm virtualenv py-make build
	@+make venv

venv: $(VENV_NAME)/bin/activate
$(VENV_NAME)/bin/activate: setup.py
	test -d $(VENV_NAME) || virtualenv -p python3 $(VENV_NAME)
	${VPYTHON} -m pip install -r requirements.txt
	${VPYTHON} -m pip install -r requirements-extras.txt
	${VPYTHON} -m pip install -r requirements-tests.txt

dev-install: venv
	${VPYTHON} -m pip install --editable '.[tests,extras]'

.PHONY: snapshot-version
snapshot-version: src/adsa.egg-info/PKG-INFO
	grep "^Version:" src/adsa.egg-info/PKG-INFO | sed 's/^Version: //' > SNAPSHOT

.PHONY: snapshot
snapshot: venv
	@+make prepare-dev
	$(VPYTHON) setup.py egg_info --tag-build=dev --tag-date sdist bdist_wheel bdist_egg
	@+make snapshot-version

.PHONY: snapshot-tag
snapshot-tag: SNAPSHOT
	git tag -a "v`cat SNAPSHOT`" -m "Snapshot v`cat SNAPSHOT`"

.PHONY: dist
dist: venv
	$(VPYTHON) setup.py sdist bdist_wheel bdist_egg

.PHONY: tests
tests:
	$(VPYTHON) -m pytest

.PHONE: checks
checks:
	@+make lint
	@+make typechecks
	@+make codestyle

.PHONY: lint
lint:
	$(VPYTHON) -m pylint src

.PHONY: typechecks
typechecks:
	$(VPYTHON) -m mypy src

.PHONY: codestyle
codestyle:
	$(VPYTHON) -m flake8 src
