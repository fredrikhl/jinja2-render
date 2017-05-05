#!/usr/bin/env python
# encoding: utf-8
""" Render a Jinja2 template. """

from __future__ import print_function, unicode_literals

import argparse
import os.path
import stat
import sys
from jinja2 import FileSystemLoader, Template
from pkg_resources import get_distribution

try:
    VERSION = str(get_distribution('j2render').version)
except:
    VERSION = 'unknown'


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


def render(template, context=None):
    """ Render a file. """
    context = context or {}
    return template.render(**context)


def is_regular_file(stream):
    """ Check if an open file is a regular file. """
    return stat.S_ISREG(os.fstat(stream.fileno())[stat.ST_MODE])


def make_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '-v', '--version',
        action='version',
        version=VERSION)
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
    parser.add_argument('template',
                        nargs='?',
                        type=argparse.FileType('r'),
                        default=sys.stdin,
                        help="Template file to render")
    return parser


def main(args=None):
    args = make_parser().parse_args(args)

    # Build context
    context = dict()
    for filename in args.ctx:
        context.update(load_ctx(filename))
    for key, value in args.assign:
        context[key] = value

    # Build template
    if is_regular_file(args.template) and os.path.isfile(args.template.name):
        curdir = os.path.abspath(os.path.dirname(args.template.name))
        if curdir not in args.dirs:
            args.dirs.append(curdir)
    template_loader = FileSystemLoader(args.dirs)
    template = Template(args.template.read())
    template.environment.loader = template_loader

    print(render(template, context=context))


if __name__ == '__main__':
    main()
