#!/usr/bin/env python3
#coding=utf-8
import  re

quant = '每各本诸'
directives = ['上','下','前','后','里','内','外','中','间','左','右','南','北','东','西','旁','对']
stop_dir = '之以'
de = '的地'
glossary = []

with open('glossary_xiandai_ext.txt','r',encoding='utf-8') as glossary_txt:
    for line in glossary_txt:
        line = line.strip()
        glossary.append(line)
        #print(line)
new_corp = open('new_corpus_mandarin.txt','w',encoding='utf-8')
with open('tagged_mandarinUTF8.txt', 'r', encoding='utf-8') as corpus:
    for line in corpus:
        tokens = line.split()
        new_line = []
        for token in tokens:
            tokentag = token.split('/')
            token_untagged = tokentag[0]
            #print(token_untagged)
            if token_untagged not in glossary:
                print(token)
                last = len(token) - 3
                if len(token) > 3 and token.endswith('/r') and token[0] in quant:
                    new_quant = token[0] + '/r'
                    new_word = token[1:]
                    new_word = new_word.replace('/r','/n')
                    new_line.append(new_quant)
                    new_line.append(new_word)
                elif len(token) == 4 and token.endswith('/s') and token[last-1] not in directives and token[last] in directives:

                    new_dir = token[last:]
                    new_word = token.replace(new_dir,'/n')
                    new_dir = new_dir.replace('/s','/f')
                    new_line.append(new_word)
                    new_line.append(new_dir)
                elif len(token) > 4 and token.endswith('/z') and token[last] in de:
                    new_de = token[last]+'/u'
                    new_word = token.replace(token[last],'')
                    #new_word = token.replace('/z', '/z')
                    new_line.append(new_word)
                    new_line.append(new_de)
                elif len(token) > 4 and token.endswith('/l') and token[last] == '的':
                    new_de = token[last] + '/u'
                    new_word = token.replace(token[last], '')
                    new_word = token.replace('/l', '/z')
                    new_line.append(new_word)
                    new_line.append(new_de)
                else:
                    new_line.append(token)
            else:
                new_line.append(token)
            """elif len(token) > 4 and token.endswith('/s') and token[last - 1] not in stop_dir and token[last] in directives and token[last - 1] in directives:
                ch = token[last]
                while ch in directives:
                    ch = token[last-1]
                new_dir = ch + '/f'
                new_word = token.replace(new_dir, '/n')
                new_line.append(new_word)
                new_line.append(new_dir)"""

        new_line.append('\n')
        line_to_write = ' '.join(new_line)
        new_corp.write(line_to_write)

new_corp.close()
