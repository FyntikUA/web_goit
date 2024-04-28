import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin

# Функція для отримання даних зі сторінки з цитатами
def scrape_quotes(url):
    quotes = []
    authors = []
    author_links = []
    base_url = 'http://quotes.toscrape.com'
    while url:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Знаходимо всі елементи з класом "quote"
        for quote_box in soup.find_all('div', class_='quote'):
            # Отримуємо текст цитати
            quote = quote_box.find('span', class_='text').text
            # Отримуємо ім'я автора цитати
            author_name = quote_box.find('small', class_='author').text
            # Отримуємо теги цитати
            tags = [tag.text for tag in quote_box.find_all('a', class_='tag')]
            # Отримуємо посилання на сторінку автора
            link = urljoin(base_url, quote_box.find('a')['href'])  # Отримуємо посилання "About"
            if link not in author_links:
                author_links.append(link)
            # Додаємо інформацію про цитату до списку цитат
            quotes.append({'tags': tags, 'author': author_name, 'quote': quote}) 
            # Додаємо інформацію про автора до списку авторів, якщо його ще не було
            if author_name not in authors:
                authors.append(author_name)
        # Отримуємо наступну сторінку з цитатами
        next_button = soup.find('li', class_='next')
        url = urljoin(base_url, next_button.find('a')['href']) if next_button else None

    return quotes, authors, author_links

# Функція для скрапінгу деталей про авторів
def scrape_authors(author_urls):
    print(author_urls)
    authors_info = []
    base_url = 'http://quotes.toscrape.com'
    for url in author_urls:
        response = requests.get(urljoin(base_url, url))
        soup = BeautifulSoup(response.text, 'html.parser')
        # Отримуємо інформацію про автора
        fullname_element = soup.find('h3', class_='author-title')
        fullname = fullname_element.text.strip() if fullname_element else "Unknown"
        born_date = soup.find('span', class_='author-born-date').text.strip()
        print(born_date)
        born_location = soup.find('span', class_='author-born-location').text.strip()
        description = soup.find('div', class_='author-description').text.strip()
        # Додаємо інформацію про автора до списку
        authors_info.append({
            'fullname': fullname,
            'born_date': born_date,
            'born_location': born_location,
            'description': description
        })

    return authors_info

# Отримуємо список цитати, лінки та авторів зі сторінки
quotes, author_urls, author_link = scrape_quotes('http://quotes.toscrape.com/')
# Отримуємо деталі про авторів
authors_info = scrape_authors(author_link)

# Зберігаємо дані у JSON файли
with open('quotes.json', 'w') as f:
    json.dump(quotes, f, indent=4)

with open('authors.json', 'w') as f:
    json.dump(authors_info, f, indent=4)
