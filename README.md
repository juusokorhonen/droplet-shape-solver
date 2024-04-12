# Droplet shape solver

Simple Young-Laplace equation solver for small droplets

## Installation

This package is currently targeting Python version 3.10 and above.

If you just want to install the latest verions, run the following pip install command:

    pip install git+https://github.com/juusokorhonen/droplet-shape-solver/@main

## Poetry installation

These instructions are for MacOS:

Install pipx (https://pipx.pypa.io/latest/installation/):

    brew install pipx
    pipx ensurepath

Optionally add pipx completions to your shell. To get instruction, run:

    pipx completions

Install Poetry (https://python-poetry.org/docs/):

    pipx install poetry

### Possible problems

Sometimes you will get an error when pip tries to install **llvmlite**: "RuntimeError: Could not find a `llvm-config` binary. There are a number of reasons this could occur, please see: https://llvmlite.readthedocs.io/en/latest/admin-guide/install.html#using-pip for help."

Install LLVM 14:

    brew install llvm@14
    export LLVM_CONFIG=/opt/homebrew/opt/llvm@14/bin/llvm-config

Sometimes poetry might not read .python-version file but try to use the wrong version instead. In this case run:

    poetry env use ~/.pyenv/versions/3.11.7/bin/python

## Developer installation

If you want to develop this package, then you can install it locally in editable mode.

#### CPython 3.10.11

    pyenv install 3.10.11
    pyenv local 3.10.11

#### Upgrade essential packages and create virtual environment

Regardless of the Python version, you should run these commands.

    cd /path/to/adsa

    python -V
    >  Python 3.11.7

    poetry install
    poetry shell

#### Install adsa in editable mode

Poetry install by default the current project.

### Windows and MinGW

Make sure you have a proper Python installed with the `py` wrapper. Here, I assume version 3.11 of Python, but you can use a later one as well.

Run these commands in the root folder of the project (ie. the folder wher this README.md file is).

    py -3.11 -m pip install --upgrade pip poetry
    py -3.11 -m poetry install
    py -3.11 -m poetry shell

## Run demo

    python -m adsa.cli demo

## Run cli

    adsa-cli -h
    adsa-cli demo
    
Or:
    
    python -m adsa.cli -h
    python -m adsa.cli -h

## Run Jupyter notebook

    poetry shell
    cd notebook
    jupyter notebook

## Testing installation

    python -m pytest

    python -m pytest --pycodestyle

    python -m flake8