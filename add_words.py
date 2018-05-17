import sqlite3
import os
import html


def add_words():
    conn = sqlite3.connect('swedish_poetry.db') ##открываю базу
    c = conn.cursor() ## создаю курсор
    c.execute('SELECT id, text FROM line') ##вытягиваю Id и текст строк
    lin = c.fetchall() ##получаю их списком
    for l in lin:
        with open('temp.txt', 'w', encoding='utf-8') as f:
            f.write(l[1]) ##записываю текст строки во временный файл
        os.system(r'java -jar stagger.jar -modelfile models'+ os.sep + 'sic.bin -tag temp.txt >annotated_conll' + os.sep + str(l[0]) + '.conll') ##тэглю файл и складываю резалты в папочку
        with open('annotated_conll' + os.sep + str(l[0]) + '.conll', 'r', encoding='utf-8') as f:
            text = f.read().split('\n')
        print(text)
        for i, word in enumerate(text):
            text[i] = word.split('\t')
        for word in text: ##собираю морфоразметку в одну строку
            if word[0] != '':
                temp_str = ''
                for part in word:
                    if part.isupper() or '|' in part:
                        temp_str += part + ' '
                print(word)
                c.execute('INSERT INTO word (id_line, word, gloss, lemma) VALUES (?, ?, ?, ?)', [l[0], word[1], temp_str, word[2]]) ##складываю все в базу
                conn.commit()


if __name__ == '__main__':
    add_words()