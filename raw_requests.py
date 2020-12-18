import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup


ua = UserAgent()

url_scheme = 'https://www.yelp.com/search?find_desc={}&find_loc={}&ns=1'
URL = 'https://www.yelp.com/search?find_desc=sports%20wear&find_loc=London&start=10'
status = 'ok'


def extract_urls(html):
    soup = BeautifulSoup(html, 'lxml')
    urls = soup.select('')
    print(urls)


def parse(html):
    pass


while status:
    r = requests.get(URL, headers={'User-Agent': ua.random})
    print(r, r.ok)
    print(extract_urls(r.text))
    status = r.ok
