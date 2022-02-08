# Droplet shape solver

Simple Young-Laplace equation solver for small droplets

## Installation

If you just want to install the latest verions, run the following pip install command:

  pip install https://github.com/juusokorhonen/droplet-shape-solver/

## Developer installation

If you want to develop this package, then you can install it locally in editable mode.

### MacOS and Pyenv

You can use anything over Python 3.7.4. I recommend either "miniconda3-latest" or one of the later CPython builds, such as 3.10.2.

#### Miniconda3

  pyenv install minicoda3-latest
  pyenv local miniconda3-latest

#### CPython 3.10.2

  pyenv install 3.10.2
  pyenv local 3.10.2

#### Upgrade essential packages and create virtual environment

Regardless of the Python version, you should run these commands.

  python -m pip install --upgrade pip setuptools wheel virtualenv py-make
  python -m virtualenv venv
  source venv/bin/activate
  python -m pip install -r requirements.txt -r requirements-dev.txt -r requirements-extras.txt

#### Install adsa in editable mode

  python -m pip install -e .

### Windows and MinGW

Make sure you have a proper Python installed with the `py` wrapper. Here, I assume version 3.7 of Python, but you can use a later one as well.

Run these commands in the root folder of the project (ie. the folder wher this README.md file is).

  py -3.7 -m pip install --upgrade pip setuptools wheel virtualenv py-make
  py -3.7 -m virtualenv venv
  source venv/Scripts/activate
  python -m pip install -r requirements.txt -r requirements-dev.txt -r requirements-extras.txt

#### Install adsa in editable mode

    python -m pip install -e .


## Run examples

    droplet_shape_simulation.py
    three_d_shape.py

## Run cli

    adsa-cli -h
    adsa-cli demo

## Run Jupyter notebook

    $ jupyter notebook
