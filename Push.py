# !/usr/bin/env python
# coding:utf-8
# file wechat.py
import datetime
import random
import time
import requests
import json

import sys

from lxml import etree
from zhdate import ZhDate

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.58'
}

class WeChat:
    def __init__(self):
        self.CORPID = 'ww60ebe29ad01c736d'
        self.CORPSECRET = '4qFt8CrcPNWlEdMqCyE1M_wywcUW8aMIx--dKA2GNcI'
        self.AGENTID = '1000004'
        self.TOUSER = "@all"  # 接收者用户名
        self.media = "2UnV-xzQ2yK2oxNaEd7fwhPnHTbkDLb6Hc523RyZX7E-KTKTBvyvKhBetg03jwHzX"

    def get_access_token(self):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        values = {'corpid': self.CORPID,
                  'corpsecret': self.CORPSECRET,
                  }
        req = requests.post(url, params=values)
        data = json.loads(req.text)
        return data["access_token"]

    def send_data(self):

        headers = {"Content-type": "application/json", "Accept": "*/*"}

        # weather
        weather = self.get_weather()
        today_weather = "\n" + "目前是：" + weather[12] + "\n" + \
                        "当前气温" + weather[9] + "℃" + "\n" + \
                        "温度：" + weather[13] + "\n" + \
                        "湿度:" + weather[16] + "\n" + \
                        "风向" + weather[17] + "\n" + \
                        "紫外线" + weather[18] + "\n" + \
                        weather[20] + "\n" + \
                        weather[21] + "\n" + \
                        weather[22] + "\n" + \
                        weather[23]
        # city
        city = str(weather[2]).replace("天气", "")
        # title
        title = str(weather[5])
        # love
        love_day = self.get_Love()
        # birthday
        birthday = self.get_birthday()
        # note
        chp, du = self.get_ciba()
        send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?debug=1&access_token=' + self.get_access_token()
        message = "<font color='{}'>".format(self.get_color())+title +"</font><br />"+\
            "城市：<font color='{}'>".format(self.get_color())+city+"</font><br />"+\
            "天气: <font color='{}'>".format(self.get_color())+today_weather+"</font><br />"+\
            "今天是我们恋爱的第<font color='{}'>{}{}天".format(self.get_color(),love_day,"</font>")+"<br />"+\
            "距离小可爱的生日还有<font color='{}'>{}{}天".format(self.get_color(),birthday,"</font>")+"<br />"+\
            "<font color={}>".format(self.get_color())+chp+"</font><br />"+\
            "<font color={}>".format(self.get_color())+du+"</font>"
        print(message)
        send_data = {
            "touser": self.TOUSER,
            "agentid": self.AGENTID,
            "msgtype": "mpnews",
            "mpnews":{
	            "articles": [
	            {
	                "title":"早安，敏敏",
	                "thumb_media_id":self.media,
	                "author":"小岩",
                    "content_source_url": "URL", # 图文消息点击“阅读原文”之后的页面链接
	                "digest":"元气满满的一天开始啦",
	                "content":message, # 图文消息的内容，支持html标签，不超过666 K个字节（支持id转译）
	                },
	            ]
            },
            "safe": 0,
        }
        #        send_data = '{"msgtype": "news", "safe": "0", "agentid": %s, "touser": "%s", "text": {"content": "%s"}}' % (
        #            self.AGENTID, self.TOUSER, msg)
        proxies = {'http': 'http://localhost:8080', 'https': 'http://localhost:8080'}
        r = requests.post(send_url, json=send_data, headers=headers)
        print(send_data)
        print(r.content)
        return r.content

    def get_weather(self):
        url = 'https://www.tianqi.com/beilin/'
        global headers
        website = requests.get(url=url, headers=headers)
        data = etree.HTML(website.text)  # 数据预处理
        # xpath解析页面天气数据
        weather_list = data.xpath('//dl[@class="weather_info"]//text()')
        return weather_list

    def get_Love(self):
        curr_time = datetime.datetime.now()
        love_start = '12/10/2016'
        love_today = curr_time.strftime("%m/%d/%Y")
        date1 = datetime.datetime.strptime(love_start[0:10], "%m/%d/%Y")
        date2 = datetime.datetime.strptime(love_today[0:10], "%m/%d/%Y")
        love_day = (date2 - date1).days
        return love_day

    def get_birthday(self):
        r = config["r"]
        mon = config["birthday"].split("-")[1]
        day = config["birthday"].split("-")[2]
        if r == "0":
            birthday = datetime.datetime(2022, int(mon), int(day))
        else:
            birthday = ZhDate(2022, int(mon), int(day)).to_datetime()
        # print(birthday)

        today = datetime.datetime.now()
        difference = birthday.toordinal() - today.toordinal()
        if difference < 0:
            oneDay = ZhDate(2022 + 1, 6, 24).to_datetime()
            difference = oneDay.toordinal() - today.toordinal()
        print(difference)
        return difference

    def get_ciba(self):
        url = "http://open.iciba.com/dsapi/"
        global headers
        r = requests.get(url, headers=headers)
        note_en = r.json()["content"]
        note_ch = r.json()["note"]
        return note_ch, note_en
    def get_color(self):
        # 获取随机颜色
        get_colors = lambda n: list(map(lambda i: "#" + "%06x" % random.randint(0, 0xFFFFFF), range(n)))
        color_list = get_colors(100)
        return random.choice(color_list)

if __name__ == '__main__':

    try:
        with open("config.txt", encoding="utf-8") as f:
            config = eval(f.read())
    except FileNotFoundError:
        print("推送消息失败，请检查config.txt文件是否与程序位于同一路径")
    except SyntaxError:
        print("推送消息失败，请检查配置文件格式是否正确")
    wx = WeChat()
    wx.send_data()
