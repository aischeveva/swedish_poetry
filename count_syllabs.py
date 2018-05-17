import os
import sqlite3


def get_arr(text):
    temp = text.split('\n\n')
    for i, strof in enumerate(temp):
        temp[i] = strof.split('\n')
        for lines in temp[i]:
            if '' in temp[i]:
                temp[i].remove('')
    return temp


def prepare_poem(text):
    characters_arr = []
    for line in text[0]:
        if not line.startswith('author'):
            characters_arr.append(line.split(': ')[1])
    characters_arr.append(len(text) - 1)
    temp = []
    for i in range(1, len(text)):
        temp.append('\n'.join(text[i]))
    characters_arr.append('\n\n'.join(temp))
    return characters_arr


def prepare_strophe(strophe, count):
    char_arr = []
    char_arr.append(count)
    char_arr.append('\n'.join(strophe))
    char_arr.append(len(strophe))
    char_arr.append('-')
    return char_arr


def prepare_line(line, count):
    char_arr = []
    char_arr.append(count)
    line = line.strip(' ')
    char_arr.append(line)
    examp = 'aieouyäåöAIEOUYÄÖÅ'
    temp = 0
    for letter in line:
        if letter in examp:
            temp += 1
    char_arr.append(temp)
    return char_arr

def open_file(f_path):
    with open(f_path, 'r', encoding='utf-8') as f:
        te = f.read()
    return te


def main():
    '''
    with open('boye' + os.sep + 'moln' + os.sep + '1.txt', 'r', encoding='utf-8') as f:
        te = f.read()
        print(get_arr(te))
    '''
    conn = sqlite3.connect('swedish_poetry.db')
    c = conn.cursor()
    dirs_temp = os.listdir('.') #получаем все файлы локальной директории
    poet_dirs = []
    for dir in dirs_temp: #отделяем папки от непапок
        if os.path.isdir(dir) and not dir.startswith('.'):
            poet_dirs.append(dir)
    print(poet_dirs)
    for dir in poet_dirs:
        num = 0
        if dir == 'boye':
            num = 1
        elif dir == 'ferlin':
            num = 2
        else:
            num = 3
        dict_dirs = os.listdir(dir)
        all_dicts = {}
        for d in dict_dirs:
            all_dicts[d] = os.listdir(dir + os.sep + d)
        i = 1
        for k in all_dicts:
            for dict in all_dicts[k]:
                #print(prepare_poem(get_arr(open_file('boye' + os.sep + k + os.sep + dict))))
                text = get_arr(open_file(dir + os.sep + k + os.sep + dict))
                temp = prepare_poem(text)
                c.execute("INSERT INTO poem (name, year, volume, strophe_num, text) VALUES(?, ?, ?, ?, ?)", temp)
                print(temp)
                c.execute("INSERT INTO p_a_connection VALUES(?, ?)", [i, num])
                for strophe in range(1, len(text)):
                    c.execute("INSERT INTO strophe (id_poem, text, line_num, rhyme_type) VALUES(?, ?, ?, ?)", prepare_strophe(text[strophe], i))
                    for line in text[strophe]:
                        c.execute("INSERT INTO line (id_strophe, text, syllable_num) VALUES(?, ?, ?)", prepare_line(line, strophe))
            i += 1
    conn.commit()
    conn.close()


if __name__ == '__main__':
    main()