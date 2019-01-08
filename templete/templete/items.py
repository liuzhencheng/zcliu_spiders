# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TempleteItem(scrapy.Item):
    # 原模板id
    Id = scrapy.Field()
    # 存放URL
    seedUrl = scrapy.Field()
    # 存放加密之后的url地址
    urlId = scrapy.Field()
    # 存放新闻标题
    title = scrapy.Field()
    # 存放新闻内容
    content = scrapy.Field()
    # 存放类型(网站，微信等)
    type = scrapy.Field()
    # source 存放该条新闻的网站
    source = scrapy.Field()
    # 存放发布时间
    releaseTime = scrapy.Field()
    # 存放发布时间的long类型，便于排序
    releaseTimeLong = scrapy.Field()
    # 存放入库时间
    collectionTime = scrapy.Field()
    # 原始网页
    originweb = scrapy.Field()
    # 是否索引
    indexFlag = scrapy.Field()
    # 网页的html代码
    pagehtml = scrapy.Field()
    url_id = scrapy.Field()
    url_key = scrapy.Field()