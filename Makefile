PYTHON=$(shell which python)
ifeq (, $PYTHON)
  $(error "PYTHON=$(PYTHON) not found in $(PATH)")
endif

PYTHON_VERSION_MIN=3.7
PYTHON_VERSION=$(shell $(PYTHON) -c 'import sys; print("%d.%d"% sys.version_info[0:2])' )
PYTHON_VERSION_OK=$(shell $(PYTHON) -c 'import sys;\
  print(int(float("%d.%d"% sys.version_info[0:2]) >= $(PYTHON_VERSION_MIN)))' )

ifeq ($(PYTHON_VERSION_OK),0)
  $(error "Need python $(PYTHON_VERSION) >= $(PYTHON_VERSION_MIN)")
endif

PYV=$(shell python3 -c "import sys;t='{v[0]}.{v[1]}'.format(v=list(sys.version_info[:2]));sys.stdout.write(t)");
PY=python -m py_compile
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
	@echo "    run pylint and mypy"
	@echo "make build"
	@echo "    build the installation package"
	@echo "make snapshot"
	@echo "    build a snapshot"

.PHONY: clean
clean:
	test -d dist && rm -rf dist/ || true
	test -d build && rm -rf build/ || true
	test -d adsa.egg-info && rm -rf adsa.egg-info || true
	find . -type d -name "__pycache__" -mindepth 1 -exec rm -rf {} \; -prune
	find . -type f -name "*.pyc" -exec rm {} \;

.PHONY: clean-all
clean-all:
	@+make clean
	test -d venv && rm -rf venv/ || true

prepare-dev: venv
	${PYTHON} -m pip install --upgrade pip setuptools wheel virtualenv py-make
	@+make venv

venv: $(VENV_NAME)/bin/activate
$(VENV_NAME)/bin/activate: setup.py
	test -d $(VENV_NAME) || virtualenv -p python3 $(VENV_NAME)
	${VPYTHON} -m pip install -r requirements.txt
	${VPYTHON} -m pip install -r requirements-dev.txt
	${VPYTHON} -m pip install -r requirements-extras.txt

dev-install: venv
	${VPYTHON} -m pip install -e .

.PHONY: snapshot-version
snapshot-version: adsa.egg-info/PKG-INFO
	grep "^Version:" adsa.egg-info/PKG-INFO | sed 's/^Version: //' > SNAPSHOT

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

.PHONY: lint
lint: venv
	$(VPYTHON) -m pytest --pycodestyle

.PHONY: codestyle
codestyle: venv
	$(VPYTHON) -m flake8
