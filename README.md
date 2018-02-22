# jinja2-render

Script to render simple Jinja2 templates.

This tool was implemented to solve my own needs for testing configs generated
from templates in Ansible.

The idea is to build a YAML file with any context variables used in the
template, and then simply render it to verify that it works as expected:

```bash
# j2render.py --ctx variables.yml nginx.conf.j2 > /etc/nginx/conf.d/test.conf
# nginx -t -c test.conf
```


## Usage

```
usage: j2render.py [-h] [-v] [-d DIR] [--ctx FILE] [--filters FILE] [--env] [-s name value] [template]

Render a Jinja2 template.

positional arguments:
  template              Template file to render

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -d DIR, --dir DIR     Add a template directory
  --ctx FILE            File(s) with context variables
  --filters FILE        File(s) with custom filters
  --env                 use OS env vars as setter for values before overriding
                        with filed values
  -s name value, --set name value
                        Set context variable
```


## Examples

```bash
$ echo "foo='{{ foo }}'" | j2render.py --set foo "some value"
foo='some value'
```

```bash
$ j2render.py -s foo "my value" examples/simple.j2
This is a simple template that just renders the value of two context variables,
`foo' and `bar':

* foo: 'my value'
* bar: Undefined
```

```bash
$ j2render --ctx examples/context.yml examples/list.md.j2 > list.md
```


```bash
$ export foo="fooo"
$ export bar='baar'
$ ./j2render.py --env --filters=examples/customfilter.py examples/customfilter.j2 
This is a template that renders the value of two context variables,
`foo' and `bar', but runs custom filters on it :

* foo: testfooo
* bar: baartest
```


## TODO

