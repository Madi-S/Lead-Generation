import re
from bs4 import BeautifulSoup


head_regex = re.compile(
    r'(ceo|owner|manager|chief|manager)', flags=re.IGNORECASE)

html = open('test.html', encoding='utf-8').read()
soup = BeautifulSoup(html, 'html.parser')

head_man = soup.find(string=head_regex)
print(head_man)
name = head_man.parent.parent.parent.find(attrs={'aria-hidden': True}).text
print(name)
