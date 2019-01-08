import pymongo
import hashlib
import requests
import json


# 工具类，包括数据库读取等
from pymongo import MongoClient

from templete import settings


class utilsModel(object):
    def __init__(self) -> object:
        super(utilsModel, self).__init__()
        # self.client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        # self.mydb = self.client['db_templete']

        # 建立MONGODB数据库链接
        uri = 'mongodb://zhdb:541%40kmust4liip@222.197.219.11:27017/zhdb_FaYun'
        self.client = MongoClient(uri)
        self.mydb = self.client['zhdb_FaYun']

    # 读取数据
    # collectionName为表名
    # search为查询的字典格式为{"key":"value"}
    def getCollection(self, collectionName, search):
        collection = self.mydb[collectionName]
        items = collection.find()
        for item in items:
            print(item)
            yield item

    # 对字符串进行加密
    def encrypt_url(self, str):
        str = str.encode('utf-8')
        hash = hashlib.md5()
        hash.update(str)
        return hash.hexdigest()

    # 判断urlid在表中是否存在
    def exists_urlid(self, urlid):
        collection = self.mydb['urlid_Collection']
        items = collection.find({"urlid": urlid})
        return items.count()

    def get_keyword(self, i):
        key_list = ['麒麟区', '曲靖市', '昆明' '麒麟区法院', '富源县', '麒麟区人民法院', '宣威市', '陆良县', '会泽县']
        if i < len(key_list):
            return key_list[i], len(key_list)
        else:
            return key_list[0], len(key_list)
