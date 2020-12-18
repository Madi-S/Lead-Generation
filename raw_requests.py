import requests
from fake_useragent import UserAgent
import lxml.html
from multiprocessing import Pool

urls_xpath = '//a[@class=" link__09f24__1kwXV link-color--inherit__09f24__3PYlA link-size--inherit__09f24__2Uj95"]/@href'
title_xpath = 'h1'


ua = UserAgent()

url_scheme = 'https://www.yelp.com/search?find_desc={}&find_loc={}&ns=1'
URL = 'https://www.yelp.com/search?find_desc=sports%20wear&find_loc=London&start=10'
status = 'ok'


def extract_urls(html):
    tree = lxml.html.document_fromstring(html)
    urls = ['https://www.yelp.com' + url for url in tree.xpath(urls_xpath)]
    print(urls)


def parse(html):
    tree = lxml.html.document_fromstring(html)


while status:
    r = requests.get(URL, headers={'User-Agent': ua.random})
    print(r, r.ok)
    extract_urls(r.text)
    status = r.ok
