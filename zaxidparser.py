import requests
import csv
from bs4 import BeautifulSoup
import os



os.chdir(r'C:\+Non_System\A-DATA-STOCK\Python\fama')
ZAXID_CSV = 'zaxid_news.csv'
ZAXID_CONTENT = 'zaxid_content.csv'
HOST = 'https://zaxid.net/'
URL = 'https://zaxid.net/news/'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0'
     }


def get_html(url, params=''):
    '''
    This function return web page as html-object
    url: takes page url
    params: takes parameters, HEADERS by default
    '''
    request_page = requests.get(url, headers=HEADERS, params=params)
    return request_page


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('li', class_='default-news-list')
    zaxid_news = []
    
    for item in items:
        zaxid_news.append(
            {
               'news_title': item.find('div', class_='news-title').get_text(strip=True),
               'news_time': item.find('div', class_='time').get_text(strip=True),
               'news_link': HOST + item.find('a').get('href')
                })
    return zaxid_news

def save_content(items, path):
    with open(path, 'w', newline='', encoding='utf-16') as file:
        writer = csv.writer(file, delimiter='|')
        writer.writerow(['heading', 'time', 'link'])
        for item in items:
            writer.writerow([item['news_title'], item['news_time'], item['news_link']])


def parse():
    PAGENATION = input('Submit the number of pages to be parsed: ')
    PAGENATION = int(PAGENATION.strip())
    PAGENATION = PAGENATION + 1
    html = get_html(URL)
    if html.status_code == 200:
        zaxid_news = []
        for page in range(1, PAGENATION):
            print(f'Parsing page {page}...')
            html = get_html(URL, params={'newsfrom':page*44})
            zaxid_news.extend(get_content(html.text))
            save_content(zaxid_news, ZAXID_CSV)
        print('Parsing is finished')
    else:
        print('Error')

parse()

