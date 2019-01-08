import datetime

import requests
import scrapy
import re

from scrapy import Request

from templete.Utils import utilsModel
from templete.items import TempleteItem
from templete.models import DateFormatHelper


class SougouSearchSpider(scrapy.Spider):
    name = 'fazhi_yunnan'
    # utils = utilsModel()
    allowed_domains = ['fazhi.yunnan.cn']
    # keyIndex = 0
    # keyword, keywordCount = utils.get_keyword(keyIndex)
    # page = 1
    urls = ['fazhixinwen',
            'yunnanzhengfa',
            'tianpingzhiguang',
            'jianchafengcai',
            'yunlingjingfang',
            'bianfangweishi',
            'jtaq',
            'yunlingsenjing',
            'flfw',
            'dajiangleiwai']
    keyIndex = 0
    base_url = 'http://fazhi.yunnan.cn//{}/'.format(urls[keyIndex])
    start_urls = [base_url]
    print(start_urls)


    def parse(self, response):
        elements = response.xpath("//div[@class='xx ohd clear']/div[@class='xlayer02 yh ohd clear']")
        # print(elements)
        for each in elements:
            url = each.xpath("./span[1]/a/@href").extract()[0]
            seedUrl = ' http:'+url
            # print(seedUrl)
            if seedUrl is not None:
                pagehtml = requests.get(url=seedUrl)
                # print(pagehtml.text)
            else:
                return None
            title = each.xpath("./span[1]/a/text()").extract()[0]
            # print(title)
            time = each.xpath("./span[2]/text()").extract()[0]
            # print(time)
            releaseTime = time

            # 下一级请求
            yield scrapy.Request(url=seedUrl, callback=self.parse_detail, meta={"info": (title, releaseTime)})

        # 发送下一页请求
        # urlnext = response.xpath("//div[@class='pageChange']/a[3]/@href").extract()[0]
        # yield scrapy.Request(url="http://www.kmust.edu.cn" + urlnext, callback=self.parse)

        yield scrapy.item

    def parse_detail(self, response):
        item = TempleteItem()
        title, releaseTime = response.meta["info"]
        seedUrl  = response.seedUrl
        source = response.xpath('//div[@class="xx ohd clear"]/div/span[2]/span[2]').extract()[0]
        print(source)
        content = response.xpath('').extract()[0]



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
        yield item
        #
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
