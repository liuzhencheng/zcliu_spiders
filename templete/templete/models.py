# encoding:utf-8
from datetime import datetime, timedelta
import re
import time


# 处理代理IP的类
class ProxyModel(object):
    def __init__(self, data):
        self.ip = data['ip']
        self.port = data['port']
        self.expire_str = data['expire_time']
        self.blacked = False
        # 将字符串格式的过期时间，转换为日期格式
        date_str, time_str = self.expire_str.split(" ")
        year, month, day = date_str.split("-")
        hour, minute, second = time_str.split(":")
        self.expire_time = datetime(year=int(year), month=int(month), day=int(day), hour=int(hour), minute=int(minute),
                                    second=int(second))
        self.proxy = "http://{}:{}".format(self.ip, self.port)

    # 判断当前ip是否到期
    @property
    def is_expiring(self):
        now = datetime.now()
        if (self.expire_time - now) < timedelta(seconds=5):
            return True
        else:
            return False


# 时间格式化类
class DateFormatHelper(object):
    @classmethod
    def parse_time(self, s_time):
        result_time = ''
        # 1、2017-06-15
        if re.findall(r'\d{1,4}-\d{1,2}-\d{1,2}', s_time):
            result_time = time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(s_time, "%Y-%m-%d"))
        # 6天前
        elif u'天前' in s_time:
            days = re.findall(u'(\d+)天前', s_time)[0]
            result_time = (datetime.now() - timedelta(days=int(days))).strftime("%Y-%m-%d %H:%M:%S")
        # 昨天 18:03
        elif u'昨天' in s_time:
            last_time = re.findall(r'.*?(\d{1,2}:\d{1,2})', s_time)[0]
            days_ago = datetime.now() - timedelta(days=int(1))
            y_m_d = str(days_ago.year) + '-' + str(days_ago.month) + '-' + str(days_ago.day)
            _time = y_m_d + ' ' + last_time
            result_time = time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(_time, "%Y-%m-%d %H:%M"))

        # 28分钟前
        elif u'分钟前' in s_time:
            minutes = re.findall(u'(\d+)分钟', s_time)[0]
            minutes_ago = (datetime.now() - timedelta(minutes=int(minutes))).strftime("%Y-%m-%d %H:%M:%S")
            result_time = minutes_ago
        # 06-29
        elif re.findall(r'\d{1,2}-\d{1,2}', s_time) and len(s_time) <= 5:
            now_year = str(datetime.now().year)
            _time = now_year + '-' + s_time
            result_time = time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(_time, "%Y-%m-%d"))
        # 1小时前
        elif u'小时前' in s_time:
            hours = re.findall(u'(\d+)小时前', s_time)[0]
            hours_ago = (datetime.now() - timedelta(hours=int(hours))).strftime("%Y-%m-%d %H:%M:%S")
            result_time = hours_ago
        time_tuple = time.strptime(result_time, "%Y-%m-%d %H:%M:%S")
        releaseTimeLong = time.mktime(time_tuple)
        return result_time, releaseTimeLong

    @classmethod
    def js_To_Date(self, str):
        timestamp = re.findall(u'\d{10}', str)[0]
        # print(timestamp)
        result_time = datetime.fromtimestamp(int(timestamp)).strftime("%Y-%m-%d %H:%M:%S")
        # print(result_time)
        time_tuple = time.strptime(result_time, "%Y-%m-%d %H:%M:%S")
        # print(time_tuple)
        releaseTimeLong = time.mktime(time_tuple)
        return result_time, releaseTimeLong
