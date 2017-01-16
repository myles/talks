#!/usr/bin/env python3

"""
Converts the README.md files to html for the GitHub Pages.

Requirments:
- markdown
- pyyaml
"""

import re
import codecs
import argparse
from os import chdir, pardir
from glob import iglob
from os.path import dirname, join, realpath

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
    output = join(dirname(path), 'index.html')
    template = Template(tpl_contents)

    with codecs.open(output, mode='w', encoding='utf-8') as fobj:
        fobj.write(template.render(**talk))


def main(output_directory):
    root_dir = join(dirname(realpath(__file__)), pardir)

    chdir(root_dir)
    talk_files = iglob('2*/**/README.md', recursive=True)

    index_path = join(root_dir, 'README.md')
    index = {'title': "Myles\' Talks"}

    with open(index_path, 'r') as fobj:
        index['description'] = markdown(fobj.read())

    with codecs.open(join(root_dir, '_pages/template.html'), mode='r',
                     encoding='utf-8') as fobj:
        tpl_contents = fobj.read()

    index_output_path = join(output_directory, 'index.html')
    render_talk_page(index, tpl_contents, index_output_path)

    for talk_file_path in talk_files:
        output = join(output_directory, talk_file_path)
        talk = get_talk_contents(talk_file_path)
        render_talk_page(talk, tpl_contents, output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("output_directory")
    args = parser.parse_args()

    main(args.output_directory)
