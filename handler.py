#!/usr/bin/env python3
#coding=utf-8

import re, os, lxml.html, time
from collections import OrderedDict
import lxml.etree as ET
from lxml import objectify
import json

PATH = 'data'   # chinese_texts
DICK_PATH = 'dic/cedict_ts.u8'
DICK_CACHE = 'dic/cedict.dat'

class ZhXMLProcessor():
    def __init__(self, dict_path):
        self.re_link = re.compile('(?:see_|see_also_|(?:old)?variant_of_|same_as_)([^,]*)')
        self.re_punct = re.compile('[《》“”！。？：  -‘、…；\n 　’—（）0-9，－]') # LEAVING WORKING PUNCT
        self.punct_dict = ''.maketrans(
                {'，': ',', '。': '.', '？': '?', '、': ',', '！': '!', '：': ':', '；': ';', '（': '(', '）': ')', '“': '"',
                 '”': '"', '-': '-', '《': '«', '》': '»'})
        try:
            with open(DICK_CACHE, 'r') as jsonfile:
                self.cedict = json.load(jsonfile)
        except:
            self.cedict = self.load_dict(dict_path)
            with open(DICK_CACHE, 'w') as outfile:
                json.dump(self.cedict, outfile)

    def load_dict(self, path): 
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

    def search_dict(self, word):
        definition = ''
        return definition

    def anal(self, sent):
        # Take sentence, look up each sequence of words in dict
        return ('word', 'lex', 'transcr', 'sem')

    def process_para(self, txt_ru, txt_zh):
        para = ET.Element("para")
        ET.SubElement(para, "se", lang="ru").text = txt_ru
        zh = ET.SubElement(para, "se", lang="zh")
        zh2 = ET.SubElement(para, "se", lang="zh2")
        # TODO: make greedy 2-pointer search
        for pos in range(len(txt_zh)):
            cnt = 1
            while txt_zh[pos:pos+cnt] in self.cedict:
                cnt += 1
            key = txt_zh[pos:pos+cnt-1]
            if len(key) < 1:
                # TODO: add non-found char to hz/zh2
                key = txt_zh[pos:pos+1]
                zh.tail(key)
                zh2.tail(key)
                continue
            worddef = self.cedict[key]
            print(b"%s [%d - %d]" % (key.encode('utf-8'), pos, pos+cnt-1))
            # TODO: form correct definition
            for definition in worddef:
                # Appending <ana> for each interpretation
                print(definition[0].encode('utf-8'))
                #ET.SubElement(zh, "w", lex=key, transcr=worddef[0], sem=worddef[1]).text(key)
        return para

    def process_file(self, path):   
        # TODO: autodetect encoding from XML header/whatnot
        with open(path, 'r', encoding='utf-8') as fh:
            new_f = open(path.rsplit('.', 1)[0] + '_processed.xml', 'wb')
            html = fh.read()
            #html = html.replace('encoding="UTF-16"', '')
            root = ET.XML(html)
            for parent in root.xpath('//PARAGRAPH'):  # Search for parent elements
                parent.tag = 'para'
                ru = ""
                zh = ""
                for sent in parent:
                    if sent.tag == 'FOREIGN':
                        zh = sent.text
                    if sent.tag == 'NATIVE':
                        ru = sent.text
                if len(ru) < 1 or len(zh) < 1:
                    print("Error fetching sentence!")
                para = self.process_para(ru, zh)
                print(ET.tostring(para))
                parent[:] = para
            new_f.write(ET.tostring(root, pretty_print=True))

if __name__ == '__main__':
    proc = ZhXMLProcessor(DICK_PATH)
    for f in os.listdir(PATH):
        if f.endswith('8.xml') and '_processed' not in f  and 'REPL' not in f:
            print("Processing %s" % f)
            proc.process_file(os.path.join(PATH, f))
