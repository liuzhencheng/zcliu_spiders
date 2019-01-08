# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
import pymongo
from pymongo import MongoClient

from templete.Utils import utilsModel



class TempletePipeline(object):
    utlis = utilsModel()

    def __init__(self):
        host = settings["MONGODB_HOST"]
        port = settings["MONGODB_PORT"]
        dbname = settings["MONGODB_DBNAME"]
        user = settings["MONGODB_USER"]
        password = settings["MONGODB_PASS"]

        # 创建MONGODB数据库链接
        # client = pymongo.MongoClient(host=host, port=port)
        uri = 'mongodb://' + user + ':' + password + '@' + host + ':' + port + '/' + dbname
        # uri = 'mongodb://zhdb:541%40kmust4liip@222.197.219.11:27017/zhdb_FaYun'
        client = MongoClient(uri)

        # 指定数据库
        mydb = client[dbname]
        # 存放数据的数据库表名
        self.collection = mydb['news']
        self.collection_url = mydb['urlid_Collection']
        # doc = self.collection.find()

    def process_item(self, item, spider):
        data = dict(item)
        # 不存在则插入
        if self.utlis.exists_urlid(item['urlId']) == 0:
            # 如果新闻标题不为空，则判断是否在urlid_Collection表中是否存在
            # 读取urlid_Collection表，然后判断当前的item['urlid']是否存在
            self.collection.insert(data)
            self.collection_url.insert({"urlid": item['urlId']})
        else:
            print("已存在")
        return item
