import os
PATH = 'dict_aligns'   # chinese_texts
sizes = [5000,10000,20000,30000,40000,50000]

for f in os.listdir(PATH):
    if f.endswith('60k.dic') and 'EXT.txt' not in f:
        for size in sizes:
            with open(os.path.join(PATH, f), 'r') as fh:
                print("Generating dictionary of size %d from %s" % (size, f))
                new_f = open(os.path.join(PATH, f.rsplit('.', 1)[0] + str(size) + '.txt'),  'wb')
                entries = []
                for line in fh:
                    entries.append(line)
                    #print(line)
                    if len(entries) > size:
                        break
                for e in entries:
                    new_f.write(e.encode('utf-8'))
                new_f.close()