import argparse
import requests
from bs4 import BeautifulSoup
import writer

class Scraper:
    _html_parser = 'html.parser'

    def __init__(self, user: str, instance: str):
        self._user = user
        self._instance = instance
        return

    def scrape(self):
        cursor = ''
        image_urls = ''
        while True:
            url = self.get_url(cursor)
            print(url)
            soup = self.get_soup(url)
            image_urls += self.get_images(soup)
            # Find next cursor.
            cursor = self.get_cursor(soup)
            if cursor is None:
                break
        writer.write_image_urls(image_urls, self._user)
        writer.download_images(image_urls, self._user)
        return

    def get_images(self, soup:BeautifulSoup):
        out = ''
        timeline = soup.find('div', class_='timeline')
        items = timeline.find_all('div', class_='timeline-item')
        for item in items:
            images = item.find_all('a', class_='still-image')
            for image in images:
                href = image['href']
                url = f'{self._instance}{href}'
                out += f'{url}\n'
        return out

    def get_url(self, cursor:str=''):
        url = f'{self._instance}{self._user}/media{cursor}'
        return url

    def get_soup(self, url:str):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, self._html_parser)
        return soup

    def get_cursor(self, soup:BeautifulSoup):
        elements = soup.find_all('div', class_='show-more')
        for e in elements:
            if e['class'] == ['show-more']:
                cursor = e.a['href']
                return cursor
        return None

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scrape nitter for user images')
    parser.add_argument('user', help='The user to scrape')
    parser.add_argument('-i', '--instance', type=str, help='The nitter instance to use')
    args = parser.parse_args()
    instance = args.instance if args.instance is not None else 'https://nitter.nixnet.services/'
    s = Scraper(args.user, instance)
    s.scrape()
