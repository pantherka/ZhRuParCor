# coding: utf-8

import re, os, lxml.html, time
from collections import OrderedDict
import lxml.etree as ET
from lxml import objectify
import json

PATH = 'data'   # chinese_texts
DICK_PATH = 'dic/cedict_ts.u8'
DICK_CACHE = 'dic/cedict.dat'

class ZhXMLProcessor():
    def __init__(self):
        try:
            with open(DICK_CACHE, 'r') as jsonfile:
                self.cedict = json.load(jsonfile)
        except:
            self.cedict = self.load_dict(DICK_PATH)
            with open(DICK_CACHE, 'w') as outfile:
                json.dump(self.cedict, outfile)

    def load_dict(self, path): # todo: save the dictionary in json and do not load it every time
        """
        transforms the dictionary file into a computationally feasible format
        :param path: the path to the dictionary
        :return: dictionary in the form {new_tok: (old_tok, transcr, transl) ...}
        """
        re_transcr = re.compile('([^\]]*\])') 
        print('load dict...', time.asctime())
        cedict = {}
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('#') or line == ' CC-CEDICT\n':
                    continue
                old, new, transcr, transl = line.strip().split(' ', 3)
                m = re_transcr.search(transl)
                if m is not None:
                    transcr += ' ' + m.group(1)
                    transl = transl.replace(m.group(1), '')
                    scr, sl = transcr.split(']', 1)
                    transcr = scr + ']'
                    transl = sl + transl
                if new not in cedict:
                    cedict[new] = [(old, transcr, transl)]
                else:
                    cedict[new].append((old, transcr, transl))
        return cedict

def read_files():
    for f in os.listdir(PATH):
        if f.endswith('8.xml') and '_processed' not in f  and 'REPL' not in f:
            print(f)
            with open(os.path.join(PATH, f), 'r') as fh:
                new_f = open(os.path.join(PATH, f.rsplit('.', 1)[0] + 'REPL.xml'), 'wb')
                html = fh.read()
                #html = html.replace('encoding="UTF-16"', '')
                root = ET.XML(html)
                for parent in root.xpath('//PARAGRAPH'):  # Search for parent elements
                    parent[:] = sorted(parent, key=lambda x: x.tag, reverse=True)
                new_f.write(ET.tostring(root, pretty_print=True))

if __name__ == '__main__':
    proc = ZhXMLProcessor()