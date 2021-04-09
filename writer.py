import os
import requests

def download_images(images: str, user: str):
    dirname = f'images/{user}/'
    urls = images.split('\n')
    urls.pop()
    count = len(urls)
    print(f'Downloading {count} images to {os.path.realpath(dirname)}')
    for u in range(count):
        url = urls[u]
        name = url.split('%')[1]
        fullpath = f'{dirname}{name}'
        realpath = os.path.realpath(fullpath)
        page = requests.get(url)
        print(f'\r{u + 1}/{count} {name}', end='')
        with open(realpath, 'wb') as image_file:
            image_file.write(page.content)
    return

def write_image_urls(images: str, user: str):
    filepath = f'images/{user}/urls.txt'
    realpath = os.path.realpath(filepath)
    create_dir(realpath)
    print(f'Writing urls to {realpath}')
    with open(filepath, 'w') as url_file:
        url_file.write(images)
    return

def create_dir(filepath: str):
    realpath = os.path.realpath(filepath)
    if os.path.isfile(filepath):
        return True
    dirpath = os.path.dirname(realpath)
    if not os.path.isdir(dirpath):
        os.makedirs(dirpath)
    return True
