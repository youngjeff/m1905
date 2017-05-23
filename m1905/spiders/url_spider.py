# encoding: utf-8
from scrapy.http import Request
import redis
import random
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
from m1905.settings import *
from m1905.items import M1905Item

class url_yspider(scrapy.Spider):
    try:
        name = 'url_spider'
        allowed_domains = ['1905.com']
        pool = redis.ConnectionPool(host=Redis_Host,port=Redis_port,db=Redis_db)
        client = redis.Redis(connection_pool=pool)
    except Exception, e:
        print e.message
    def start_requests(self):
        i = 1
        already_num = set()
        while i<11000:
            random_num = random.choice(range(11000))
            if not random_num in already_num:
                already_num.add(random_num)
                url = ("http://www.1905.com/mdb/film/list/o0d0p%s.html" % str(random_num))
                i = i + 1
                yield Request(url,self.parse)
        print "数据获取完毕"

    def parse(self, response):
        urls = BeautifulSoup(response.text,'lxml').find('ul',class_='inqList pt18').find_all('li','fl')
        for url in urls:
            try:
                movie_url = 'http://www.1905.com'+url.find('a')['href']
                movie_id = movie_url.split('/')[-2]

                if not self.client.exists(movie_id):
                    self.client.hset(movie_id,'movie_url',movie_url)
                    self.client.hset(movie_id,'crawled','False')
                    print "insert one data"
                else:
                    print "the data is already exist"
            except Exception, e:
                print e.message