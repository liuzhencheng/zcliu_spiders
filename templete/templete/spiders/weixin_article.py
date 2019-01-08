# -*- coding: utf-8 -*-
import requests
import scrapy
from datetime import datetime

from templete.Utils import utilsModel
from templete.items import TempleteItem
from templete.models import DateFormatHelper


class WeixinArticleSpider(scrapy.Spider):
    utils = utilsModel()
    name = 'weixin_article'
    # allowed_domains = ['weixin.sogou.com']
    keyIndex = 0
    keyword, keywordCount = utils.get_keyword(keyIndex)
    print(keyword)
    page = 1
    base_url = 'https://weixin.sogou.com/weixin?type=2&query={}&ie=utf8&s_from=input&_sug_=n&_sug_type_=1&page={}'.format(
        keyword, page)
    start_urls = [base_url]

    def parse(self, response):
        # 获取所有的标题，然后拼接为字符串
        elements = response.xpath("//div[@class='txt-box']")
        item = TempleteItem()
        for each in elements:
            # 获取标题
            title = ""
            content = ""
            Url = each.xpath("./h3/a/@href").extract()[0]
            seedUrl = str(Url).replace('\']', '').replace('[\'', '')
            # print(url)
            if seedUrl is not None:
                pagehtml = requests.get(url=seedUrl)
                # print(str(pagehtml.text))
            else:
                return None
            source = each.xpath("./div[@class='s-p']/a/text()").extract()[0]
            for sub_title in each.xpath("./h3/a//text()").extract():
                sub_title = sub_title.strip()
                title = title + sub_title
            # 获取内容
            for sub_content in each.xpath("./p//text()").extract():
                sub_content = sub_content.strip()
                content = content + sub_content
            # 处理时间 将字符串传入一个函数，来判断时间，返回时间格式
            js_time = each.xpath(".//span[@class='s2']/script/text()").extract()[0]
            # print(js_time)
            # 时间格式处理
            releaseTime, releaseTimeLong = DateFormatHelper.js_To_Date(js_time)
            item['Id'] = '1801999'
            item['indexFlag'] = False
            item['originweb'] = '搜狗微信搜索'
            item['seedUrl'] = seedUrl
            item['urlId'] = self.utils.encrypt_url(str(seedUrl))
            item['title'] = title
            item['content'] = content
            item['source'] = source
            item['type'] = '微信'
            item['releaseTime'] = releaseTime
            item['url_id'] = '1000'
            item['url_key'] = '1801999'
            item['pagehtml'] = str(pagehtml)
            item['releaseTimeLong'] = releaseTimeLong
            item['collectionTime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            yield item
        if self.page < 2:
            self.page = self.page + 1
            yield scrapy.Request(
                'https://weixin.sogou.com/weixin?type=2&query={}&ie=utf8&s_from=input&_sug_=n&_sug_type_=1&page={}'.format(
                    self.keyword, self.page))
        else:
            if self.keyIndex < self.keywordCount:
                # 如果当前关键词爬取结束，则发送爬取下一个关键词的请求
                self.page = 1
                self.keyIndex = self.keyIndex + 1
                self.keyword, _ = self.utils.get_keyword(self.keyIndex)
                yield scrapy.Request(
                    'https://weixin.sogou.com/weixin?type=2&query={}&ie=utf8&s_from=input&_sug_=n&_sug_type_=1&page={}'.format(
                        self.keyword, self.page))
