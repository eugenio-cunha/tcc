#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json


def main():
    with open('./json/data.json', 'r') as json_file:
        data = json.load(json_file)
        with open('./tab/data.tab', 'w') as tab_file:
            tab_file.write('mS#theme\tS#title\tS#text\tcC#comp1\tiC#comp2\tiC#comp3\tiC#comp4\tiC#comp5\n')
            for i, wording in enumerate(data['data']):
                print(i)
                tab_file.write('"{0}"\t"{1}"\t"{2}"\t{3:.2f}\t{4:.2f}\t{5:.2f}\t{6:.2f}\t{7:.2f}\n'
                               .format(wording['theme'],
                                       wording['title'],
                                       wording['text'],
                                       wording['competencies'][0]['value'],
                                       wording['competencies'][1]['value'],
                                       wording['competencies'][2]['value'],
                                       wording['competencies'][3]['value'],
                                       wording['competencies'][4]['value']))


if __name__ == '__main__':
    main()
