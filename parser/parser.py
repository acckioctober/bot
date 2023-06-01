import requests
from bs4 import BeautifulSoup


url = 'https://m.mashina.kg/search/all/'
headers = {'accept': 'https://m.mashina.kg/css/1ede353-1015a15.css',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
           }


def get_html(url):
    html = requests.get(url, headers=headers)
    return html


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='list-item list-label')
    cars = []
    for item in items:
        info = item.find('div', class_='block info-wrapper item-info-wrapper')
        car = {
            'name' : item.find('div', class_='block title').find('h2', class_='name').text.strip(),
            'link': item.find('a', href=True)['href'],
            'usd_price': item.find('div', class_='block price').find('p').text.split('\n')[1].strip(),
            'som_price': item.find('div', class_='block price').find('p').text.split('\n')[3].strip(),
            'year': info.find('p',class_='year-miles').text.strip(),
            'color': info.find('p',class_='year-miles').find('i', class_='color-icon').get('title'),
            'engine': info.find('p',class_='body-type').text.strip(),
            'mileage': info.find('p',class_='volume').text.strip(),
            'city': item.find('div', class_='block city').find('p',class_='city').text.split('\n')[1].strip(),
        }
        cars.append(car)
    return cars


def parser():
    if get_html(url).status_code == 200:
        full_cars = []
        for i in range(1, 5):
            print(f'Парсинг страницы {i}')
            html = get_html(f'{url}?page={i}')  # Сохраняем html для каждой страницы
            cars = get_content(html.text)
            full_cars.extend(cars)
        return full_cars
    else:
        raise Exception('parser Error')
