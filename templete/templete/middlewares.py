# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random
import requests
import json
# from templete.models import ProxyModel
from twisted.internet.defer import DeferredLock

from templete.models import ProxyModel


class UserAgentDownloaderMiddleware(object):
    USERAGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/44.0.2403.155 Safari/537.36'
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 10.6; Windows NT 6.1; Trident/5.0; InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 2.0.50727) 3gpp-gba UNTRUSTED/1.0',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/4.0; InfoPath.2; SV1; .NET CLR 2.0.50727; WOW64)',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A',
        'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25',
        'Mozilla/5.0 (X11; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0',
        'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:63.0) Gecko/20100101 Firefox/63.0',
        'Mozilla/5.0 (X11; Linux i586; rv:63.0) Gecko/20100101 Firefox/63.0',
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
    ]

    def process_request(self, request, spider):
        user_agent = random.choice(self.USERAGENTS)
        request.headers['User-Agent'] = user_agent


# 随机代理Ipclass
class IPProxyDownloaderMiddleware(object):
    PROXY_URL = "http://webapi.http.zhimacangku.com/getip?num=1&type=2&pro=&city=0&yys=0&port=1&time=1&ts=1&ys=0&cs=1&lb=1&sb=0&pb=45&mr=1&regions="

    # 初始化函数
    def __init__(self):
        super(IPProxyDownloaderMiddleware, self).__init__()
        self.current_proxy = None
        self.lock = DeferredLock()

    # 处理请求
    def process_request(self, request, spider):
        # 如果请求头中不包含代理，则请求代理
        if 'proxy' not in request.meta or self.current_proxy.is_expiring:
            # 请求代理
            self.update_proxy()
        request.meta['proxy'] = self.current_proxy.proxy

    # 处理响应
    def process_response(self, request, response, spider):
        if response.status != 200 or "captcha" in response.url:
            # 如果IP没有被拉黑，则
            if not self.current_proxy.blacked:
                self.current_proxy.blacked = True
            print("%s这个Ip被拉入黑名单了" % self.current_proxy.ip)
            self.update_proxy()
            return request
        return response

    # 更新代理
    def update_proxy(self):
        self.lock.acquire()
        if not self.current_proxy or self.current_proxy.is_expiring or self.current_proxy.blacked:
            response = requests.get(self.PROXY_URL)
            text = response.text
            print("重新获取了一个代理：", text)
            # print(text)
            results = json.loads(text)
            if len(results['data']) > 0:
                data = results['data'][0]
                proxy_model = ProxyModel(data)
                self.current_proxy = proxy_model
        self.lock.release()
