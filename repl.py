# coding: utf-8

import re, os, lxml.html, time
from collections import OrderedDict
import lxml.etree as ET
from lxml import objectify

PATH = '/Users/marat/Documents/ZhRuParCo/ruzhparallel-materials/corpus materials (2)'   # chinese_texts

for f in os.listdir(PATH):
    if f.endswith('8.xml') and '_processed' not in f  and 'REPL' not in f:
        print(f)
        with open(f, 'r') as fh:
            new_f = open(os.path.join(PATH, f.rsplit('.', 1)[0] + 'REPL.xml'), 'wb')
            html = fh.read()
            #html = html.replace('encoding="UTF-16"', '')
            root = ET.XML(html)
            for parent in root.xpath('//PARAGRAPH'):  # Search for parent elements
                parent[:] = sorted(parent, key=lambda x: x.tag, reverse=True)
            new_f.write(ET.tostring(root, pretty_print=True))

