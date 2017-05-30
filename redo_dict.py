import csv

file = open('1_kotov-1.txt', 'r', encoding='utf-8')
reader = csv.reader(file, delimiter='\t', quotechar='"')
new_file = open('new_kotov.txt','w',encoding='utf-8')
for row in reader:
    chin = row[0]
    rus = row[1]
    new_file.write(rus+' <> '+chin+'\n')

file.close()
new_file.close()