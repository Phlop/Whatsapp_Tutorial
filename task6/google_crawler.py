#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Collect sources where images have previously appeared on, for a set of JSON
files describing a set of images.

@author: Hugo Sousa (hugosousa@dcc.ufmg.br)
'''


from bs4 import BeautifulSoup
from contextlib import closing
from datetime import date, timedelta
from time import sleep
from random import uniform
from zlib import decompress, MAX_WBITS

import urllib.request  #Python 3
#from urllib2 import urlopen  #Python 2.7
#try: #python3
#    from urllib.request import urlopen
#except: #python2
#    from urllib2 import urlopen
#    import urllib2

FACT_CHECKERS = ['boatos.org', 'e-farsas.com', 'g1.globo.com/e-ou-nao-e',
                 'piaui.folha.uol.com.br/lupa', 'g1.globo.com/fato-ou-fake',
                 'oglobo.globo.com/fato-ou-fake',
                 'veja.abril.com.br/blog/me-engana-que-eu-posto',
                 'aosfatos.org']

FACT_CHECK_HISTORY = {}

TIME_PARAM = '%2Ccdr%3A1%2Ccd_min%3A1%2F1%2F0%2Ccd_max%3A&tbm='
URL = 'http://images.google.com.br/searchbyimage?image_url=' + \
      'http://www.monitor-de-whatsapp.dcc.ufmg.br/data/images/{}'

DOMAIN = 'www.google.com.br'

USER_AGENT = '''Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36'''

MONTHS = {y: (x + 1) for (x, y) in enumerate(['jan', 'fev', 'mar',
                                              'abr', 'mai', 'jun',
                                              'jul', 'ago', 'set',
                                              'out', 'nov', 'dez'])}

headers = [('User-Agent', USER_AGENT)]

opener = urllib.request.build_opener()
opener.addheaders = headers
#try: #python3
#    opener = urllib.request.build_opener()
#    opener.addheaders = headers
#except: #python2
#    #opener = urllib2.build_opener()
#    opener = ()


def process_url(url):
    '''
        Process URL assuring it has the proper format.

        @url: (string) URL.

        @return: (string) Processed URL.
    '''

    if url.find('http') < 0:
        url = 'https://' + url

    return url


def get_html(url, sleep_min, sleep_max, redirect=False):
    '''
        Get the HTML string corresponding to a particular URL.

        @url: (string) URL.
        @sleep_min: (float) Minimum amount of seconds to sleep for.
        @sleep_max: (float) Maximum amount of seconds to sleep for.
        @redirect: (bool) Indicates whether the param url will be redirected.

        @return: (string) HTML string.
    '''

    url = process_url(url)

    if redirect:
        while True:
            #try:
                with closing(opener.open(url)) as open_url:
                    redirect_url = open_url.url
                    new_url = redirect_url
                    url = process_url(new_url)
                    slow_down(sleep_min, sleep_max)
                    break
            #except:
             #   print('\t\t[-] Exception 1 occurred: %s, retrying.' %(url))
             #   slow_down(sleep_min, sleep_max)
             #   continue

    while True:
        try:
            with closing(opener.open(url)) as open_url:
                data = open_url.read()
                html = data.decode()
                slow_down(sleep_min, sleep_max)
                break
        except UnicodeDecodeError:
            with closing(opener.open(url)) as open_url:
                content_type = open_url.getheader('Content-Type')
                content_encoding = open_url.getheader('Content-Encoding')
                data = open_url.read()

                # Try to decompress content.
                if content_encoding is not None and 'gzip' in content_encoding:
                    html = decompress(data, 16 + MAX_WBITS)
                    slow_down(sleep_min, sleep_max)
                    break

                # Try to guess encoding.
                if content_type is not None and 'charset' in content_type:
                    charset = content_type.split('charset=')[1]
                    html = data.decode(charset)
                    slow_down(sleep_min, sleep_max)
                    break

            return ''
        except:
            print('\t\t[-] Exception 2 occurred: %s, retrying.' %(url))
            slow_down(sleep_min, sleep_max)
            continue

    return html


def parse_date(raw_date):
    '''
        Parse a raw date string and return a formatted date string.

        @raw_date: (string) Raw date string.

        @return: (string) Formatted date string.
    '''

    pieces = raw_date.split()

    if len(pieces) == 5:  # x de x de x
        year = int(pieces[4])
        month = MONTHS[pieces[2]]
        day = int(pieces[0])

        return date(year, month, day).isoformat()
    elif len(pieces) == 3:  # x x atrás
        offset = int(pieces[0])
        return (date.today() - timedelta(days=offset)).isoformat()
    else:  # unknown
        return ''


def get_page_sources(html):
    '''
        Get image sources on a particular page.

        @html: (string) Page HTML content.

        @return: (string list) List of sources of the image on the page.
    '''

    soup = BeautifulSoup(html, 'html.parser')

    links = [link.a.get('href')
             for link in soup.find_all(['div', 'h3'], {'class': 'r'})]

    dates = [parse_date(date.span.string.split(' - ')[1])
             if date.span is not None and date.span.string is not None else ''
             for date in soup.find_all('span', {'class': 'st'})]

    if len(links) != len(dates) - dates.count(''):
        forum_dates = soup.find_all('div', {'class': 'slp f'})

        if len(forum_dates) > 0:
            forum_dates = [parse_date(date.string.split(' - ')[0])
                           if date is not None and date.string is not None else ''
                           for date in forum_dates]

            boxes = soup.find_all('div', {'class': 'rc'})
            indexes = [True if b.find_all('div', {'class': 'slp f'}) else False
                       for b in boxes]

            index = 0
            for i, b in enumerate(indexes):
                if b and dates[i] == '':
                    if index >= len(forum_dates):
                        break

                    dates[i] = forum_dates[index]
                    index += 1

    return list(zip(links, dates))


def get_next_page(html, sleep_min, sleep_max):
    '''
        Get the HTML content for the next search result page.

        @html: (string) HTML content of current page.
        @sleep_min: (float) Minimum amount of seconds to sleep for.
        @sleep_max: (float) Maximum amount of seconds to sleep for.

        @return: (string) HTML content of next page.
    '''

    soup = BeautifulSoup(html, 'html.parser')
    next_page = soup.find_all('a', {'class': 'pn', 'id': 'pnnext'})

    if len(next_page) == 0:
        return None

    next_page_link = DOMAIN + next_page[0].get('href')
    return get_html(next_page_link, sleep_min, sleep_max)


def slow_down(sleep_min, sleep_max):
    '''
        Sleeps for awhile after each request, so the crawler looks slightly
        more human.

        @sleep_min: (float) Minimum amount of seconds to sleep for.
        @sleep_max: (float) Maximum amount of seconds to sleep for.
    '''

    sleep(uniform(sleep_min, sleep_max))


def get_sources(url, sleep_min, sleep_max, pages):
    '''
        Get all source links where the image has appeared on.

        @url: (string) HTML of the first result page for the image.
        @sleep_min: (float) Minimum amount of seconds to sleep for.
        @sleep_max: (float) Maximum amount of seconds to sleep for.
        @pages: (int) Number of search result pages to go through.

        @return: ((string, string) list) List of all the source links where
            the image has appeared on.
    '''

    html = get_html(url, sleep_min, sleep_max, True)
    sources = []

    en_matching = 'Pages that include matching image'
    pt_matching = 'Páginas que incluem imagens correspondentes'

    matching_string = en_matching
    # Only look for links where the image has appeared on.
    if html.find(pt_matching) != -1:
        matching_string = pt_matching
    html = html[html.find(matching_string):]

    page = 1
    while True:  # Look for other sources in the rest of the result pages.
        print('\t\t[+] Search result page {}'.format(page))
        page += 1
        if page > pages:
            break

        sources += get_page_sources(html)
        html = get_next_page(html, sleep_min, sleep_max)

        if html is None:
            break

    return sources


def generate_links(imgs_data):
    '''
        Generate Google Search by Image links.

        @imgs_data: (dict) JSON dict with images data.

        @return: (dict) Dict with the Google Search by Image links.
    '''

    links = {}

    for img_n in imgs_data:
        links[img_n] = URL.format(imgs_data[img_n]['imageID'])

    return links



def generate_search_url(url):
    '''
        Generate Google Search by Image links.

        @imgs_data: (string) URL of the images searched.

        @return: String with the Google Search by Image link.
    '''

    link = 'https://www.google.com/searchbyimage?image_url='+url

    return link


def is_fact_checked(sources):
    '''
        Checks if a particular image was fact checked.

        @sources: ((string, string) list) List of all the source links where
            the image has appeared on.

        @return: (bool) True, iff, the image was fact checked.
    '''

    links = set([s[0] for s in sources])
    return any(f in l for f in FACT_CHECKERS for l in links)


def check_boatos(link, sleep_min, sleep_max):
    '''
        Check boatos.org judgment about a content.

        @link: (string) Link to content.
        @sleep_min: (float) Minimum amount of seconds to sleep for.
        @sleep_max: (float) Maximum amount of seconds to sleep for.

        @return: (bool) True iff the content was considered true.
    '''

    # Check if link is root.
    split = link.split('//')
    if len(split) >= 2:
        split = split[1].split('/')

        if len(split) >= 2:
            if split[1] == '' or split[1] == 'wp-content':
                return None

            if 'boatos.org' not in split[0]:
                return None

    # In case it's not root
    html = get_html(link, sleep_min, sleep_max)

    if '#boato' in html:
        return False

    return None


def check_efarsas(link, sleep_min, sleep_max):
    '''
        Check e-farsas judgment about a content.

        @link: (string) Link to content.
        @sleep_min: (float) Minimum amount of seconds to sleep for.
        @sleep_max: (float) Maximum amount of seconds to sleep for.

        @return: (bool) True iff the content was considered true.
    '''

    # Check if link is root or blog.
    split = link.split('//')
    if len(split) >= 2:
        split = split[1].split('/')

        if len(split) >= 2:
            if split[1] == '' or split[1] == 'blog':
                return None

    if 'e-farsas.com/secoes' in link:
        return None

    html = get_html(link, sleep_min, sleep_max)
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find_all('span', {'class': 'mvp-post-cat left'})

    if len(title) > 0 and title[0].string is not None:
        tag = title[0].string.lower()

        if tag == 'falso':
            return False

    return None


def check_e_ou_nao_e(link, sleep_min, sleep_max):
    '''
        Check G1 É ou não É judgment about a content.

        @link: (string) Link to content.
        @sleep_min: (float) Minimum amount of seconds to sleep for.
        @sleep_max: (float) Maximum amount of seconds to sleep for.

        @return: (bool) True iff the content was considered true.
    '''

    # Check if link is root.
    split = link.split('//')
    if len(split) >= 2:
        split = split[1].split('/')

        if len(split) <= 2:
            return None

    html = get_html(link, sleep_min, sleep_max)
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find_all('h1', {'class': 'content-head__title'})

    if len(title) > 0:
        title = title[0].string.lower()
        return 'é verdade!' in title

    return None


def check_lupa(link, sleep_min, sleep_max):
    '''
        Check Lupa judgment about a content.

        @link: (string) Link to content.
        @sleep_min: (float) Minimum amount of seconds to sleep for.
        @sleep_max: (float) Maximum amount of seconds to sleep for.

        @return: (bool) True iff the content was considered true.
    '''

    # Check if link is root.
    split = link.split('//')
    if len(split) >= 2:
        split = split[1].split('/')

        if len(split) <= 2:
            return None

    html = get_html(link, sleep_min, sleep_max)
    soup = BeautifulSoup(html, 'html.parser')
    post = soup.find_all('div', {'class': 'post-inner'})

    if len(post) > 0:
        post = post[0]
        tag_false = post.find_all('div', {'class': 'etiqueta etiqueta-7'})
        tag_true = post.find_all(
            'div', {'class': ['etiqueta etiqueta-1', 'etiqueta etiqueta-2']})

        return len(tag_true) > len(tag_false)

    return None


def check_fato_ou_fake(link, sleep_min, sleep_max):
    '''
        Check G1 Fato ou Fake judgment about a content.

        @link: (string) Link to content.
        @sleep_min: (float) Minimum amount of seconds to sleep for.
        @sleep_max: (float) Maximum amount of seconds to sleep for.

        @return: (bool) True iff the content was considered true.
    '''

    # Check if link is root.
    split = link.split('//')
    if len(split) >= 2:
        split = split[1].split('/')

        if len(split) <= 2:
            return None

    html = get_html(link, sleep_min, sleep_max)
    soup = BeautifulSoup(html, 'html.parser')

    if 'oglobo.globo.com' in link:  # O Globo
        title = soup.find_all('h1', {'class': 'article__title'})
    else:  # G1
        title = soup.find_all('h1', {'class': 'content-head__title'})

    if len(title) > 0:
        title = title[0].string.lower()

        if '#fato' in title and '#fake' in title:
            return None
        elif '#fato' in title:
            return True
        elif '#fake' in title:
            return False

    return None


def check_aos_fatos(link, sleep_min, sleep_max):
    '''
        Check Aos Fatos judgment about a content.

        @link: (string) Link to content.
        @sleep_min: (float) Minimum amount of seconds to sleep for.
        @sleep_max: (float) Maximum amount of seconds to sleep for.

        @return: (bool) True iff the content was considered true.
    '''

    # Check if link is root or blog.
    split = link.split('//')
    if len(split) >= 2:
        split = split[1].split('/')

        if len(split) >= 2:
            if split[1] == '':
                return None

    html = get_html(link, sleep_min, sleep_max)
    soup = BeautifulSoup(html, 'html.parser')
    tags = [cap.string.lower()
            if cap.string is not None else None
            for cap in soup.find_all('figcaption')]

    return tags.count('verdadeiro') > tags.count('falso')


def get_fact_check(sources, sleep_min, sleep_max):
    '''
        Check if a particular image was fact checked true or false.

        @sources: ((string, string) list) List of sources where the image has
            appeared.
        @sleep_min: (float) Minimum amount of seconds to sleep for.
        @sleep_max: (float) Maximum amount of seconds to sleep for.

        @return: (dict) Dictionary with the fact checkers and their fact check
            judgment.
    '''

    global FACT_CHECK_HISTORY

    fact_checks = {}
    check_functions = {
        'boatos.org': check_boatos,
        'e-farsas.com': check_efarsas,
        'g1.globo.com/e-ou-nao-e': check_e_ou_nao_e,
        'piaui.folha.uol.com.br/lupa': check_lupa,
        'g1.globo.com/fato-ou-fake': check_fato_ou_fake,
        'oglobo.globo.com/fato-ou-fake': check_fato_ou_fake,
        'aosfatos.org': check_aos_fatos
    }

    for source, _ in sources:
        for f in check_functions:
            if f in source and fact_checks.get(f, None) is None:
                if source in FACT_CHECK_HISTORY:
                    fact_checks[f] = FACT_CHECK_HISTORY[source]
                else:
                    fact_checks[f] = check_functions[f](
                        source, sleep_min, sleep_max)
                    FACT_CHECK_HISTORY[source] = fact_checks[f]

                continue

    return fact_checks
