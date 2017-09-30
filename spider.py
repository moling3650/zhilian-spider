#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date    : 2017-09-29 10:33:20
# Author  : moling3650
import re
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


    def _getJobURLs(self):
        r = self.session.get(self.search_URL, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        self._setNextSearchURL(soup)
        return (el.attrs['href'] for el in soup.select('.zwmc a[href^="http://jobs.zhaopin.com/"]'))

    def _getDataByURL(self, url):
        data = {}
        try: 
            r = self.session.get(url, timeout=10)
            soup = BeautifulSoup(r.text, 'html.parser')
            data['id'] = re.compile("http.+/|\.htm.*").sub('', url)
            data['职位链接'] = url
            data['职位名称'] = soup.select_one('.fl > h1').text.strip()
            data['公司名称'] = soup.select_one('.fl > h2 > a').text.strip()
            data['公司福利'] = '/'.join(el.text.strip() for el in soup.select('.welfare-tab-box > span'))
            tab = soup.select_one('.tab-inner-cont')
            data['职位描述'] =  '\n'.join(p.text.strip() for p in tab.find_all('p'))
            data['详细工作地点'] = tab.find('h2').contents[0].strip()
            fields = (el.text.strip().replace('：', '') for el in soup.select('.terminal-ul li > span'))
            values = (el.text.strip() for el in soup.select('.terminal-ul li > strong'))
            data.update(dict(zip(fields, values)))
        except e:
            print('timeout: %s' % url)
            
        return data


    def main(self):
        urls = self._getJobURLs()
        for url in urls: 
            time.sleep(random.randint(3, 5))
            data = self._getDataByURL(url)
            if data:
                print(data['职位描述'])


if __name__ == '__main__':
    spider = ZhiLianSpider('前端', job_location='深圳')
    spider.main()
