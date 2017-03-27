#!/usr/bin/env python3
#coding=utf-8

import re, os, lxml.html, time
from collections import OrderedDict
import lxml.etree as ET
from lxml import objectify
import json

PATH = '/Users/marat/Documents/ZhRuParCo/ruzhparallel-materials/corpus materials (2)'   # chinese_texts
DICK_PATH = '/Users/marat/Documents/ZhRuParCo/ruzhparallel-materials/cedict_ts (1).u8'
DICK_CACHE = 'dic/cedict.dat'

def unescape(text):
    def fixup(m):
        text = m.group(0)
        # character reference
        try:
            if text[:3] == "&#x":
                return chr(int(text[3:-1], 16))
            else:
                return chr(int(text[2:-1]))
        except ValueError:
            pass
    return re.sub("&#?\w+;", fixup, text)

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

    def convert_pinyin(self, car):
        # car = car.lower()
        car = re.sub(r"a5", "a", car)
        car = re.sub(r"e5", "e", car)
        car = re.sub(r"i5", "i", car)
        car = re.sub(r"o5", "o", car)
        car = re.sub(r"u5", "u", car)
        car = re.sub(r"u:", "ü", car)
        car = re.sub(r"ü5", "ü", car)
        car = re.sub(r"a1", "ā", car)
        car = re.sub(r"A1", "Ā", car)
        car = re.sub(r"a2", "á", car)
        car = re.sub(r"A2", "Á", car)
        car = re.sub(r"a3", "ǎ", car)
        car = re.sub(r"A3", "Ǎ", car)
        car = re.sub(r"a4", "à", car)
        car = re.sub(r"A4", "À", car)
        car = re.sub(r"e1", "ē", car)
        car = re.sub(r"E1", "Ē", car)
        car = re.sub(r"e2", "é", car)
        car = re.sub(r"E2", "É", car)
        car = re.sub(r"e3", "ě", car)
        car = re.sub(r"E3", "Ě", car)
        car = re.sub(r"e4", "è", car)
        car = re.sub(r"E4", "È", car)
        car = re.sub(r"i1", "ī", car)
        car = re.sub(r"i2", "í", car)
        car = re.sub(r"i3", "ǐ", car)
        car = re.sub(r"i4", "ì", car)
        car = re.sub(r"o1", "ō", car)
        car = re.sub(r"O1", "Ō", car)
        car = re.sub(r"o2", "ó", car)
        car = re.sub(r"O2", "Ó", car)
        car = re.sub(r"o3", "ǒ", car)
        car = re.sub(r"O3", "Ǒ", car)
        car = re.sub(r"o4", "ò", car)
        car = re.sub(r"O4", "Ò", car)
        car = re.sub(r"u1", "ū", car)
        car = re.sub(r"u2", "ú", car)
        car = re.sub(r"u3", "ǔ", car)
        car = re.sub(r"u4", "ù", car)
        car = re.sub(r"ü1", "ǖ", car)
        car = re.sub(r"ü2", "ǘ", car)
        car = re.sub(r"ü3", "ǚ", car)
        car = re.sub(r"ü4", "ǜ", car)
        car = re.sub(r"an1", "ān", car)
        car = re.sub(r"An1", "Ān", car)
        car = re.sub(r"an2", "án", car)
        car = re.sub(r"An2", "Án", car)
        car = re.sub(r"an3", "ǎn", car)
        car = re.sub(r"An3", "Ǎn", car)
        car = re.sub(r"an4", "àn", car)
        car = re.sub(r"An4", "Àn", car)
        car = re.sub(r"ang1", "āng", car)
        car = re.sub(r"Ang1", "Āng", car)
        car = re.sub(r"ang2", "áng", car)
        car = re.sub(r"Ang2", "Áng", car)
        car = re.sub(r"ang3", "ǎng", car)
        car = re.sub(r"Ang3", "Ǎng", car)
        car = re.sub(r"ang4", "àng", car)
        car = re.sub(r"Ang4", "Àng", car)
        car = re.sub(r"en1", "ēn", car)
        car = re.sub(r"En1", "Ēn", car)
        car = re.sub(r"en2", "én", car)
        car = re.sub(r"En2", "Én", car)
        car = re.sub(r"en3", "ěn", car)
        car = re.sub(r"En3", "Ěn", car)
        car = re.sub(r"en4", "èn", car)
        car = re.sub(r"En4", "Èn", car)
        car = re.sub(r"eng1", "ēng", car)
        car = re.sub(r"Eng1", "Ēng", car)
        car = re.sub(r"eng2", "éng", car)
        car = re.sub(r"Eng2", "Éng", car)
        car = re.sub(r"eng3", "ěng", car)
        car = re.sub(r"Eng3", "Ěng", car)
        car = re.sub(r"eng4", "èng", car)
        car = re.sub(r"Eng4", "Èng", car)
        car = re.sub(r"in1", "īn", car)
        car = re.sub(r"in2", "ín", car)
        car = re.sub(r"in3", "ǐn", car)
        car = re.sub(r"in4", "ìn", car)
        car = re.sub(r"ing1", "īng", car)
        car = re.sub(r"ing2", "íng", car)
        car = re.sub(r"ing3", "ǐng", car)
        car = re.sub(r"ing4", "ìng", car)
        car = re.sub(r"ong1", "ōng", car)
        car = re.sub(r"ong2", "óng", car)
        car = re.sub(r"ong3", "ǒng", car)
        car = re.sub(r"ong4", "òng", car)
        car = re.sub(r"un1", "ūn", car)
        car = re.sub(r"un2", "ún", car)
        car = re.sub(r"un3", "ǔn", car)
        car = re.sub(r"un4", "ùn", car)
        car = re.sub(r"er2", "ér", car)
        car = re.sub(r"Er2", "Ér", car)
        car = re.sub(r"er3", "ěr", car)
        car = re.sub(r"Er3", "Ěr", car)
        car = re.sub(r"er4", "èr", car)
        car = re.sub(r"Er4", "Èr", car)
        car = re.sub(r"aō", "āo", car)
        car = re.sub(r"Aō", "Āo", car)
        car = re.sub(r"aó", "áo", car)
        car = re.sub(r"Aó", "Áo", car)
        car = re.sub(r"aǒ", "ǎo", car)
        car = re.sub(r"Aǒ", "Ǎo", car)
        car = re.sub(r"aò", "ào", car)
        car = re.sub(r"Aò", "Ào", car)
        car = re.sub(r"oū", "ōu", car)
        car = re.sub(r"Oū", "Ōu", car)
        car = re.sub(r"oú", "óu", car)
        car = re.sub(r"Oú", "Óu", car)
        car = re.sub(r"oǔ", "ǒu", car)
        car = re.sub(r"Oǔ", "Ǒu", car)
        car = re.sub(r"où", "òu", car)
        car = re.sub(r"Où", "Òu", car)
        car = re.sub(r"aī", "āi", car)
        car = re.sub(r"Aī", "Āi", car)
        car = re.sub(r"aí", "ái", car)
        car = re.sub(r"Aí", "Ái", car)
        car = re.sub(r"aǐ", "ǎi", car)
        car = re.sub(r"Aǐ", "Ǎi", car)
        car = re.sub(r"aì", "ài", car)
        car = re.sub(r"Aì", "Ài", car)
        car = re.sub(r"eī", "ēi", car)
        car = re.sub(r"Eī", "Ēi", car)
        car = re.sub(r"eí", "éi", car)
        car = re.sub(r"Eí", "Éi", car)
        car = re.sub(r"eǐ", "ěi", car)
        car = re.sub(r"Eǐ", "Ěi", car)
        car = re.sub(r"eì", "èi", car)
        car = re.sub(r"Eì", "Èi", car)
        car = re.sub(r"5", "", car)
        return car

    def clean_transcr(self, definition):
        transcr = definition[1].strip('[').strip(']').replace(' ','')
        transcr = self.convert_pinyin(transcr)
        return transcr

    def process_classifiers(self, definition):
        cl = re.findall(r'/CL:.+?/',definition[2])
        gr_cl = []
        for c in cl:
            gr_cl.append(c.strip('/'))
        if len(gr_cl) == 0:
            gr_cl = 'NO'
        elif len(gr_cl) > 0:
            gr_cl = ','.join(gr_cl)
            gr_cl = gr_cl.replace('[,',',').replace('CL:','')
            gr_cl = re.sub(r'\w\|','',gr_cl)
            gr_cl = self.convert_pinyin(gr_cl)
        return gr_cl

    def clean_sem(self, definition):
        print(definition)
        defi = definition[2]
        print(defi)
        cls = re.findall(r'/CL:.+?/', defi)
        for cl in cls:
            print(cl)
            defi = defi.replace(cl,'')
        print(defi)
        sem = defi.replace(' ','_').replace('/',' ').replace(',_',' ').replace(',',' ').strip('_').strip()
        transcr = re.findall(r'\[[0-9A-z]+?\]',sem)
        for tr in transcr:
            tr_ = self.convert_pinyin(tr).replace('_','')
            sem = sem.replace(tr,tr_)
        return sem

    def process_para(self, txt_ru, txt_zh):
        para = ET.Element("para")
        ET.SubElement(para, "se", lang="ru").text = txt_ru
        zh = ET.SubElement(para, "se", lang="zh")
        zh.text = ""
        zh2 = ET.SubElement(para, "se", lang="zh2")
        zh2.text = ""
        last_zh = None
        last_zh2 = None
        for pos in range(len(txt_zh)):
            cnt = 1
            while txt_zh[pos:pos+cnt] in self.cedict:
                cnt += 1
            key = txt_zh[pos:pos+cnt-1]
            print(("Found key: %s (%d)" % (key, cnt)).encode())
            if len(key) < 1:        # not found in dict
                # add non-found char to hz/zh2
                key = txt_zh[pos:pos+1]
                if last_zh is not None:
                    if last_zh.tail == None:
                        last_zh.tail = ""
                    last_zh.tail += key
                else:
                    zh.text = zh.text + key
                key = key.translate(self.punct_dict)
                if last_zh2 is not None:
                    if last_zh2.tail == None:
                        last_zh2.tail = ""
                    last_zh2.tail += key
                else:
                    zh2.text = zh2.text + key
                continue
            pos += cnt - 1
            worddef = self.cedict[key]
            #print('KEY PRINTING...', key)
            #print('JSON PRINTING...',self.cedict[key])
            # TODO: form correct definition
            last_zh = ET.SubElement(zh, 'w')
            last_zh2 = ET.SubElement(zh2, 'w')
            ana_zh = None
            transcr = ""
            ana_zh2 = None
            all_transcr = []
            for definition in worddef:
                #print(definition)
                # Appending <ana> for each interpretation
                transcr = self.clean_transcr(definition)
                if transcr.lower() not in all_transcr:
                    all_transcr.append(transcr.lower())
                desc = self.clean_sem(definition)
                gr_cls = self.process_classifiers(definition)
                #print(gr_cls)
                #print(desc)
                if desc == 'MOD' or desc == 'PFV' or desc == 'PRG' or desc == 'PST' or desc == 'EVAL' or desc == 'QUEST' or desc == 'CAUS' or desc == 'PL' or desc == 'BA' or desc == 'ATRN' or desc == 'ATRV' or desc == 'PASS' or desc == 'DIR':
                    ana_zh = ET.SubElement(last_zh, "ana", lex=key, transcr=transcr, gr=desc)
                    ana_zh2 = ET.SubElement(last_zh2, "ana", lex=transcr, transcr=transcr, gr=desc)
                else:
                    if gr_cls != 'NO':
                        ana_zh = ET.SubElement(last_zh, "ana", lex=key, transcr=transcr, sem=desc, gr = gr_cls)
                        ana_zh2 = ET.SubElement(last_zh2, "ana", lex=transcr, transcr=transcr, sem=desc, gr = gr_cls)
                    else:
                        ana_zh = ET.SubElement(last_zh, "ana", lex=key, transcr=transcr, sem=desc,gr='DEFAULT')
                        ana_zh2 = ET.SubElement(last_zh2, "ana", lex=transcr, transcr=transcr, sem=desc,gr='DEFAULT')
            ana_zh.tail = key
            transcr_lem = "/".join(all_transcr)
            #print(transcr_lem)
            ana_zh2.tail = transcr_lem
        return para

    def process_file(self, path):   
        # TODO: autodetect encoding from XML header/whatnot
        with open(path, 'r', encoding='utf-8') as fh:
            new_f = open(path.rsplit('.', 1)[0] + '_processed.xml', 'w')
            new_f.write('<?xml version="1.0" encoding="utf-8"?><html>\n<head>\n</head>\n<body>')
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
                parent[:] = para
                new_f.write(unescape(ET.tostring(parent, pretty_print=True, method="xml").decode('utf-8')).replace(">", ">\n"))
            new_f.write("</body></html>")
            new_f.close()

if __name__ == '__main__':
    proc = ZhXMLProcessor(DICK_PATH)
    for f in os.listdir(PATH):
        if f.endswith('est.xml') and '_processed' not in f  and 'REPL' not in f:
            print("Processing %s" % f)
            proc.process_file(os.path.join(PATH, f))
