#!/usr/bin/env python
#coding=utf-8

import re, os, lxml.html, time, string
from collections import OrderedDict

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

# put the path to your file directory here
DIR_PATH = 'data'   # chinese_texts
# put the path to the dictionary here
DICT_PATH = 'dic/cedict_ts.u8'   # cedict_ts.utf8
# smart transription split
re_transcr = re.compile('([^\]]*\])')
re_punct = re.compile('[《》“”！。？：  -‘、…；\n 　’—（）0-9，－]') # LEAVING WORKING PUNCT
#re_punct = re.compile('[0-9《》“”！。？：  -‘、…；\n 　’—（），－ａ-ｚＡ-Ｚ]')
re_clean1 = re.compile('(</w>)+')
re_clean2 = re.compile('<w><ana lex="\n[^\n]*\n')
re_link = re.compile('(?:see_|see_also_|(?:old)?variant_of_|same_as_)([^,]*)')


def load_dict(path): # todo: save the dictionary in json and do not load it every time
    """
    transforms the dictionary file into a computationally feasible format
    :param path: the path to the dictionary
    :return: dictionary in the form {new_tok: (old_tok, transcr, transl) ...}
    """
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


def load_corpus(path, cedict, bAnton=True):
    """
    load and read all the files, transform them into the required form, write it down
    :param path: path to the dir with files, where the processed files will be put as well
    :param cedict: Chinese dictionary
    """
    for f in os.listdir(path):
        if f.endswith('REPL.xml') and '_processed' not in f:
            #print(f)
            new_f = open(os.path.join(path, f.rsplit('.', 1)[0] + '_processed.xml'), 'w', encoding="utf-8")
            new_f.write('<?xml version="1.0" encoding="utf-8"?><html>\n<head>\n</head>\n<body>\n')
            # here goes all the transformation
            sentences = make_xml(os.path.join(path, f), cedict)
            #with open('all_zh_xml.txt', 'w')as fh:
            #  for k, v in sentences.items():
            #    fh.write(k + "\n")
            #with open('temp.out', 'w') as fh:
            #  for s, v in sentences.items():
            #    fh.write(repr(s) +  repr(v) + "\n")
            # write the transformed sentences one after another
            punct_dict = ''.maketrans(
                {'，': ',', '。': '.', '？': '?', '、': ',', '！': '!', '：': ':', '；': ';', '（': '(', '）': ')', '“': '"',
                 '”': '"', '-': '-', '《': '«', '》': '»'})
            with open(os.path.join(path, f), 'r', encoding='utf-8') as orig:
                text = unescape(orig.read())
                para = text.split('</PARAGRAPH>')
                #print('replacing...', time.asctime())
                n = 0
                for p in para:
                    try:
                        #print(p)
                        p = re.sub(r'<PARAGRAPH id="[0-9]+">', "<para>", p)
                        #print(p)
                        #zh = re.findall('<se lang="zh">([^<]*)<', p, flags=re.DOTALL)[0]
                        zh_rex = re.findall('<FOREIGN>([^<]*)<', p, flags=re.DOTALL)
                        zh = zh_rex[len(zh_rex) - 1].strip()
                        #print("Chinese text: '"+ zh + "'")
                        #with open('all_zh.txt', 'a') as fh:
                        #  fh.write(zh + "\n")
                        if zh in sentences:
                            p = p.replace(zh, sentences[zh])
                            #print(p)
                            p = re.sub(r'<FOREIGN', '<se lang="zh"', p)
                            p = re.sub(r'<NATIVE', '<se lang="ru"', p)
                            #print(p)
                            p = re.sub(r'</(FOREIGN|NATIVE)>', "</se>", p)
                            #print(p)
                            #p = p.replace(', ', ' ')
                            p = p.replace('_ ', '')
                            p = p.replace(' _', '')

                            s = re.sub(r'<para>','', re.sub(r'<se lang="ru".+</se>', "", p)).strip()
                            NS = s.replace(', ', ' ')
                            p = p.replace(s,NS)
                            s = s.replace(', ', ' ')
                            term = re.findall(r'>(\W+?)</se>',s)
                            for trm in term:
                                print(trm[0])	# RECENTLY DISABLED
                                terminal = trm[0]
                            #print(s)
                            #rus = re.sub(r'<se lang="zh".+</se>','',p)
                            #print(rus)
                            #p = re.sub(r'<se lang="ru".+</se>',)
                            #print(s)
                            sent = []
                            for sec in s.split("</w>"):
                                #print(sec)
                                sec = sec.split('/><ana')
                                new_sec = []
                                lems = []
                                for se in range(len(sec)):
                                    reg = re.findall(r'lex=("\w+?") transcr=("[0-9A-zŌÒǘāǍūÀǒÉěǚÈĀōáéǎóèǜàĚòÁúǑìíǖÓùĒīüǔēǐ]+") ', sec[se])
                                    #print(reg)
                                    for t in reg:
                                        secT = sec[se]

                                        #print(secT)
                                        #print(secT + " : "+t[0]+"=> "+t[1])
                                        secT = secT.replace(t[0], t[1])
                                        lem = convert_pinyin(t[1]).strip('"').lower()
                                        if lem not in lems:
                                            lems.append(lem)
                                        secT = secT.replace('"zh"','"zh2"')
                                        secT = re.sub(r'transcr="[0-9A-zŌÒǘāǍūÀǒÉěǚÈĀōáéǎóèǜàĚòÁúǑìíǖÓùĒīüǔēǐ]+?" ', '', secT)

                                        secT = secT.translate(punct_dict)
                                        #print(secT)
                                        new_sec.append(convert_pinyin(secT))
                                fin_lem = '/'.join(lems)
                                w_out = '/><ana'.join(new_sec)
                                #print(w_out)
                                old_lem = re.findall(r'/>(\w+$)', w_out)
                                #print(w_out)
                                #print(w_out.replace(old_lem[0], fin_lem))
                                #print("\n\n")
                                try:
                                    to_add = w_out.replace(old_lem[0], fin_lem)
                                except:
                                    #print("Error finding %s " % repr(old_lem))
                                    to_add = w_out
                                #print(to_add)
                                sent.append(to_add)
                                #print(to_add)
                            #print(p + "</w>".join(sent) + '</se>\n</para>')
                            terminal = terminal.translate(punct_dict)
                            new_f.write(p + "</w>".join(sent) + terminal +'</se>\n</para>')
                        else:
                            print("Whoops, I've just lost something: " + p)
                    except IndexError:
                        pass
                        #raise
                    #text = re_clean1.sub('</w>', text)
                    #text = re_clean2.sub('', text)
                    n += 1
            new_f.write('\n\n</body>\n</html>')
            new_f.close()


def extract_sentences(fname):
    """
    extract all Chinese sentences
    :param fname: path to the file
    :return: list of all Chinese sentences
    """
    with open(fname, 'r') as f:
        html = unescape(f.read()).replace('<?xml version="1.0" ?>', '')
    root = lxml.html.fromstring(html)
    #sentences = root.xpath(u'//se[contains(@lang, "zh")]/text()')
    sentences = root.xpath(u'//paragraph/foreign/text()')
    #print(sentences)
    return sentences

def make_xml(fname, cedict):
    """
    transform the sentences into RNC XML
    :param fname: path to the file
    :param cedict: Chinese dictionary
    :return: wrapped sentences
    """
    #print('make xml...', time.asctime())
    sentences = extract_sentences(fname)
    sent_dict = OrderedDict()
    for sent in range(len(sentences)):
        orig_sent = sentences[sent].strip()
        transformed = ''
        # take a sentence and divide it into chunks
        punct = re_punct.findall(sentences[sent])
        fragments = [x for x in re_punct.split(sentences[sent]) if x != '']
        punct_i = 0
        for fragment in fragments:
            # delete all the punctuation (keep in the original sentence)
            while len(fragment) > 0:
                if len(re.findall('[ａ-ｚ]', fragment)) > 0:
                    print('Whoosh, processing wide latin: ' + fragment)
                # if we still have smth in the fragment...
                chunk = fragment
                # find the shortest dictionary entry
                # todo: there was some dynamic algorithm for this
                while chunk not in cedict and chunk != '':
                    chunk = chunk[:-1]
                if chunk == '':
                    word_xml = '\n<w>' + fragment + '</w>'
                    transformed += word_xml.replace('=" ', '="')
                    if len(punct) != 0:
                        try:
                            transformed += punct[punct_i]
                            punct_i += 1
                        except:
                            #print("Whoops... I've failed processing a sentence, here it is: \n" + fragment + "\n")
                            pass #print(fragment)
                    fragment = fragment[1:]
                    continue
                # now we have the dictionary entry, extract its features and wrap into tags
                word_xml = '\n<w>'
                for elem in cedict[chunk]:
                    #print('elem : ',elem)
                    transcr = elem[1][1:-1]
                    transcr_parts = transcr.split()
                    new_transcr = ''
                    for tr in transcr_parts:
                        new_transcr += tr
                    new_transcr = convert_pinyin(new_transcr)

                    # preprocess the translation
                    transl = elem[2].replace('&', 'and').replace('("', '(«').replace('/"', '/«').replace(' "', ' «').replace('" ', '» ').replace('")', '»)').replace('",', '»,')\
                        .replace('"/', '»/').replace(' ', '_').replace('/', ', ').replace(', ', ' ').replace('_, ', '').strip().strip(',')
                    links = re_link.findall(transl)
                    #print('transl : ',transl,'\nlinks : ',links)
                    if links != []:
                        for link in links:
                            try:
                                char = link.split('[')[0].split('|')[1]
                            except IndexError:
                                char = link.split('[')[0].split('|')[0]
                            if char in cedict:
                                transl_char = cedict[char][0]
                                #print(type(transl_char))
                                transl_char = transl_char[2].replace('&', 'and').replace('("', '(«').replace('/"', '/«').replace(
                                    ' "', ' «').replace('" ', '» ').replace('")', '»)').replace('",', '»,') \
                                    .replace('"/', '»/').replace(' ', '_').replace(',',' ').replace('/', ', ').replace('_, ', '').strip().strip(',')
                                transl = transl.replace(link, transl_char)
                                transl = re.sub('see_|see_also_|(old)?variant_of_|same_as_', '', transl)
                                transl = transl.replace('old_old_', '')
                                #transl = transl.replace(', ',' ')
                                #print(transl)
                    if transl.strip() == 'MOD' or transl.strip() == 'PFV' or transl.strip() == 'PRG' or transl.strip() == 'PST' or transl.strip() == 'EVAL' or transl.strip() == 'QUEST' or transl.strip() == 'CAUS' or transl.strip() == 'PL' or transl.strip() == 'BA' or transl.strip() == 'ATRN' or transl.strip() == 'ATRV' or transl.strip() == 'PASS' or transl.strip() == 'DIR':
                        word_xml += '<ana lex="%s" transcr="%s" gr="%s"/>' % (chunk, new_transcr, transl)
                    else:
                        #print(transl)
                        word_xml += '<ana lex="%s" transcr="%s" sem="%s"/>' % (chunk, new_transcr, transl)
                word_xml += chunk + '</w>'
                transformed += word_xml.replace('=" ', '="')
                fragment = fragment[len(chunk):]
            if len(punct) != 0 and transformed[-1] not in punct:
                try:
                    transformed += punct[punct_i]
                    punct_i += 1
                except IndexError:
                    pass#print(fragment)
        sent_dict[orig_sent] = transformed
    #print(sent_dict)
    return sent_dict

def convert_pinyin(car):
    #car = car.lower()
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


if __name__ == '__main__':

    cedict = load_dict(DICT_PATH)
    if False:   # WOrking with old format from Lizza
        load_corpus(DIR_PATH, cedict)
    else:
        load_corpus(DIR_PATH, cedict, True)