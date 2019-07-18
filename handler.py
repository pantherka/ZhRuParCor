#!/usr/bin/env python3
# coding=utf-8

import re
import os
import lxml.html
import time
from collections import OrderedDict
import lxml.etree as ET
from lxml import objectify
import json
from pymystem3 import Mystem

DICK_PATH = 'cedict_ts.u8'
DICK_CACHE = 'cedict.txt'
PATH = os.path.join(os.path.dirname(__file__), 'ready_tmx')


class ZhXMLProcessor():
    def __init__(self, dict_path):
        self.re_link = re.compile('(?:see_|see_also_|(?:old)?variant_of_|same_as_)([^,]*)')
        self.re_punct = re.compile('[《》“”！。？：  -‘、…；\n 　’—（）0-9，－]')  # LEAVING WORKING PUNCT
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

    def convert_pinyin(self, car):
        """
        changes some symbols in the transcription to more specific ones

        """
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
        transcr = definition[1].strip('[').strip(']').replace(' ', '')
        transcr = self.convert_pinyin(transcr)
        return transcr

    def process_classifiers(self, definition):
        cl = re.findall(r'/CL:.+?/', definition[2])
        gr_cl = []
        for c in cl:
            gr_cl.append(c.strip('/'))
        if len(gr_cl) == 0:
            gr_cl = 'NO'
        elif len(gr_cl) > 0:
            gr_cl = ','.join(gr_cl)
            gr_cl = gr_cl.replace('[,', ',').replace('CL:', '')
            gr_cl = re.sub(r'\w\|', '', gr_cl)
            gr_cl = self.convert_pinyin(gr_cl)
        return gr_cl

    def clean_sem(self, definition):
        defi = definition[2]
        cls = re.findall(r'/CL:.+?/', defi)
        for cl in cls:
            defi = defi.replace(cl, '')
        sem = defi.replace(' ', '_').replace('/', ' ').replace(',_', ' ').replace(',', ' ').strip('_').strip()
        transcr = re.findall(r'\[[0-9A-z]+?\]', sem)
        for tr in transcr:
            tr_ = self.convert_pinyin(tr).replace('_', '')
            sem = sem.replace(tr, tr_)
        return sem

    def process_ru(self, para, txt_ru, tag):
        """
        adds morphological tagging for russian words using pymystem3
        returns a node with tagged russian text
        """
        ru = ET.Element("se", lang=tag)
        ru.text = ""
        analyz = mystem.analyze(txt_ru)
        last_ru = None
        for word in analyz:
            if 'analysis' not in word or word['analysis'] == []:
                if last_ru is not None:
                    if last_ru.tail is None:
                        last_ru.tail = ''
                    last_ru.tail += word['text']
                else:
                    ru.text = word['text']
            else:
                last_ru = ET.SubElement(ru, 'w')
                for ana in word['analysis']:
                    lex = ana['lex']
                    text = word['text']
                    buf = ana['gr']
                    if buf[len(buf) - 1] == '=':
                        buf = buf[:-1]
                    buf = buf.replace('=', ',')
                    parts = buf.split('(')
                    if len(parts) == 1:
                        ana_ru = ET.SubElement(last_ru, 'ana', gr=parts[0], lex=lex)
                    else:
                        parts[0] = parts[0][:-1]
                        if parts[1][-1] == ')':
                            parts[1] = parts[1][:-1]
                        ana_ru = None
                        for disamb in parts[1].split('|'):
                            ana_ru = ET.SubElement(last_ru, 'ana', gr=parts[0] + ',' + disamb, lex=lex)
                ana_ru.tail = text
        return ru

    def process_para(self, txt_ru, txt_zh, now):
        """
        makes a new node od ElementTree - tuple of russian, chineese and transcription
        controls the structure of tags
        returns this node

        """
        para = ET.Element("para")
        para.set('id', str(now))
        zh = ET.SubElement(para, "se", lang="zh")
        zh.text = ""
        zh2 = ET.SubElement(para, "se", lang="zh2")
        zh2.text = ""
        last_zh = None
        last_zh2 = None
        worddef = []
        if txt_ru is not None:
            ru = para.insert(0, self.process_ru(para, txt_ru, 'ru'))
        if txt_zh is not None:
            pos = 0
            while pos < len(txt_zh):
                cnt = 1
                while txt_zh[pos:pos + cnt] in self.cedict.keys() and cnt < len(txt_zh) - pos:
                    # print("Checking key: %s (%d)" % (txt_zh[pos:pos+cnt], cnt))
                    cnt += 1
                key = txt_zh[pos:pos + cnt - 1]
                if len(key) < 1:        # not found in dict
                    # add non-found char to zh/zh2
                    key = txt_zh[pos:pos + 1]
                    if last_zh is not None:
                        if last_zh.tail is None:
                            last_zh.tail = ""
                        last_zh.tail += key
                    else:
                        zh.text = zh.text + key
                    key = key.translate(self.punct_dict)
                    if last_zh2 is not None:
                        if last_zh2.tail is None:
                            last_zh2.tail = ""
                        last_zh2.tail += key
                    else:
                        zh2.text = zh2.text + key
                    pos += 1
                    continue
                pos += cnt - 1
                # print("Found key: %s (%d)\n" % (key, cnt))
                worddef = self.cedict[key]
                # print('KEY PRINTING...', key)
                # print('JSON PRINTING...',self.cedict[key])
                # TODO: form correct definition
                last_zh = ET.SubElement(zh, 'w')
                last_zh2 = ET.SubElement(zh2, 'w')
                ana_zh = None
                transcr = ""
                ana_zh2 = None
                all_transcr = []
                for definition in worddef:
                    # Appending <ana> for each interpretation
                    transcr = self.clean_transcr(definition)
                    if transcr.lower() not in all_transcr:
                        all_transcr.append(transcr.lower())
                    desc = self.clean_sem(definition)
                    gr_cls = self.process_classifiers(definition)
                    if desc in ['MOD', 'PFV', 'PRG', 'PST', 'EVAL', 'QUEST', 'CAUS', 'PL', 'BA', 'ATRN', 'ATRV', 'PASS', 'DIR']:
                        ana_zh = ET.SubElement(last_zh, "ana", lex=key, transcr=transcr, gr=desc)
                        ana_zh2 = ET.SubElement(last_zh2, "ana", lex=transcr, transcr=transcr, gr=desc)
                    else:
                        if gr_cls != 'NO':
                            ana_zh = ET.SubElement(last_zh, "ana", lex=key, transcr=transcr, sem=desc, gr='DEFAULT，' + gr_cls)
                            ana_zh2 = ET.SubElement(last_zh2, "ana", lex=transcr, transcr=transcr, sem=desc, gr='DEFAULT，' + gr_cls)
                        else:
                            ana_zh = ET.SubElement(last_zh, "ana", lex=key, transcr=transcr, sem=desc, gr='DEFAULT')
                            ana_zh2 = ET.SubElement(last_zh2, "ana", lex=transcr, transcr=transcr, sem=desc, gr='DEFAULT')
                if ana_zh is not None:
                    ana_zh.tail = key
                transcr_lem = "/".join(all_transcr)
                # print(transcr_lem)
                if ana_zh2 is not None:
                    ana_zh2.tail = transcr_lem
        return para

    def process_file(self, path, meta):
        """
        opens a file .xml and a file with metainfo _meta.txt
        adds chineese transcriptions and english definitions
        writes the result to another file, which ends with "_processed.xml"

        """
        with open(path, 'rb') as fh:
            new_f = open(path.rsplit('.', 1)[0] + '_processed.xml', 'w', encoding='utf-8')
            new_f.write('<?xml version="1.0" encoding="utf-8"?><html>\n')
            html = fh.read()
            # html = html.replace('encoding="UTF-16"', '')
            root = ET.XML(html)
            with open(meta, 'r', encoding='utf-8') as fmeta:
                info = ET.Element("head")
                for line in fmeta:
                    if 'head>' not in line:
                        new_info = ET.fromstring(line)
                        info.append(new_info)
                new_f.write(ET.tostring(info, pretty_print=True, method="xml", encoding='unicode').replace(">", ">\n"))
            new_f.write('<body>')
            now = 1
            for parent in root.xpath('//tu'):  # Search for parent elements
                parent.tag = 'para'
                ru = ""
                zh = ""
                for lang in parent:
                    for sent in lang:
                        buf_tag = lang.attrib['{http://www.w3.org/XML/1998/namespace}lang']
                        if buf_tag.split('-')[0] == 'zh':
                            zh = sent.text
                        if buf_tag.split('-')[0] == 'ru':
                            ru = sent.text
                if ru is None or zh is None:
                    print("Error fetching sentence!")
                if ru is not None or zh is not None:
                    para = self.process_para(ru, zh, now)
                    now += 1
                    new_f.write(ET.tostring(para, pretty_print=True, method="xml", encoding='unicode').replace(">", ">\n"))
            new_f.write("</body></html>")
            new_f.close()


if __name__ == '__main__':
    mystem = Mystem(
        disambiguation=False,
        weight=False,
        generate_all=True,
        use_english_names=True,)
    proc = ZhXMLProcessor(DICK_PATH)
    for f in os.listdir(PATH):
        if f.endswith('.xml') and '_processed' not in f and 'REPL' not in f:
            print("Processing %s" % f)
            p = os.path.abspath(f)
            name = os.path.basename(p)
            meta = PATH + '\\' + name[:name.find('.')] + '_meta.txt'
            if os.path.exists(meta):
                proc.process_file(os.path.join(PATH, f), meta)
            else:
                print("Error connecting metainfo for %s" % f)
