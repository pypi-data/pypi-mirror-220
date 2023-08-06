import urllib.request
from itertools import zip_longest


def replace(x, old, new=None, strip=False) -> str:
    if not new:
        new = ''
    if isinstance(old, str):
        x = x.replace(old, new)
    if isinstance(old, list):
        for _old, _new in zip_longest(old, new, fillvalue='_'):
            if _new == None:
                _new = ''
            x = x.replace(_old, _new)

    if strip:
        x = x.strip()
    return x


def url2filename(url):
    filename = urllib.request.url2pathname(url)
    filename = replace(filename, ['S:', '.', '<', '>', '/', '\\', '|', ':', '*', '?'])
    return filename


def str2filename(url):
    return replace(url, ['S:', '.', '<', '>', '/', '\\', '|', ':', '*', '?', '://', '#'])
