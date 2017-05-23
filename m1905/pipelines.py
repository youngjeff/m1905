# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from m1905.db_util import m1905_movies,DB_Util
from m1905.items import M1905Item
import redis
from m1905.settings import *

class M1905Pipeline(object):
    pool = redis.ConnectionPool(host=Redis_Host, port=Redis_port, db=Redis_db)
    client = redis.Redis(connection_pool=pool)
    def open_spider(self,spider):
        DB_Util.init_db()

    def process_item(self,item,spider):

        if not item['info_id']:
            raise DropItem('item info_id is null.{0}'.format(item))
        else:
            try:
                session = DB_Util.get_session()
                moive = m1905_movies()
                moive.info_id = item['info_id']
                moive.name = item['name']
                moive.director = item['director']
                moive.actor = item['actor']
                moive.type = item['type']
                moive.country = item['country']
                moive.date = item['date']
                moive.gernic = item['gernic']
                moive.score = item['score']
                moive.time = item['time']
                session.add(moive)
                self.client.hset(moive.info_id, "crawled", "True")
                session.commit()
            except:
                print "the data is already exist!"
        return item
