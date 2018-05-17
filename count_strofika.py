import sqlite3


def correct_stanza():
    conn = sqlite3.connect('swedish_poetry.db')
    c = conn.cursor()
    c.execute('SELECT id, text FROM poem')
    poem_list = c.fetchall()
    for item in poem_list:
        stroph_list = item[1].split('\n\n')
        for strophe in stroph_list:
            c.execute('INSERT INTO strophe (id_poem, text, line_num) VALUES (?, ?, ?)', [item[0], strophe, len(strophe.split('\n'))])
            conn.commit()


def correct_lines():
    conn = sqlite3.connect('swedish_poetry.db')
    c = conn.cursor()
    c.execute('SELECT id, text FROM strophe')
    stroph_list = c.fetchall()
    examp = 'aieouyäåöAIEOUYÄÖÅ'
    for item in stroph_list:
        lines = item[1].split('\n')
        for line in lines:
            temp = 0
            for letter in line:
                if letter in examp:
                    temp +=1
            c.execute('INSERT INTO line (id_strophe, text, syllable_num) VALUES (?, ?, ?)', [item[0], line, temp])
            conn.commit()


def count_stanza():
    conn = sqlite3.connect('swedish_poetry.db')
    c = conn.cursor()
    c.execute('SELECT id FROM poem')
    poems = c.fetchall()
    for id in poems:
        c.execute('SELECT line_num FROM strophe WHERE id_poem=?', id)
        stros = c.fetchall()
        flag = True
        print(id)
        print(stros)
        for i in range(1, len(stros)):
            if stros[i] != stros[i - 1]:
                flag = False
        if flag == True:
            exp = 'regular'
        else:
            exp = 'irregular'
        #c.execute('UPDATE poem SET strophika=? WHERE id=?', [exp, id[0]])
        #conn.commit()


def count_syllab():
    conn = sqlite3.connect('swedish_poetry.db')
    c = conn.cursor()
    c.execute('SELECT id FROM strophe')
    lines = c.fetchall()
    for id in lines:
        c.execute('SELECT syllable_num FROM line WHERE id_strophe=?', id)
        stros = c.fetchall()
        flag = True
        for i in range(1, len(stros)):
            if stros[i] != stros[i - 1]:
                flag = False
        if flag == True:
            exp = 'regular'
        else:
            exp = 'irregular'
        c.execute('UPDATE strophe SET syllab_descr=? WHERE id=?', [exp, id[0]])
        conn.commit()


if __name__ == '__main__':
    #correct_stanza()
    #correct_lines()
    count_stanza()
    #count_syllab()