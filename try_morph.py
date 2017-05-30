import pymorphy2

word = 'ишак'
morph = pymorphy2.MorphAnalyzer()

ishak = morph.parse(word)
for i in ishak:
    lex = i.lexeme
    for j in lex:
        print(j)