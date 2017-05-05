# jinja2-render

Script to render simple Jinja2 templates.

This tool was implemented to solve my own needs for testing Ansible templates.


## Usage

```
usage: j2render.py [-h] [-v] [-d DIR] [--ctx FILE] [-s name value] [template]

Render a Jinja2 template.

positional arguments:
  template              Template file to render

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -d DIR, --dir DIR     Add a template directory
  --ctx FILE            File(s) with context variables
  -s name value, --set name value
                        Set context variable
```


## Examples

```bash
$ j2render.py --ctx examples/foo.yml -s title mytitle examples/foo.j2
--- mytitle ---
Hello,

this example template attempts to render a template with two values, 'foo' and
'bar':

 - foo: bar
 - bar: 4
---------------
```


```bash
$ cat examples/foo.j2 | j2render.py -d examples --ctx examples/foo.yml
--- base template ---
Hello,

this example template attempts to render a template with two values, 'foo' and
'bar':

 - foo: bar
 - bar: 4
---------------------
```

## TODO

- Load custom filter modules?
