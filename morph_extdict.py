import pymorphy2
import os
PATH = 'dict_aligns'

morph = pymorphy2.MorphAnalyzer()
i = 0
n = 0
z = 0

for f in os.listdir(PATH):
    if 'EXT' not in f  and f.endswith("zhCogn.dic"):
        print("Reading %s" % f)
        new_dict = open(f.replace('.dic', '_EXT.dic'), 'w', encoding='utf-8')
        with open(os.path.join(PATH, f),'r',encoding='utf-8') as dict_txt:
            for line in dict_txt:
                sides = line.split(' @ ')
                rus = sides[1].replace('\n','')
                if ' ' not in rus:
                    i += 1
                    if len(morph.parse(rus)) == 1:
                        n += 1
                        rus_list = morph.parse(rus)[0].lexeme
                        for l in rus_list:
                            new_dict.write(sides[0] + ' @ ' + l[0] +'\n')
                    else:
                        grams = []
                        POStags = []
                        #print(morph.parse(rus))
                        for p in morph.parse(rus):
                            #print(p)
                            grams.append(str(p[1]))
                            #POStags = []
                            for g in grams:
                                #print(rus)
                                #print(g)
                                POS = g[0:4]
                                POStags.append(POS)
                            #print(set(POStags))
                            #print(len(set(POStags)))
                                #print(POS)
                        #print(len(set(grams)))
                        #print(len(set(POStags)))
                        if len(set(POStags)) == 1:
                            razbor_list = morph.parse(rus)[0].lexeme
                            for rl in razbor_list:
                                #print(rus)
                                #razbor_list = razbor.lexeme
                                #for l in razbor_list:

                                new_dict.write(sides[0] + ' @ ' + rl[0] + '\n')
                        else:
                            new_dict.write(sides[0] + ' @ ' + sides[1] + '\n')
                else:
                    i += 1
                    z += 1
                    new_dict.write(sides[0] + ' @ ' + sides[1] + '\n')
#print(n,' ',z)
        new_dict.close()

"""for k in morph.parse('Любовь'):
    print(k)
print(len(morph.parse('Любовь')))

print(morph.parse('Любовь')[0].lexeme)"""