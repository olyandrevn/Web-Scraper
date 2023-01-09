import requests
from bs4 import BeautifulSoup
import string
import os

class WebScrapper:
    def __init__(self, url, num_of_pages, article_type):
        self.url = url
        self.num_of_pages = num_of_pages
        self.article_type = article_type

    def send_http_request(self, url):
        response = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})

        if response.status_code != 200:
            print(f'The URL returned {response.status_code}!')
            return -1

        return response

    def parse_website(self):
        url = self.url
        is_last_page = False
        num_page = 1
        dir = os.getcwd()

        while not is_last_page and num_page <= self.num_of_pages:
            os.chdir(dir)
            print(f'Current directory is {os.getcwd()}')
            page_dir = f'{dir}/Page_{num_page}'
            response = self.send_http_request(url)

            if response == -1:
                return -1

            soup = BeautifulSoup(response.content, 'html.parser')
            self.parse_webpage(soup, page_dir)

            next_page = soup.find('li', {'data-page': "next"})
            is_last_page = next_page.find('span', {'class': "c-pagination__link c-pagination__link--disabled"}) is not None
            num_page += 1

            if not is_last_page:
                url = 'https://www.nature.com' + next_page.find('a').get('href')

    def parse_webpage(self, soup, page_dir):
        articles = soup.find_all('article')
        curr_articles = []

        os.mkdir(page_dir)
        os.chdir(page_dir)

        print(f'\nCurrent directory is {os.getcwd()}')

        for article in articles:
            article_type = article.find('span', {'class': "c-meta__type"}).text

            if article_type != self.article_type:
                continue

            title = article.find('h3').text.strip('\n')
            link = article.find('a', {'data-track-action': "view article"}).get('href')
            link = 'https://www.nature.com' + link

            article_response = requests.get(link, headers={'Accept-Language': 'en-US,en;q=0.5'})
            article_soup = BeautifulSoup(article_response.content, 'html.parser')
            content = article_soup.find('div', {'class': 'c-article-body'}).text

            title = title.strip(string.punctuation)
            title = title.replace(' ', '_')

            f = open(title + '.txt', 'wb')
            f.write(bytes(content, encoding='utf-8'))
            f.close()

            curr_articles.append(title)

        print(curr_articles)
        print('\n')


url = 'https://www.nature.com/nature/articles?sort=PubDate&year=2020'
num_of_pages = int(input())
article_type = input()

request = WebScrapper(url, num_of_pages, article_type)
request.parse_website()
