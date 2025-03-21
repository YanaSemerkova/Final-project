from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import urllib, requests, socket, re, lxml, io, bs4, sqlite3, pandas, sqlalchemy
from bs4 import BeautifulSoup
from requests.compat import urljoin, quote_plus, urlparse, unquote

stations_inside_ttk = [
    "Александровский сад",
    "Арбатская",
    "Баррикадная",
    "Бауманская",
    "Белорусская",
    "Библиотека имени Ленина",
    "Боровицкая",
    "ВДНХ",
    "Динамо",
    "Достоевская",
    "Китай-город",
    "Красные Ворота",
    "Кропоткинская",
    "Кузнецкий Мост",
    "Курская",
    "Лубянка",
    "Маяковская",
    "Менделеевская",
    "Новослободская",
    "Охотный Ряд",
    "Павелецкая",
    "Парк культуры",
    "Площадь Революции",
    "Пушкинская",
    "Смоленская",
    "Сретенский бульвар",
    "Сухаревская",
    "Тверская",
    "Театральная",
    "Трубная",
    "Тургеневская",
    "Цветной бульвар",
    "Чеховская",
    "Чистые пруды",
    "Чкаловская"
]

# Включаем страничку в Интернете
driver = webdriver.Chrome()
driver.get("https://findsport.ru/volleyball/hall?Search[date_start]=2025-03-11&Search[date_finish]=2025-03-25&Search[time_from]=00%3A00&Search[time_to]=24%3A00")

# Собираем данные с первого листа площадок
url = driver.current_url
html = requests.get(url).content.decode('utf-8')
soup = BeautifulSoup(html, 'lxml')
corts_names = soup.find_all('div', {'class': 'object-search-card__title'})
corts_location = soup.find_all('div', {'class': 'object-search-card__def-value object-search-card__def-value__metro'})
html_corts_urls = soup.find_all('a', {'class': 'object-search-card object-search-card_link object-search-card_type_inline object-search-card_horizontal'})

corts_urls = []
for i in html_corts_urls:
  corts_urls.append('https://findsport.ru' + i["href"])
corts_urls


list_of_corts = []
for i in corts_names:
  mas = str(i.text).split()
  cort_name = mas[0]
  for j in mas[1:]:
    cort_name += ' ' + j
  list_of_corts.append(cort_name)

corts_metro_station = []
for i in corts_location:
  mas = str(i.text).split()
  metro_station = mas[0]
  for j in mas[1:]:
    if j.islower():
      metro_station += ' ' + j
      break
  corts_metro_station.append(metro_station)

inside_ttk = []
for i in corts_metro_station:
  if i in stations_inside_ttk:
    inside_ttk.append(1)
  else:
    inside_ttk.append(0)

corts_rating = []
lists_of_comments = []
for i in range(len(corts_urls)):
    if inside_ttk[i] == 1 or inside_ttk[i] == 0:
        temp_url = corts_urls[i]
        html = requests.get(temp_url).content.decode('utf-8')
        soup = BeautifulSoup(html, 'lxml')
        html_corts_rating = soup.find_all('div', {'class': 'w-reviewlist-rating-average-mark'})
        html_comments = soup.find_all('p', {'itemprop': 'reviewBody'})

        list_of_comments = []
        for j in html_comments:
            list_of_comments.append(str(j.text))

        lists_of_comments.append(list_of_comments)

        if html_corts_rating != []:
            num = html_corts_rating[0].text.split(',')
            num = num[0] + '.' + num[1]
            corts_rating.append(float(num))
        else:
            corts_rating.append(-1)



# Листаем остальные площадки и вытаскиваем информацию из них
for i in range(2, 8):

    next_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@class='object-search-pagination__link' and @data-page='" + str(i) + "']"))
    )

    next_button.click()

    url = driver.current_url
    html = requests.get(url).content.decode('utf-8')
    soup = BeautifulSoup(html, 'lxml')
    corts_names = soup.find_all('div', {'class': 'object-search-card__title'})
    corts_location = soup.find_all('div', {'class': 'object-search-card__def-value object-search-card__def-value__metro'})
    html_corts_urls = soup.find_all('a', {
        'class': 'object-search-card object-search-card_link object-search-card_type_inline object-search-card_horizontal'})

    corts_urls = []
    for i in html_corts_urls:
        corts_urls.append('https://findsport.ru' + i["href"])
    corts_urls

    for i in corts_names:
      mas = str(i.text).split()
      cort_name = mas[0]
      for j in mas[1:]:
        cort_name += ' ' + j
      list_of_corts.append(cort_name)

    for i in corts_location:
        mas = str(i.text).split()
        metro_station = mas[0]
        for j in mas[1:]:
            if j.islower():
                metro_station += ' ' + j
                break
        corts_metro_station.append(metro_station)

    for i in corts_metro_station:
        if i in stations_inside_ttk:
            inside_ttk.append(1)
        else:
            inside_ttk.append(0)

    for i in range(len(corts_urls)):
        if inside_ttk[i] == 1 or inside_ttk[i] == 0:
            temp_url = corts_urls[i]
            html = requests.get(temp_url).content.decode('utf-8')
            soup = BeautifulSoup(html, 'lxml')
            html_corts_rating = soup.find_all('div', {'class': 'w-reviewlist-rating-average-mark'})
            html_comments = soup.find_all('p', {'itemprop': 'reviewBody'})

            list_of_comments = []
            for j in html_comments:
                list_of_comments.append(str(j.text))

            lists_of_comments.append(list_of_comments)

            if html_corts_rating != []:
                num = html_corts_rating[0].text.split(',')
                num = num[0] + '.' + num[1]
                corts_rating.append(float(num))
            else:
                corts_rating.append(-1)



print(list_of_corts)
print(corts_metro_station)
print(inside_ttk)
print(corts_rating)
print(lists_of_comments)
