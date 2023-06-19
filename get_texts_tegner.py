import urllib.request
import re
import json
from bs4 import BeautifulSoup


def clean_text(text):
    soup = BeautifulSoup(text, 'html.parser')
    paragraphs = soup.find_all('p')
    # so far the first paragraph usually contains poem text, but it might change in the future
    text = paragraphs[0].get_text()
    regSpace = re.compile('\s{2,}', flags=re.DOTALL)
    text = regSpace.sub('', text)
    return text


def get_names():
    with open('tegner_saga.txt', 'r', encoding='utf-8') as f:
        names = f.read().split('\n')
    for i, name in enumerate(names):
        names[i] = '_'.join(name.split())
    return names


def download_poems(poem_list):
    source = 'http://svenskadikter.com/'
    temp_arr = {}
    for poem in poem_list:
        try:
            page = urllib.request.urlopen(source+poem)
            text = page.read().decode('utf-8')
            text = clean_text(text)
            temp_arr[' '.join(poem.split('_'))] = text
        except:
            print('reading page failed')
            continue
    return temp_arr


def main():
    frithiofs_saga_poems = get_names()
    poems = download_poems(frithiofs_saga_poems)
    with open('tegner_frithiofs_saga_source_text.json', 'w', encoding='utf-8') as file:
        json.dump(poems, file)


if __name__ == '__main__':
    main()