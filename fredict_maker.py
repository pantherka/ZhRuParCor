fredict = {}
fredict_file = open('fredict_corp.txt','w',encoding='utf-8')
with open('glossary_xiandai_ext.txt','r',encoding='utf-8') as glossary_txt:
    for line in glossary_txt:
        line = line.strip()
        fredict[line] = 1
with open('new_corpus_mandarin.txt','r',encoding='utf-8') as corpus:
    for line in corpus:
        line = line.split()
        tokensInLine = []
        for l in line:
            token_tag = l.split('/')
            token = token_tag[0]
            tokensInLine.append(token)
            if token in fredict:
                fredict[token] += 1

for i in fredict:
    fredict_file.write(str(fredict[i])+' '+i+'\n')
fredict_file.close()