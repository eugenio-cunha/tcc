#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
# import unicodedata

from os import walk
from json import dumps
from bs4 import BeautifulSoup


def main():
    result = {
        'data': []
    }
    for (dirpath, dirnames, filenames) in walk('./htm'):
        for name in filenames:
            if '.htm' in name:
                with open('./htm/{0}'.format(name), 'r') as htm_file:
                    html = BeautifulSoup(htm_file, 'html.parser')
                    wording = {
                        'html': get_html(html),
                        'competencies': get_competencies(html),
                        'theme': get_theme(html),
                        'title': get_title(html),
                        'text': get_text(html),
                    }
                    wording['score'] = sum([c['value'] for c in wording['competencies']])
                    result['data'].append(wording)
                    print(name)

    with open('./json/data.json', 'w') as json_file:
        json_file.write(dumps(result, indent=4))


def get_theme(html):
    p = html.find('p', {'class': 'redacao-tema'}, recursive=True).getText()
    theme = p.replace('Tema:', '')
    return normalize(theme)


def get_title(html):
    header = html.find('header', {'class': 'pg_cp_topoPaginas'},
                       recursive=True)
    h1 = header.find('h1', recursive=True)
    title = h1.getText()
    title = re.sub(r'\[.+\]', '', title)
    return normalize(title)


def get_text(html):
    text = html.find('div', {'id': 'texto'}, recursive=True)

    for tag_section in text.find_all('section', {'class': 'list-items'}):
        tag_section.replaceWith('')

    for tag_div in text.find_all('div', {'class': 'redacoes-corrigidas pg-bordercolor7'}):
        tag_div.replaceWith('')

    for tag_ul in text.find_all('ul'):
        tag_ul.unwrap()

    for tag_span in text.find_all('span', {'class': 'certo'}):
        tag_span.replaceWith('')

    return normalize(text.getText())


def get_competencies(html):
    result = []
    table = html.find('table', {'class': 'table-redacoes'}, recursive=True)
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        result.append({
            'competency': cols[0].getText().strip(),
            'value': float(cols[1].getText().replace(',', '.'))
        })
    return result


def get_html(html):
    source = html.find('div', {'id': 'texto'}, recursive=True)
    return str(source)


def normalize(string):
    # string = str(string or '').strip().lower()
    # norm = unicodedata.normalize('NFD', string)
    # shaved = ''.join(c for c in norm if not unicodedata.combining(c))
    # string = unicodedata.normalize('NFC', shaved)

    string = re.sub(r' "', ' “', string)
    string = re.sub(r'"', '”', string)
    string = re.sub(r' +', ' ', string)
    return string.strip()


if __name__ == '__main__':
    main()
