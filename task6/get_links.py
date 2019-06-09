#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Script to get links where an image has previously appeared on, through Google
Search by image.

@author: Hugo Sousa (hugosousa@dcc.ufmg.br)
'''


from bs4 import BeautifulSoup
import urllib.request


DOMAIN = 'www.google.com'


def process_url(url):
    '''
        Process URL assuring it has the proper format.

        @url: (string) URL.

        @return: (string) Processed URL.
    '''

    if url.find('http') < 0:
        url = 'https://' + url

    return url


def get_html(url):
    '''
        Get the HTML string corresponding to a particular URL.

        @url: (string) URL.

        @return: (string) HTML string.
    '''

    url = process_url(url)
    user_agent = '''Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTM
        L, like Gecko) Chrome/ 58.0.3029.81 Safari/537.36'''
    headers = [('User-Agent', user_agent),
               ("Accept-Language", "en-US,en;q=0.5"), ]
    opener = urllib.request.build_opener()
    opener.addheaders = headers

    html = opener.open(url).read().decode()
    return html


def get_page_sources(html):
    '''
        Get image sources on a particular page.

        @html: (string) Page HTML content.

        @return: (string list) List of sources of the image on the page.
    '''

    soup = BeautifulSoup(html, 'html.parser')
    return [link.a.get('href') for link in soup.find_all('h3', {'class': 'r'})]


def get_next_page(html):
    '''
        Get the HTML content for the next search result page.

        @html: (string) HTML content of current page.

        @return: (string) HTML content of next page.
    '''

    soup = BeautifulSoup(html, 'html.parser')
    next_page = soup.find_all('a', {'class': 'pn', 'id': 'pnnext'})

    if len(next_page) == 0:
        return None

    next_page_link = DOMAIN + next_page[0].get('href')
    return get_html(next_page_link)


def get_sources(url):
    '''
        Get all source links where the image has appeared on.

        @url: (string) HTML of the first result page for the image.

        @return: (string list) List of all the source links where the image has
        appeared on.
    '''

    html = get_html(url)
    sources = []

    # Only look for links where the image has appeared on.
    html = html[html.find('Páginas que incluem imagens correspondentes'):]

    while True:  # Look for other sources in the rest of the result pages.
        sources += get_page_sources(html)
        html = get_next_page(html)

        if html is None:
            break

    return sources


def main():
    '''
        Main function.
    '''

    url = '''http://images.google.com/searchbyimage?image_url=http://www.monitor-de-whatsapp.dcc.ufmg.br/data/images/139829889318352_2.jpe&obtained_at=2018-08-07'''

    sources = get_sources(url)

    for source in sources:
        print(source)


main()
