#!/usr/bin/env python3

"""
Converts the README.md files to html for the GitHub Pages.

Requirments:
- markdown
- pyyaml
"""

import re
import yaml
import codecs
from os import chdir
from glob import iglob
from os.path import dirname, realpath, join

from markdown import markdown

readme_regex = re.compile(r'(?s)(---(?P<yaml>.*)---)(?P<markdown>.*)')


def get_talk_contents(path):
    with codecs.open(path, mode='r', encoding='utf-8') as fobj:
        raw = fobj.read()

    result = re.match(readme_regex, raw).groupdict()

    talk = yaml.load(result['yaml'])

    talk['description'] = markdown(result['markdown'].strip())

    return talk


def render_talk_page(talk, template, path):
    with codecs.open(join(dirname(path), 'index.html'), mode='w',
                     encoding='utf-8') as fobj:
        fobj.write(template.format(**talk))


def main():
    current_dir = join(dirname(realpath(__file__)))

    chdir(current_dir)
    talk_files = iglob('../2*/**/README.md', recursive=True)

    with codecs.open(join(current_dir, 'template.html'), mode='r',
                     encoding='utf-8') as fobj:
        tpl = fobj.read()

    for talk_file_path in talk_files:
        print(talk_file_path)
        talk = get_talk_contents(talk_file_path)
        render_talk_page(talk, tpl, talk_file_path)


if __name__ == '__main__':
    main()
