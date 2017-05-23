# encoding: utf-8
from scrapy.http import Request
import re
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
from datetime import datetime
from m1905.items import M1905Item
import redis
import random
from m1905.settings import *


class movie_spider(scrapy.Spider):
    
    
    name = 'movie_spider'
    allowed_domains = ["1905.com"]
    pool = redis.ConnectionPool(host=Redis_Host, port=Redis_port, db=Redis_db)
    client = redis.Redis(connection_pool=pool)
    
    def start_requests(self):
        redis_Keys = self.client.keys()
        redis_urls_nums = len(redis_Keys)
        i = 0
        already_num = set()
        while i<redis_urls_nums:
            movie_elem = random.choice(redis_Keys)
            if movie_elem in already_num:
                continue
            else:
                already_num.add(movie_elem)
                i=i+1
                redis_crawled = self.client.hget(movie_elem, "crawled")
                if redis_crawled == 'False':
                    redis_urls = self.client.hget(movie_elem, "movie_url")
                   
                    yield Request(redis_urls, self.parse)
                else:
                    continue
    
    def parse(self, response):
        try:
            item = M1905Item()
            info = BeautifulSoup(response.text, 'lxml')
            item['info_id'] = response.url.split('/')[-2]
            item['name'] = info.find('a',class_='laGrayS_f').get_text()
            sub_info = info.find('ol',class_='movStaff line_BSld')
            try:
                item['director']= sub_info.find('li',class_='g6e_f line-h20').find('a',class_='laBlueS_f pr06').get_text()
            except:
                item['director'] = ''
            try:
                item['actor'] = sub_info.find('li',class_='laGrayQdd_f line-h20').get_text().replace(u'主演:\n','').replace(u'/',' ')
            except:
                item['actor'] = ''
            try:
                type_temp = sub_info.find('div',class_='golbalTag').get_text().replace(u' 类型/地区:\n','').split(' ')

                i = 1
                item['type']=''
                while type_temp[i] !='':
                    item['type'] += type_temp[i]+' '
                    i=i+1
                i=i+1
                item['country']=''
                while type_temp[i] !='':
                    item['country'] += type_temp[i]+' '
                    i=i+1
            except:
                item['type'] = ''
                item['country'] = ''
            try:
                item['date'] = sub_info.find_all('li',class_=' g6e_f line-h20')[-1].get_text().replace(u'上映日期:','').split(' ')[1]
            except:
                item['date'] = ''
            try:
                item['gernic'] = sub_info.find('li',class_='mdbTags g6e_f').get_text().replace(u'电影基因:','').replace('\n','')
            except:
                item['gernic'] = ''
            try:
                item['score'] = info.find('span', class_="score").get_text()
            except:
                item['score'] = ''
            
            item['time'] =  datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            return item
        except Exception, e:
            print e.message
