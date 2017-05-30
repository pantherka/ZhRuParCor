import pymorphy2
morph = pymorphy2.MorphAnalyzer()

line = 'Я люблю китайско-русский параллельный корпус НКРЯ!'

def normal_form(line):
    tokens = line.split()
    lemmas = []
    for token in tokens:
        if len(morph.parse(token)) == 1:
            lemmas.append(morph.parse(token)[0].normal_form)
        else:
            lemmas.append(token)
    new_line = (' ').join(lemmas)
    return new_line

if __name__ == '__main__':
    print(normal_form(line))

