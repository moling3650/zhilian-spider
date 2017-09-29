
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date    : 2017-09-29 10:33:20
# Author  : moling3650
import time
import random
import requests
from bs4 import BeautifulSoup

HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'}

class ZhiLianSpider(object):
    def __init__(self, keyword, job_location='全国'):
        self.keyword = keyword
        self.job_location = job_location
        self.search_URL = 'http://sou.zhaopin.com/jobs/searchresult.ashx?kw=%s&jl=%s' % (keyword, job_location)
        self.session = requests.Session()
        self.session.headers = HEADERS


    def _setNextSearchURL(self, soup):
        next_page = soup.select_one('.next-page')        
        self.search_URL = next_page.attrs['href'] if (next_page and next_page.has_attr('href')) else ''


    def getJobURLs(self):
        r = self.session.get(self.search_URL, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        self._setNextSearchURL(soup)
        return (el.attrs['href'] for el in soup.select('.zwmc a[href^="http://jobs.zhaopin.com/"]'))



if __name__ == '__main__':
    spider = ZhiLianSpider('前端', job_location='深圳')
    while spider.search_URL:
        time.sleep(random.randint(1, 3))
        print(spider.search_URL)
        spider.getJobURLs()
