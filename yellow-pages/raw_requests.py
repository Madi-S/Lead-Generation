import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import lxml.html
from multiprocessing import Pool

urls_xpath = '//a[@class=" link__09f24__1kwXV link-color--inherit__09f24__3PYlA link-size--inherit__09f24__2Uj95"]/@href'
title_xpath = 'h1'


ua = UserAgent()

url_scheme = 'https://www.yelp.com/search?find_desc={}&find_loc={}&ns=1'
URL = 'https://www.yelp.com/search?find_desc=sports%20wear&find_loc=London&start={start}'
status = 'ok'


def extract_urls(html):
    tree = lxml.html.document_fromstring(html)
    urls = ['https://www.yelp.com' + url for url in tree.xpath(urls_xpath)]
    print(urls)


def parse(html):
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find()
    phone = soup.find()
    addr = soup.find()
    website = soup.find()

    return {'title': title, 'phone': phone}

# def main():
#     page = 1
#     urls = []
#     while True:
#         urls = extract_urls(page)
#         page += 1
#         if urls >= 200:
#             with Pool(40) as p:
#                 p.map(parse, urls)
#             urls.clear()

# while status:
#     r = requests.get(URL, headers={'User-Agent': ua.random})
#     print(r, r.ok)
#     extract_urls(r.text)
#     status = r.ok


if __name__ == '__main__':
    f = open('test.html',encoding='utf-8')
    text = f.read()
    print(parse(text))
