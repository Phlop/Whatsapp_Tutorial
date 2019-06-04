#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Main piece of code.
# In here you can find the function main of the crawler.


import re
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from scrapy.selector import Selector


OUT_FOLDER = './out/'
CONFIG_FILES_PATH = './config_files/'
whatsapp_invite_regex = r"(?i)(chat\.whatsapp\.com\/)(invite\/)?([a-zA-Z0-9]{22})"



class WhatsappCrawler(scrapy.Spider):
  '''
    This is a crawler implemented using scrapy.
    This crawler seeks only for group invite links from Whatsapp on the web.
  '''

  name = 'Whatsapp-Crawler'
  
  forbidden_domains = ['verifiedloot.com',
                       'defesa.org',
                       'play.google.com',
                       'facebook.com',
                       'fb.com',
                       'chat.whatsapp.com']
  
  custom_settings = {
    # Setting a 5 seconds delay between each request.
    'DOWNLOAD_DELAY': 5,
    'AUTOTHROTTLE_ENABLED': True,
    'HTTPCACHE_ENABLED': True,
    'CONCURRENT_REQUESTS': 500,
    'COOKIES_ENABLED': False,
    'RETRY_ENABLED': False,
    'DOWNLOAD_TIMEOUT': 10,
    'CONCURRENT_REQUESTS_PER_DOMAIN': 3,
    'DEPTH_PRIORITY': 1,
    'SCHEDULER_DISK_QUEUE': 'scrapy.squeues.PickleFifoDiskQueue',
    'SCHEDULER_MEMORY_QUEUE': 'scrapy.squeues.FifoMemoryQueue',
  }

  rules = [
    Rule(
      LinkExtractor(
        canonicalize=True,
        unique=True,
        deny_domains = forbidden_domains,
      ),
      follow=True,
      callback="parse"
    )
  ]


  def start_requests(self):
    '''
      This function gets all seeds and starts the crawler.
    '''
    gseeds = []
    fseeds = open(CONFIG_FILES_PATH+'seeds', 'r')
    gseeds = fseeds.readlines()
    fseeds.close()

    for url in gseeds:
      yield scrapy.Request(url, callback=self.parse)



  def parse(self, response):
    if str(response.body).lower().find('whatsapp') == -1:
      return

    self.log('Visited: %s' % response.url)


    matches = re.findall(whatsapp_invite_regex, str(response.body))
    if len(matches):
      with open(OUT_FOLDER+'whatsapp_invite_links', 'a') as whatsapp_file:
        for match in matches:
          whatsapp_file.write("https://" + "".join(match) + '\n')

    items = []

    # In case we're scraping a google's results page, grep all results links.
    if str(response.url).lower().find('google.com') != -1:
      sel = Selector(response)
      gsearch_links_list = sel.xpath('//h3/a/@href').extract()
      gsearch_links_list = [re.search('q=(.*)&sa',n).group(1) for n in gsearch_links_list]
      gsearch_links_list = list(set(gsearch_links_list))

      for url in gsearch_links_list:
        yield response.follow(url, callback=self.parse)
    else:
      links = LinkExtractor(canonicalize=True, unique=True,
                            deny_domains=self.forbidden_domains).extract_links(response)

      for link in links:
        if str(link.url).lower().find('chat.whatsapp.com') == -1:
          yield response.follow(link.url, callback=self.parse)

