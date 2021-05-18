#!/usr/bin/env python3

import os
import requests
from optparse import OptionParser
from bs4 import BeautifulSoup as BS
from translator import translate
from time import sleep
import sqlite3

parser = OptionParser()
parser.add_option('-l', '--link', dest='link',
                  help='Link', metavar='LINK')
parser.add_option('-s', '--sub', dest='sub',
                  help='Subcategory_id', metavar='SUB')

(options, args) = parser.parse_args()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}


def show_table(cursor):
    cursor.execute(f'SELECT * FROM {"products_product"}')
    return cursor.fetchall()


resp = requests.get(options.link, headers=headers)
if resp.status_code == 200:
    slugs = []
    soup = BS(resp.content, 'html.parser')
    product_li = soup.find_all('li', attrs={'class': 'type-product'})
    for li in product_li:
        a = li.find_all('a', attrs={'class': 'woocommerce-loop-product__link'}, href=True)
        for url in a:
            slugs.append(url['href'])

    for product_link in slugs:
        resp = requests.get(product_link, headers=headers)
        subcategories_with_ids = {
            'Пластырь кордовый для диагональных шин': '1',
            'Пластырь кордовый для радиальных шин': '2',
            'Химия': '3',
            'Резина сырая': '4',
            'Абразивный инструмент': '5',
            'Адаптеры': '6',
            'Ручной инструмент': '7',
            'Удлинители вентиля': '8',
            'Вентили оснастка': '9',
            'Вулканизационное оборудование': '10',
            'Плоские пневмоподушки чехлы': '11',
            'Электроматы': '12',
            'Пистолет подкачки': '13',
            'Пневмодрели': '14',
            'Прочий пневмоинструмент': '15',
            'Оборудование для шиноремонтной мастерско': '16',
            'Смазочные материалы': '17',
            'Пластыри кордовые для радиальных шин': '18',
            'Ремпластина': '19',
            'Пластыри с металлокордом': '20',
            'Пластыри кордовые для диагональных шин': '21',
            'Жгуты ремонтные': '22',
            'Универсальные латки': '23',
            'Грибки для ремонта шин': '24',
            'Ножки грибков': '25',
            'Балансировочные материалы': '26',
            'Латки камерные (круглые)': '27',
            'Латки камерные (овальные)': '28',
            'Вентили для ремонта камер': '29',
            'Резина сырая': '30',
            'Герметик': '31',
            'Клей': '32',
            'Буферный очиститель': '33',
            'Термоклей': '34',
            'Прочая химия': '35',
        }
        product_info = {
            'name': '',
            'slug': '',
            'subcategory': '',
            'price': '',
            'photo': '',
            'desc': '',
            'article': '',
        }
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_div = soup.find('div', attrs={'class': 'summary'})
            name = main_div.find('h1', attrs={'class': 'product_title'})
            product_info['name'] = name.text
            product_info['slug'] = translate(name.text)
            desc_div = main_div.find('div', attrs={'class': 'woocommerce-product-details__short-description'})
            for desc in desc_div.find_all('p')[-3:]:
                product_info['desc'] += f'{desc.text}'
            product_info['article'] = main_div.find('span', attrs={'class': 'sku'}).text
            product_info['subcategory'] = main_div.find('div', attrs={'class': 'product_meta'}).find('a').text
            product_info['price'] = main_div.find('bdi').text.replace("UZS", '').replace(',', '')
            image_link = soup.find('div', attrs={'class': 'woocommerce-product-gallery__image'}).find('img')[
                'data-large_image']
            resp = requests.get(image_link)
            product_image = open(
                f'/home/alex/Desktop/rossvik-site/src/media/media/{translate(product_info["name"])}.jpg', 'wb')
            product_image.write(resp.content)
            product_image.close()
            product_info['photo'] = f'media/{translate(product_info["name"])}.jpg'
            print(product_info['slug'])
            if product_info['subcategory'] in subcategories_with_ids:
                con = sqlite3.connect('db.sqlite3')
                cursor = con.cursor()
                params = (
                    show_table(cursor)[-1][0] + 1 if len(show_table(cursor)) != 0 else 0,
                    product_info['name'], product_info['slug'], product_info['price'], product_info['photo'],
                    product_info['desc'], product_info['article'],
                    int(subcategories_with_ids[product_info['subcategory']]))
                cursor.execute(f"INSERT INTO products_product VALUES (?,?,?,?,?,?,?,?)", params)
                con.commit()
                print("Record inserted successfully into SqliteDb_developers table ", cursor.rowcount)
                cursor.close()
            else:
                print("\n\n\nNOOOOOOOOOOOOOOOOOOOOOOOOO\n\n\n")
            sleep(1)

# h = open('page.html', 'w')
# h.write(str(resp.text))
# h.close()
