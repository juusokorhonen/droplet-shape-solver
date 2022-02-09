# -*- coding: utf-8 -*-
"""Command line interface for interacting with the module.

The command line interface can be used to run simple simulations and analyses
using the module.
"""
import sys
import argparse
import logging
from pathlib import Path

from .demo import run_demo


def do_nothing(args):
    return 0


def run_tests(args):
    try:
        import pytest
    except ImportError:
        logging.error("Cannot run tests, pytest is not installed.")
        return -1
    logging.info("Running tests.")
    exit_code = pytest.main(["-x", str(Path(__file__).parent.resolve() / "../tests")])
    return exit_code


def cli():
    parser = argparse.ArgumentParser()

    loglevels = {
        'critical': logging.CRITICAL,
        'error': logging.ERROR,
        'warn': logging.WARNING,
        'warning': logging.WARNING,
        'info': logging.INFO,
        'debug': logging.DEBUG
    }

    def lowercase(value: str):
        return value.lower()

    def mm(value: str) -> float:
        return float(value) * 1e-3

    parser.add_argument('-log', "--loglevel",
                        default="warning",
                        choices=loglevels.keys(),
                        type=lowercase,
                        help="Logging level to use. Example: 'debug'. Default: 'warning'.")

    commands = {
        'tests': run_tests,
        'nothing': do_nothing,
        'demo': run_demo,
    }
    cmdparsers = parser.add_subparsers(dest="command", required=True)
    nothing_parser = cmdparsers.add_parser('nothing')   # noqa: F841
    tests_parser = cmdparsers.add_parser('tests')   # noqa: F841
    demo_parser = cmdparsers.add_parser('demo')
    demo_parser.add_argument("R0", default=10.0e-3, type=mm, help="Radius of curvature at top, in mm", nargs='?')
    demo_parser.add_argument("ca", default=150.0, type=float, help="Contact angle at surface, in deg.", nargs='?')
    demo_parser.add_argument("--type", default='2d', type=str, choices=['2d', '3d'], help="Plotting type to use.")
    demo_parser.add_argument("--style", default=1, type=int, choices=[1, 2], help="Plotting style to use.")

    args = parser.parse_args()
    logging.basicConfig(level=loglevels[args.loglevel])

    sys.exit(commands[args.command](args))
