import os
import requests
import pylinhsu.parallel as pl


def preceding_zero(i, n):
    n_s = len(str(n - 1))
    s = str(i)
    return '0' * (n_s - len(s)) + s


def filter_urls(urls):
    result = []
    for url in urls:
        url = url.strip()
        if url == '' or url[0] == '#':
            continue
        result.append(url)
    return result


def proxies(proxy_port=None):
    if not proxy_port:
        return None
    return {
        'http': f'127.0.0.1:{proxy_port}',
        'https': f'127.0.0.1:{proxy_port}',
    }


def download_from_url(url, file_name=None, proxy_port=None):
    if not file_name:
        file_name = f'{os.path.basename(url)}'
    data = requests.get(url, proxies=proxies(proxy_port)).content
    with open(file_name, 'wb') as f:
        f.write(data)


def download_from_urls(urls, proxy_port=None):
    n = len(urls)

    def _download_from_url(i):
        url = urls[i]
        file_name = f'{preceding_zero(i, n)}.{os.path.basename(url)}'
        download_from_url(url, file_name, proxy_port)
    # pl.parallel_for(_download_from_url, range(n))
    for i, url in enumerate(urls):
        file_name = f'{preceding_zero(i, n)}.{os.path.basename(url)}'
        download_from_url(url, file_name, proxy_port)


def download_from_urls_text(text, proxy_port=None):
    urls = text.strip().splitlines()
    urls = filter_urls(urls)
    download_from_urls(urls, proxy_port)


def download_from_urls_text_file(file_path, proxy_port=None):
    with open(file_path) as f:
        urls = f.read().strip().splitlines()
        urls = filter_urls(urls)
        download_from_urls(urls, proxy_port)
