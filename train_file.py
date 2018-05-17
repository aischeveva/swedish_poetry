import os

l = os.listdir('annotated')
for f in l:
    with open('annotated' + os.sep + f, 'r', encoding='utf-8') as fin:
        text = fin.read()
    with open('train_file.conll', 'a', encoding='utf-8') as fout:
        fout.write(text)