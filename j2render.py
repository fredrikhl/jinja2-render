#!/usr/bin/env python
# encoding: utf-8
""" Render a Jinja2 template. """

from __future__ import print_function, unicode_literals
    
import argparse
import json
import os.path
import yaml
from jinja2 import Environment, FileSystemLoader


def load_yaml(filename):
    with open(filename) as f:
        return yaml.load(f)


def load_json(filename):
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


def render(filename, context=None, template_dirs=None):
    """ Render a file. """
    context = context or dict()
    template_dirs = list(template_dirs or [])
    filename = os.path.abspath(filename)
    template_dirs.append(os.path.dirname(filename))
    env = Environment(loader=FileSystemLoader(template_dirs))
    template = env.get_template(os.path.basename(filename))
    return template.render(**context)


def main(args=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '-d', '--dir',
        dest='dirs',
        action='append',
        default=[],
        metavar='DIR',
        help="Add a template directory")
    parser.add_argument(
        '--ctx',
        action='append',
        default=[],
        metavar='FILE',
        help="File(s) with context variables")
    parser.add_argument('template', help="Template file to render")

    args = parser.parse_args(args)

    context = dict()
    for filename in args.ctx:
        context.update(load_ctx(filename))

    print(render(args.template, context=context, template_dirs=args.dirs))


if __name__ == '__main__':
    main()
