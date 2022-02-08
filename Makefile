PY=python -m py_compile

nothing:
	echo "Nothing done."

.PHONY:
	clean
	preinstall
	preinstalldev
	preinstallextras
	tests
	lint
	codestyle

clean:
	test -d dist && rm -rf dist/ || true
	test -d build && rm -rf build/ || true
	test -d adsa.egg-info && rm -rf adsa.egg-info || true
	find . -type d -name "__pycache__" -mindepth 1 -exec rm -rf {} \; -prune
	find . -type f -name "*.pyc" -exec rm {} \;

preinstall:
	$(PY) -m pip install -r requirements.txt

preinstalldev:
	@+make preinstall
	$(PY) -m pip install -r requirements-dev.txt

preinstallextras:
	@+make preinstall
	$(PY) -m pip install -r requirements-extras.txt

snapshot-version: adsa.egg-info/PKG-INFO
	grep "^Version:" adsa.egg-info/PKG-INFO | sed 's/^Version: //' > SNAPSHOT

snapshot:
	@+make preinstalldev
	$(PY) setup.py egg_info --tag-build=dev --tag-date sdist bdist_wheel bdist_egg && \
	@+make snapshot-version

snapshot-tag: SNAPSHOT
	git tag -a "v`cat SNAPSHOT`" -m "Snapshot v`cat SNAPSHOT`"

dist:
	@+make preinstaldev
	$(PY) setup.py sdist bdist_wheel bdist_egg

tests:
	@+make preinstalldev
	$(PY) -m pytest

lint:
	@+make preinstalldev
	$(PY) -m pytest --pycodestyle

codestyle:
	@+make preinstalldev
	$(PY) -m flake8
