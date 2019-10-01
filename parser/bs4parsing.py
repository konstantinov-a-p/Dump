# Выполнить парсинг сайта bash.im/best
# Выделить цитаты, а именно:
# текст цитаты, ссылку и дату
# Сохранить результаты в текстовый файл

import requests
from bs4 import BeautifulSoup

url_root = 'https://bash.im'
url_branch= '/best'

result = []

response = requests.get(url_root + url_branch)
bs4object = BeautifulSoup(response.text, 'html.parser')

content = bs4object.find_all('article',class_="quote",limit=2)
for item in content:
    quote_href = item.find('a', href=True)['href']
    quote_text = item.select_one('div.quote__body').text.strip()
    quote_date = item.select_one('div.quote__header_date').text.strip()
    #quote_date = item.find(class_="quote__header_date").get_text().strip()[:10]
    #quote_text = item.find(class_="quote__body").get_text().strip()
    #print(quote_href)
    #print(quote_date)
    #print(quote_text)
    string = f"{quote_date}\n{url_root}{quote_href}\n{quote_text}"
    result.append(string)

with open('result.txt', 'w') as file:
    file.write('\n\n'.join(result))
