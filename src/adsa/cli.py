# -*- coding: utf-8 -*-
"""Command line interface for interacting with the module.

The command line interface can be used to run simple simulations and analyses
using the module.
"""
import sys
import argparse
import logging
from typing import Tuple, List
from datetime import datetime
from pathlib import Path
from lazy_import import lazy_callable
run_demo = lazy_callable('adsa.demo.run_demo')
run_sweep = lazy_callable('adsa.demo.run_sweep')
#from .demo import run_demo


def do_nothing(args):
    return 0


def run_tests(args):
    try:
        import pytest
        from . import units
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
        'sweep': run_sweep,
    }
    cmdparsers = parser.add_subparsers(dest="command", required=True)
    nothing_parser = cmdparsers.add_parser('nothing')   # noqa: F841
    tests_parser = cmdparsers.add_parser('tests')   # noqa: F841
    demo_parser = cmdparsers.add_parser('demo')
    demo_parser.add_argument("R0", default=10.0e-3, type=mm, help="Radius of curvature at top, in mm", nargs='?')
    demo_parser.add_argument("ca", default=150.0, type=float, help="Contact angle at surface, in deg.", nargs='?')
    demo_parser.add_argument("--type", default='2d', type=str, choices=['2d', '3d'], help="Plotting type to use.")
    demo_parser.add_argument("--style", default=1, type=int, choices=[1, 2], help="Plotting style to use.")
    demo_parser.add_argument("--save", type=str, help="Save output to provided filename")
    demo_parser.add_argument("--noshow", default=False, action='store_true', help="Do not show the output image.")

    def mm_range(value: str) -> List[float]:
        value_split = value.strip().split(",")
        if len(value_split) == 1:
            return list(max(0.0, float(value_split[0])*1e-3))

        from_ = max(0.0, float(value_split[0])*1e-3)
        to_ = max(from_, float(value_split[2])*1e-3)
        step_ = max(0.0, float(value_split[1])*1e-3)

        n_steps = int((to_ - from_)/step_)+1
        return list(from_ + step_*x for x in range(n_steps))

    def deg_range(value: str) -> List[float]:
        value_split = value.strip().split(",")
        if len(value_split) == 1:
            return list(max(0.0, float(value_split[0])*1e-3))

        from_ = min(max(0.0, float(value_split[0])), 180.0)
        to_ = min(max(from_, float(value_split[2])), 180.0)
        step_ = max(0.0, float(value_split[1]))

        n_steps = int((to_ - from_)/step_)+1
        return list(from_ + step_*x for x in range(n_steps))

    def str_list(value: str) -> List[str]:
        return value.strip().split(",")

    datestr = datetime.now().strftime('%Y%m%d%H%M%S')

    sweep_parser = cmdparsers.add_parser('sweep')
    sweep_parser.add_argument("R0", type=mm_range, help="Radius of curvature at the top, in mm. Example: '1,0.5,2.5' for sweep of values 1, 1.5, 2.0.")
    sweep_parser.add_argument("ca", type=deg_range, help="Contact angle at surface, in degrees. Example: '60,15,91' for sweep of values 60, 75, 90.")
    sweep_parser.add_argument("--filename", type=str, help="Filename tempalte the use. Please include both {ca}, {R0}, {ext} as template variables. Example: 'output/out_{ca}deg_{R0}mm.png'.",
                              default=f"output/{datestr}_{{ca}}deg_{{R0}}mm.{{ext}}")
    sweep_parser.add_argument("--filetypes", type=str_list, help="File type extensions to save. Example: 'png,svg'. Default: 'png'", default="png")
    sweep_parser.add_argument("--style", default=1, type=int, choices=[1, 2], help="Plotting style to use.")
    sweep_parser.add_argument("--results", type=str, help="Filename where to store csv results.",
                              default=f"output/{datestr}_results.csv")

    args = parser.parse_args()
    logging.basicConfig(level=loglevels[args.loglevel])

    sys.exit(commands[args.command](args))


if __name__ == "__main__":
    cli()
