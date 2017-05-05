# jinja2-render

Script to render Jinja2 templates


## Usage

```
usage: j2render.py [-h] [-d DIR] [--ctx FILE] template

Render a Jinja2 template.

positional arguments:
  template           Template file to render

optional arguments:
  -h, --help         show this help message and exit
  -d DIR, --dir DIR  Add a template directory
  --ctx FILE         File(s) with context variables
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
