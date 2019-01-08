# -*- coding: utf-8 -*-
import datetime

import requests
import scrapy
import re

from templete.Utils import utilsModel
from templete.items import TempleteItem
from templete.models import DateFormatHelper


class SougouSearchSpider(scrapy.Spider):
    name = 'sougou_search'
    utils = utilsModel()
    allowed_domains = ['news.sogou.com']
    keyIndex = 0
    keyword, keywordCount = utils.get_keyword(keyIndex)
    # print(keyword)
    page = 1
    base_url = 'https://news.sogou.com/news?mode=1&query={}&page={}'.format(
        keyword, page)
    start_urls = [base_url]

    def parse(self, response):
        item = TempleteItem()
        try:
            elements = response.xpath('//div[@class="vrwrap"]/div')
            for each in elements:
                # 获取url
                Url = each.xpath("./h3/a/@href").extract_first()
                # print(seedUrl)
                if Url == None:
                    print('无效网页！！！')
                seedUrl = str(Url).replace('\']', '').replace('[\'', '')
                # print(seedUrl)
                if seedUrl is not None:
                    pagehtml = requests.get(url=seedUrl)
                    # print(str(pagehtml.text))
                else:
                    return None

                # 获取标题
                if seedUrl == None:
                    pass
                else:
                    title = ''.join(each.xpath('./h3/a//text()').extract()).strip()
                    # print(title)

                # 获取来源
                if seedUrl == None:
                    pass
                else:
                    sources = each.xpath('.//div/div/p[1]/text()').extract()
                    source = ''.join(re.findall(r'[\u4e00-\u9fa5]', str(sources))).strip()

                # 获取时间
                if seedUrl == None:
                    pass
                else:
                    js_time = re.findall(r'\d{1,4}-\d{1,2}-\d{1,2}',
                                         str(each.xpath('.//div/div/p[1]/text()').extract()))
                    releaseTime = str(js_time).replace('[\'', '').replace('\']', '')
                    # print(releaseTime)
                    # 处理时间 将字符串传入一个函数，来判断时间，返回时间格式
                    # 时间格式处理
                    # releaseTime, releaseTimeLong = DateFormatHelper.js_To_Date(js_time)

                # 获取内容
                if seedUrl == None:
                    pass
                else:
                    content = ''.join(each.xpath('.//p[2]/span//text()').extract()).strip()
                    # print(content)

                item['Id'] = '1801999'
                item['indexFlag'] = False
                item['originweb'] = '搜狗新闻搜索'
                item['seedUrl'] = seedUrl
                item['urlId'] = self.utils.encrypt_url(str(seedUrl))
                item['title'] = title
                item['content'] = content
                item['source'] = source
                item['type'] = '新闻'
                item['releaseTime'] = releaseTime
                # item['releaseTimeLong'] = releaseTimeLong
                item['url_id'] = '1000'
                item['url_key'] = '1801999'
                item['pagehtml'] = str(pagehtml)
                item['collectionTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                yield item

            # # 发送下一页请求
            # if len(response.xpath('//*[@id="pagebar_container"]/a[@id="sogou_next"]/@href')) == 0:
            #     print("当前网站爬取结束！！！")
            # else:
            #     urlnext_page = response.xpath('//*[@id="pagebar_container"]/a[@id="sogou_next"]/@href').extract()[0]
            #     yield scrapy.Request(url="https://news.sogou.com/news" + urlnext_page, callback=self.parse)

            if self.page < 2:
                self.page = self.page + 1
                yield scrapy.Request(
                    'https://news.sogou.com/news?mode=1&query={}&page={}'.format(
                        self.keyword, self.page))
            else:
                if self.keyIndex < self.keywordCount:
                    # 如果当前关键词爬取结束，则发送爬取下一个关键词的请求
                    self.page = 1
                    self.keyIndex = self.keyIndex + 1
                    self.keyword, _ = self.utils.get_keyword(self.keyIndex)
                    print(self.keyword)
                    yield scrapy.Request(
                        'https://news.sogou.com/news?mode=1&query={}&page={}'.format(
                            self.keyword, self.page))


        except Exception as e:
            print(e)
