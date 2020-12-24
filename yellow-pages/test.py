import json
from bs4 import BeautifulSoup

f = open('html.html')
html = f.read()

soup = BeautifulSoup(html, 'html.parser')
data = json.loads(soup.find('script', attrs={'type':'application/ld+json'}).string)

print(soup.find(attrs={'rel': 'noopener nofollow'}).text)