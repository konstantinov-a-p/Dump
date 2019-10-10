import argparse
import requests
from bs4 import BeautifulSoup


def data_parsing(content):
    """"
    Извлекает из html сайта freelansim.ru описание заказа, ссылку, теги, цену время создания
    """
    bs4content = BeautifulSoup(content, 'html.parser')
    jobs = bs4content.find_all('article', class_='task task_list')
    output = []
    for job in jobs:
        job_link = job.select_one('a', href=True)['href']
        job_description = job.select_one('a', href=True).text
        job_price = job.aside.find_all('span')[1].text
        job_date = job.find('span', class_="params__published-at icon_task_publish_at").text
        job_tags = []
        job_tag_list = job.find_all('a', class_="tags__item_link")
        for item in job_tag_list:
            job_tags.append(item.text)

        result = {
            'title': job_description,
            'link': job_link,
            'tags': job_tags,
            'price': job_price,
            'date': job_date
        }
        output.append(result)
    return output


def data_request(url):
    """
    Запрос данных с url
    """
    return requests.get(url).text


def save_as_json(data, file):
    import json
    with open(file, 'w') as file:
        json.dump(data, file, indent=4, separators=(', ', ': '))


if __name__ == '__main__':
    from _datetime import datetime
    search_choices = ('c++', 'c#', 'objective c', 'java', 'python', 'ruby', 'haskel', 'php', 'css')

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--search", type=str, choices=search_choices, default='', help="Search query. Must be one from list. ")
    parser.add_argument("-p", "--pages", type=int, choices=range(1, 10), default=3, help="Number of pages to parse.")
    parser.add_argument("-rs", "--reverse_sort", action="store_true", help="Sort option, date is default.")
    parser.add_argument("-o", "--output", type=str, help="Specify output file")
    args = parser.parse_args()

    url_list = [f'https://freelansim.ru/tasks?q={args.search}&page={s}' for s in range(1, args.pages + 1)]

    result = []
    info = [dict(date = str(datetime.now()), url = 'https://freelansim.ru/tasks', request = args.search, pages = args.pages)]

    for url in url_list:
        html = data_request(url)
        result += data_parsing(html)
    if args.reverse_sort:
        result = result[-1::-1]
    result = info + result

    if args.output is not None:
        save_as_json(result, fr'{args.output}.json')
    else:
        print(result)