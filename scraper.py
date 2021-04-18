import os
import argparse
import requests
from bs4 import BeautifulSoup

class Scraper:
    _parser = 'html.parser'
    _images = []

    def __init__(self, user: str, instance: str):
        self._user = user
        self._instance = instance
        self._image_dir = f'images/{user}/'
        self._archive_path = f'{self._image_dir}archive.txt'
        return

    def scrape(self):
        # Get image urls from nitter.
        self._get_image_urls()
        # Save images to a file.
        self._download_images()
        return

    def _download_images(self):
        count = len(self._images)
        for i in range(count):
            image = self._images[i]
            filename = image.split('%')[1]
            if self._in_archive(filename):
                print(f'{filename} already in archive')
                continue
            url = f'{self._instance}{image}'
            print(f'\r{i}/{count} {url}', end='')
            r = requests.get(url)
            r.raise_for_status()
            # Check if directory exists.
            if not os.path.isdir(self._image_dir):
                os.makedirs(self._image_dir)
            # Save image to file.
            with open(f'{self._image_dir}{filename}', 'wb') as image_file:
                image_file.write(r.content)
            # Save href to archive.
            self._save_to_archive(filename)
        return

    def _get_image_urls(self):
        # Scrape nitter for image urls.
        cursor = ''
        self._images = []
        while cursor is not None:
            url = self._get_url(cursor)
            print(url)
            soup = self._get_soup(url)
            self._get_images(soup)
            cursor = self._get_cursor(soup)
        # Return image urls.
        print(f'Found {len(self._images)} images in total')
        return

    def _in_archive(self, image: str):
        try:
            with open(self._archive_path, 'r') as archive_file:
                for line in archive_file:
                    if image == line.strip('\n'):
                        return True
            return False
        except FileNotFoundError:
            return False

    def _save_to_archive(self, image: str):
        with open(self._archive_path, 'a') as archive_file:
            archive_file.write(f'{image}\n')
        return

    def _get_url(self, cursor: str):
        url = f'{self._instance}{self._user}/media{cursor}'
        return url

    def _get_soup(self, url: str):
        r = requests.get(url)
        r.raise_for_status()
        soup = BeautifulSoup(r.content, self._parser)
        return soup

    def _get_cursor(self, soup: str):
        element = soup.find('a', string='Load more')
        return None if element is None else element['href']

    def _get_images(self, soup: str):
        count = 0
        timeline = soup.find('div', class_='timeline')
        items = timeline.find_all('div', class_='timeline-item')
        for item in items:
            images = item.find_all('a', class_='still-image')
            for image in images:
                href = image['href'][1:]
                self._images.append(href)
                count += 1
        print(f'Found {count} images')
        return

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scrape twitter')
    parser.add_argument('user', type=str, help='The user to scrape')
    args = parser.parse_args()
    Scraper(args.user, 'https://birdsite.xanny.family/').scrape()
