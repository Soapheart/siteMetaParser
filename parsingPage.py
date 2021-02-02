import requests
from bs4 import BeautifulSoup
import csv
import os
import time

URL = ''
HEADERS = {'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36', 'accept': '*/*'}
HOST=''
FILE = 'pageMeta.csv'

def get_html (url, params=None):
    r = requests.get(url, headers=HEADERS)
    return r
def get_meta(html):
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup.find_all('meta', class_='proposition')
    metatags = []
    url = soup.find("meta", property="og:url")
    title = soup.find("meta",  property="og:title")
    description = soup.find("meta", property="og:description")
    h1 = soup.find('h1').get_text()
    # check
    url["content"] if url else "URL  не указан"
    title["content"] if title else "Title  не указан"
    description["content"] if title else "Description  не указан"
    h1 if title else "H1  не указан"
    metatags.append({
        'url': url["content"],
        'title': title["content"],
        'description': description["content"],
        'h1': h1
    })
    return metatags
    
def save_file (tags,path):
    with open(path,'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['URL', 'Title', 'Description', 'H1'])
        for tag in tags:
            writer.writerow([tag['url'], tag['title'], tag['description'], tag['h1']])

def parse():
    html = get_html(URL)
    if html.status_code == 200:
        metatags=[]
        metatags.extend (get_meta(html.text))
        save_file(metatags, FILE)
    else:
        print ('Error')

    os.startfile(FILE)
parse()