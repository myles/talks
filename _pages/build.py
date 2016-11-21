#!/usr/bin/env python3

"""
Converts the README.md files to html for the GitHub Pages.

Requirments:
- markdown
- pyyaml
"""

import re
import codecs
from os import chdir
from glob import iglob
from os.path import dirname, realpath, join

import yaml
from jinja2 import Template
from markdown import markdown

readme_regex = re.compile(r'(?s)(---(?P<yaml>.*)---)(?P<markdown>.*)')


def get_talk_contents(path):
    with codecs.open(path, mode='r', encoding='utf-8') as fobj:
        raw = fobj.read()

    result = re.match(readme_regex, raw).groupdict()

    talk = yaml.load(result['yaml'])

    talk['description'] = markdown(result['markdown'].strip())

    return talk


def render_talk_page(talk, tpl_contents, path):
    template = Template(tpl_contents)

    with codecs.open(join(dirname(path), 'index.html'), mode='w',
                     encoding='utf-8') as fobj:
        fobj.write(template.render(**talk))


def main():
    current_dir = join(dirname(realpath(__file__)))

    chdir(current_dir)
    talk_files = iglob('../2*/**/README.md', recursive=True)

    index_path = join(current_dir, '../README.md')
    index = {'title': 'Myles\' Talks'}

    with open(index_path, 'r') as fobj:
        index['description'] = markdown(fobj.read())

    with codecs.open(join(current_dir, 'template.html'), mode='r',
                     encoding='utf-8') as fobj:
        tpl_contents = fobj.read()

    render_talk_page(index, tpl_contents, index_path)

    for talk_file_path in talk_files:
        print(talk_file_path)
        talk = get_talk_contents(talk_file_path)
        render_talk_page(talk, tpl_contents, talk_file_path)


if __name__ == '__main__':
    main()
