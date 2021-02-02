import requests
from bs4 import BeautifulSoup
import csv
import os
import time

URL = ''
HEADERS = {'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36', 'accept': '*/*'}
# Paste site hostname
HOST=''
FILE = ''

def get_html (url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find('div', class_='bx-pagination-container').find('ul').find_all('li')
    if pagination:
        return int(pagination[-2].get_text())
    else:
        return 1

def get_urls(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='tabloid nowp')
    itemsURLs = []
    for item in items:
        itemsURLs.extend({
            HOST + item.find('a', class_='name').get('href'),
        })
    return itemsURLs

def parse():
    URL = input('Введите URL каталога: ')
    URL = URL.strip() + '/'
    html = get_html(URL)
    if html.status_code == 200:
        productsURLs = []
        pages_count=get_pages_count(html.text)
        for page in range (1, pages_count+1):
            print(f'Парсинг ссылок страниц, страница {page} из {pages_count}...')
            html = get_html(URL, params={'PAGEN_1': page})
            productsURLs.extend(get_urls(html.text))
        print(f'Получено {len(productsURLs)} страниц в списке')
    else:
        print('Ошибка в получении данных списка')
    return productsURLs

def get_meta(html):
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup.find_all('html')
    metatags = []
    for tag in tags:
        url = tag.find("meta", property="og:url")
        title = tag.find("meta",  property="og:title")
        description = tag.find("meta", property="og:description")
        h1 = tag.find('h1').get_text()
        # check
        url["content"] if url else "URL не указан"
        title["content"] if title else "Title не указан"
        description["content"] if title else "Description не указан"
        h1 if title else "H1 не указан"
        metatags.append({
            'url': url["content"],
            'title': title["content"],
            'description': description["content"],
            'h1': h1
        })
    return metatags

def save_file (tags,path):
    with open(path,'w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file, delimiter='В¬')
        writer.writerow(['URL', 'Title', 'Description', 'H1'])
        for tag in tags:
            writer.writerow([tag['url'], tag['title'], tag['description'], tag['h1']])

def finalParse():
    FILE = input('Введите название файла:')
    FILE = FILE.strip() + '.csv'
    productsURLs = parse()
    bad_chars = ["{","}","'"]
    metatags=[]
    for productURL in productsURLs:
        for i in bad_chars:
            strURL = str(productURL)
            URL = strURL.replace(i,'')
        print (f'Обработка страницы: {URL}')
        html = get_html(URL)
        metatags.extend (get_meta(html.text))
        time.sleep(2)
            # print (metatags)
    print('Парсинг данных завершен, файл сохранён в кодировке: UTF-8, Delimiter указан символом: ¬')
    save_file(metatags, FILE)
finalParse()