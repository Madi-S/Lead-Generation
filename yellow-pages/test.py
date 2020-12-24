from bs4 import BeautifulSoup

f = open('html.html')
html = f.read()

soup = BeautifulSoup(html, 'html.parser')
order = {
    #'Title': None,
    'Address': 'icon--24-directions-v2',
    'WebSite': 'Business website',
    'PhoneNumber': 'icon--24-phone-v2'
}

data = []
for title, str_ in order.items():
    data.append(soup.find(string=str_).next_element.text)

print(data)