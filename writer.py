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
        # Check cache
        if in_cache(name, user):
            continue
        write_cache(name, user)
        fullpath = f'{dirname}{name}'
        realpath = os.path.realpath(fullpath)
        page = requests.get(url)
        print(f'\r{u + 1}/{count} {name}', end='')
        with open(realpath, 'wb') as image_file:
            image_file.write(page.content)
    return

def in_cache(name: str, user: str):
    filepath = f'images/{user}/cache.txt'
    realpath = os.path.realpath(filepath)
    # Check if file doesn't exist.
    if not os.path.isfile(realpath):
        return False
    with open(realpath, 'r') as cache_file:
        names = cache_file.read().split('\n')
        for n in names:
            if name == n:
                return True
    return False

def write_cache(name: str, user: str):
    filepath = f'images/{user}/cache.txt'
    realpath = os.path.realpath(filepath)
    create_dir(realpath)
    with open(filepath, 'a') as cache_file:
        cache_file.write(f'{name}\n')
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
