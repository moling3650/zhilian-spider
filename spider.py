#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date    : 2017-09-29 10:33:20
# Author  : moling3650
import re
import time
import random
import pymysql
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
        try:
            r = self.session.get(self.search_URL, timeout=10)
        except:
            print('爬取列表页失败: %s' % self.search_URL)
            return []
        soup = BeautifulSoup(r.text, 'html.parser')
        self._setNextSearchURL(soup)
        return (el.attrs['href'] for el in soup.select('.zwmc a[href^="http://jobs.zhaopin.com/"]'))


    def _getDataByURL(self, url):
        try: 
            r = self.session.get(url, timeout=10)
        except:
            print('请求超时: %s' % url)
            return None

        data = {}
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
        return data


    def _saveToDatabase(self, data):
        if not data:
            return

        connection = pymysql.connect(host='localhost',
                                     user='zl',
                                     password='zl-data',
                                     db='zhilian',
                                     charset='utf8')
        try:
            with connection.cursor() as cursor:
                sql = 'DELETE FROM `jobs` WHERE `id` = %s'
                cursor.execute(sql, (data['id'],))
                sql = 'INSERT INTO `jobs` (%s) VALUES (%s)' % ( ','.join('`%s`' % k for k in data.keys()), ','.join(['%s'] * len(data)))
                cursor.execute(sql, tuple(data.values()))
            connection.commit()
            print('储存成功: %s' % data['职位链接'])
        except:
            print('储存失败: %s' % data['职位链接'])
        finally:
            connection.close()


    def crawl(self):
        while self.search_URL:
            print('现在开始爬取列表页: %s' % self.search_URL)
            for url in self._getJobURLs(): 
                time.sleep(random.randint(1, 5))
                data = self._getDataByURL(url)
                self._saveToDatabase(data)


if __name__ == '__main__':
    spider = ZhiLianSpider('前端', job_location='深圳')
    spider.crawl()
