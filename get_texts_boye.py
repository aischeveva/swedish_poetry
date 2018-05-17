import urllib.request
import re
import html
import os


def get_names():
    with open('dikt.txt', 'r', encoding='utf-8') as f:
        text = f.read()
        names = text.lower().strip('.?!')
        text = text.split('\n')
        #names = f.read().lower().strip('.?!')
        names = re.sub(' \.\.\.', '', names)
        names = re.sub('\.', '', names)
        names = re.sub('å|ä', 'a', names)
        names = re.sub('ö', 'o', names)
        names = re.sub('ü', 'u', names)
        names = re.sub(' ', '-', names)
        names = names.split('\n')
    dic = {}
    dic['MOLN'] = ['1922', []]
    dic['GÖMDA LAND'] = ['1924', []]
    dic['HÄRDARNA'] = ['1927', []]
    dic['FÖR TRÄDETS SKULL'] = ['1935', []]
    dic['DE SJU DÖDSSYNDERNA'] = ['1941', []]
    for i in range(0, 42):
        dic['MOLN'][1].append([names[i], text[i]])
    for i in range(42, 76):
        dic['GÖMDA LAND'][1].append([names[i], text[i]])
    for i in range(76, 110):
        dic['HÄRDARNA'][1].append([names[i], text[i]])
    for i in range(110, 149):
        dic['FÖR TRÄDETS SKULL'][1].append([names[i], text[i]])
    for i in range(149, 190):
        dic['DE SJU DÖDSSYNDERNA'][1].append([names[i], text[i]])
    return dic


def download_text(page_url):
    #print(page_url)
    try:
        page = urllib.request.urlopen(page_url)
        text = page.read().decode()
    except:
        return ''
    poem = re.findall('<PRE class="dikttext">.+?</PRE>', text, flags=re.DOTALL)[0]
    poem = re.sub('<.*?>', '', poem)
    poem = html.unescape(poem)
    return poem


if __name__ == '__main__':
    arr = get_names()
    url1 = 'http://www.karinboye.se/verk/dikter/dikter/'
    url2 = '.shtml'
    for k in arr:
        for i, poem in enumerate(arr[k][1]):
            text = download_text(url1 + poem[0] + url2)
            folder_name = k.lower()
            folder_name = re.sub(' ', '_', folder_name)
            if text != '':
                with open('boye' + os.sep + folder_name + os.sep + str(i + 1) + '.txt', 'w', encoding='utf-8') as f:
                    f.write('name: ' + poem[1].upper() + '\n')
                    f.write('year: ' + arr[k][0] + '\n')
                    f.write('author: KARIN BOYE\n')
                    f.write('volume: ' + k + '\n\n')
                    f.write(download_text(url1 + poem[0] + url2))


