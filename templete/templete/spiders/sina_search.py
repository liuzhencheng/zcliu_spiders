import datetime

import requests
import scrapy
import re


from templete.Utils import utilsModel
from templete.items import TempleteItem
from templete.models import DateFormatHelper


class SougouSearchSpider(scrapy.Spider):
    name = 'sina_search'
    utils = utilsModel()
    allowed_domains = ['search.sina.com.cn']
    keyIndex = 0
    keyword, keywordCount = utils.get_keyword(keyIndex)
    page = 1
    base_url = 'https://search.sina.com.cn/?q={}&c=news&time=&a=&page={}'.format(
        keyword, page)
    start_urls = [base_url]

    def parse(self, response):
        item = TempleteItem()
        try:
            elements = response.xpath('//div[@class="box-result clearfix"]')
            # print(elements)
            for each in elements:
                Url = each.xpath('./h2/a/@href | ./div/h2/a/@href').extract()
                # print(seedUrl)
                seedUrl = str(Url).replace('\']', '').replace('[\'', '')
                # print(url)
                if seedUrl is not None:
                    pagehtml = requests.get(url=seedUrl)
                    # print(str(pagehtml.text))
                else:
                    return None
                title = ''.join(each.xpath('./h2/a//text() | ./div/h2/a//text()').extract()).strip()
                # print(title)
                sources = each.xpath('./h2/span/text() | ./div/h2/span/text()').extract()
                source = ''.join(re.findall(r'[\u4e00-\u9fa5]', str(sources)))
                # print(source)
                time = ''.join(re.findall(r'\d{1,4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2}', str(sources)))
                releaseTime = time
                # 时间格式处理
                # releaseTime, releaseTimeLong = DateFormatHelper.js_To_Date(time)
                # print(js_time)
                content = ''.join(each.xpath('./div/p//text()').extract()).strip()
                # print(content)

                item['Id'] = '1801999'
                item['indexFlag'] = False
                item['originweb'] = '新浪新闻搜索'
                item['seedUrl'] = seedUrl
                item['urlId'] = self.utils.encrypt_url(str(seedUrl))
                item['title'] = title
                item['content'] = content
                item['source'] = source
                item['type'] = '新闻'
                item['releaseTime'] = releaseTime
                item['url_id'] = '1000'
                item['url_key'] = '1801999'
                item['pagehtml'] = str(pagehtml)
                # item['releaseTimeLong'] = releaseTimeLong
                item['collectionTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                yield item

            if self.page < 2:
                self.page = self.page + 1
                yield scrapy.Request(
                    'https://search.sina.com.cn/?q={}&c=news&time=&a=&page={}'.format(
                        self.keyword, self.page))
            else:
                if self.keyIndex < self.keywordCount:
                    # 如果当前关键词爬取结束，则发送爬取下一个关键词的请求
                    self.page = 1
                    self.keyIndex = self.keyIndex + 1
                    self.keyword, _ = self.utils.get_keyword(self.keyIndex)
                    yield scrapy.Request(
                        'https://search.sina.com.cn/?q={}&c=news&time=&a=&page={}'.format(
                            self.keyword, self.page))
        except Exception as e:
            print(e)
