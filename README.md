# Droplet shape solver

Simple Young-Laplace equation solver for small droplets

## Installation

This package is currently targeting Python version 3.10 and above.

If you just want to install the latest verions, run the following pip install command:

    pip install git+https://github.com/juusokorhonen/droplet-shape-solver/@main

## Developer installation

If you want to develop this package, then you can install it locally in editable mode.

### Using Makefile

    make prepare-dev
    make dev-install

#### CPython 3.10.11

    pyenv install 3.10.11
    pyenv local 3.10.11

#### Upgrade essential packages and create virtual environment

Regardless of the Python version, you should run these commands.

    cd /path/to/adsa

    python -V
    >  Python 3.10.11

    python -m pip install --upgrade pip setuptools setuptools_scm virtualenv py-make build
    python -m virtualenv venv
    source venv/bin/activate   # Linux, MacOS
    .\venv\Source\activate
    python -m pip install -r requirements.txt -r requirements-tests.txt -r requirements-extras.txt

#### Install adsa in editable mode

    python -m pip install -e /path/to/adsa


### Windows and MinGW

Make sure you have a proper Python installed with the `py` wrapper. Here, I assume version 3.7 of Python, but you can use a later one as well.

Run these commands in the root folder of the project (ie. the folder wher this README.md file is).

    py -3.10 -m pip install --upgrade pip setuptools setuptools_scm virtualenv py-make build
    py -3.10 -m virtualenv venv
    source venv/Scripts/activate.  # git-bash
    .\venv\Source\activate.        # windows terminal
    python -m pip install -r requirements.txt -r requirements-tests.txt -r requirements-extras.txt

#### Install adsa in editable mode

    python -m pip install --editable /path/to/adsa

## Run examples

    python -m adsa.examples.droplet_shape_simulation
    python -m adsa.examples.three_d_shape.py

## Run cli

    adsa-cli -h
    adsa-cli demo
    
Or:
    
    python -m adsa.cli -h
    python -m adsa.cli -h

## Run Jupyter notebook

    $ jupyter notebook

## Testing installation

The following commands are presented in pairs, which are mutually exclusive. Ie. use either one.

    make tests
    python -m pytest

    make lint
    python -m pytest --pycodestyle

    make codestyle
    python -m flake8

## Create a snapshot file

    make snapshot

## Create a distribution

    make dist
