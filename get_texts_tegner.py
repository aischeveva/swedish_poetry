import urllib.request
import re
import os
import html


def clean_text(text):
    regClean = re.compile('<.*?>', flags=re.DOTALL)
    regSpace = re.compile('\s{2,}', flags=re.DOTALL)
    text = regClean.sub('', text)
    text = regSpace.sub('', text)
    text = html.unescape(text)
    return text


def get_names():
    with open('tegner_saga.txt', 'r', encoding='utf-8') as f:
        names = f.read().split('\n')
    for i, name in enumerate(names):
        names[i] = '_'.join(name.split())
    return names


def download_poems(poem_list):
    user = 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; .NET4.0E; .NET4.0C; .NET CLR 3.5.30729; .NET CLR 2.0.50727; .NET CLR 3.0.30729; Tablet PC 2.0; rv:11.0) like Gecko'
    #req = urllib.request.Request('https://yandex.ru/pogoda/10463', headers={'User-Agent': user_agent})
    source = 'http://svenskadikter.com/'
    temp_arr = {}
    for poem in poem_list:
        try:
            #req = urllib.request.Request(source + poem, headers={'User-Agent': user_agent})
            #with urllib.request.urlopen(req) as response:
            #    text = response.read().decode('utf-8')
            page = urllib.request.urlopen(source+poem)
            text = page.read().decode('utf-8')
            text = clean_text(text)
            temp_arr[' '.join(poem.split('_'))] = text
        except:
            print('oh no')
            continue
    return temp_arr


def main():
    print(get_names())
    print(download_poems(get_names()))


if __name__ == '__main__':
    main()