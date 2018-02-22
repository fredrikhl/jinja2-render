#!/usr/bin/env python
# encoding: utf-8
""" Render a Jinja2 template. """

from __future__ import print_function, unicode_literals

import argparse
import logging
import os.path
import signal
import stat
import sys
from jinja2 import Environment, FileSystemLoader
from pkg_resources import get_distribution, DistributionNotFound

try:
    __version__ = get_distribution('j2render').version
except DistributionNotFound:
    # TODO: Or `pass`, e.g. attribute is not set?
    # TODO: Or dummy value, e.g. '0.0'
    __version__ = None

DEFAULT_ENCODING = 'utf-8'

LOGGER_FMT = '%(levelname)s %(message)s'

logger = logging.getLogger(__name__)


def load_yaml(filename):
    import yaml
    with open(filename) as f:
        return yaml.load(f)


def load_json(filename):
    import json
    with open(filename) as f:
        return json.load(f)


def load_ctx(filename):
    ext = os.path.splitext(filename)[-1]
    if ext in ('.yml', '.yaml'):
        return load_yaml(filename)
    elif ext in ('.json', ):
        return load_json(filename)

    raise NotImplementedError(
        'Unknown format {!r} for context file {!r}'.format(ext, filename))


def is_regular_file(stream):
    """ Check if an open file is a regular file. """
    return stat.S_ISREG(os.fstat(stream.fileno())[stat.ST_MODE])


def setup_logging(quiet=False, verbose=False):
    level = logging.DEBUG if verbose else logging.WARNING
    root = logging.getLogger()
    if quiet:
        root.addHandler(logging.NullHandler())
    else:
        logging.basicConfig(format=LOGGER_FMT)
    root.setLevel(level)


def make_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    # --version: should we include the `package_name`?
    parser.add_argument(
        '--version',
        action='version',
        version=__version__)
    parser.add_argument(
        '-d', '--dir',
        dest='dirs',
        action='append',
        type=os.path.abspath,
        default=[],
        metavar='DIR',
        help="Add a template directory")
    parser.add_argument(
        '--ctx',
        action='append',
        default=[],
        metavar='FILE',
        help="File(s) with context variables")
    parser.add_argument(
        '-s', '--set',
        dest='assign',
        action='append',
        default=[],
        nargs=2,
        metavar=('name', 'value'),
        help="Set context variable")
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        default=False,
        help="Get more verbose log output on stderr")
    parser.add_argument(
        '--env',
        action='store_true',
        default=False,
        help="use OS env vars as setter for values before overriding with filed values")
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        default=False,
        help="Suppress all log messages")
    parser.add_argument(
        '-e', '--encoding',
        default=None)
    parser.add_argument('template',
                        nargs='?',
                        type=argparse.FileType(mode='r'),
                        default=sys.stdin,
                        help="Template file to render")
    return parser


def main(args=None):
    args = make_parser().parse_args(args)

    setup_logging(quiet=args.quiet, verbose=args.verbose)
    logger.debug("args: {0}".format(repr(args)))

    # Build context
    context = dict()

    # if ---env is set build context from os.environ
    # file context will override env
    if args.env:
        for envvar in os.environ:
            context[envvar] = os.environ[envvar]

    # build context from file
    for filename in args.ctx:
        context.update(load_ctx(filename))
    for key, value in args.assign:
        context[key] = value

    # Build template
    if is_regular_file(args.template) and os.path.isfile(args.template.name):
        curdir = os.path.abspath(os.path.dirname(args.template.name))
        if curdir not in args.dirs:
            args.dirs.append(curdir)

    logger.info("template: {0}".format(repr(args.template.name)))

    logger.info("paths: {0}".format(repr(args.dirs)))
    template_loader = FileSystemLoader(args.dirs)

    encoding = args.encoding or args.template.encoding or DEFAULT_ENCODING
    logger.info("encoding: {0}".format(repr(encoding)))

    environment = Environment(loader=template_loader)

    template = environment.from_string(args.template.read().decode(encoding))
    print(template.render(**context))


if __name__ == '__main__':
    # Kill silently if stdin, stdout, stderr is closed
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    main()
