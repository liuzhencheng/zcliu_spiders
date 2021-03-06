import datetime

import requests
import scrapy
import re


from templete.Utils import utilsModel
from templete.items import TempleteItem
from templete.models import DateFormatHelper


class SougouSearchSpider(scrapy.Spider):
    name = 'wangyi_news'
    utils = utilsModel()
    allowed_domains = ['news.163.com']
    keyIndex = 0
    keyword, keywordCount = utils.get_keyword(keyIndex)
    page = 1
    # base_url = 'http://news.163.com/latest/'.format(
    #     keyword, page)
    base_url = 'http://news.163.com/latest/'
    start_urls = [base_url]

    def parse(self, response):
        # item = TempleteItem()
        try:
            elements = response.xpath('//div[@id=instantPanel""]/div[@class="cnt"]/ul/li')
            print(elements)





                # item['Id'] = '1801999'
                # item['indexFlag'] = False
                # item['originweb'] = '新浪新闻搜索'
                # item['seedUrl'] = seedUrl
                # item['urlId'] = self.utils.encrypt_url(str(seedUrl))
                # item['title'] = title
                # item['content'] = content
                # item['source'] = source
                # item['type'] = '新闻'
                # item['releaseTime'] = releaseTime
                # item['url_id'] = '1000'
                # item['url_key'] = '1801999'
                # item['pagehtml'] = str(pagehtml)
                # # item['releaseTimeLong'] = releaseTimeLong
                # item['collectionTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # yield item

            # if self.page < 2:
            #     self.page = self.page + 1
            #     yield scrapy.Request(
            #         'https://search.sina.com.cn/?q={}&c=news&time=&a=&page={}'.format(
            #             self.keyword, self.page))
            # else:
            #     if self.keyIndex < self.keywordCount:
            #         # 如果当前关键词爬取结束，则发送爬取下一个关键词的请求
            #         self.page = 1
            #         self.keyIndex = self.keyIndex + 1
            #         self.keyword, _ = self.utils.get_keyword(self.keyIndex)
            #         yield scrapy.Request(
            #             'https://search.sina.com.cn/?q={}&c=news&time=&a=&page={}'.format(
            #                 self.keyword, self.page))
        except Exception as e:
            print(e)
