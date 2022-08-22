# -*- encoding:utf-8 -*-

import requests
import json

# 后续把关键参数写成环境变量，放在github上
class SendMessage():
    def __init__(self):
        self.appID = config["app_id"]
        self.appsecret = config["app_secret"]
        self.access_token = self.get_access_token()
        self.opend_ids = self.get_openid()

    def get_access_token(self):
        """
        获取微信公众号的access_token值
        """
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}'.\
            format(self.appID, self.appsecret)
        # print(url)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36'
        }
        response = requests.get(url, headers=headers).json()
        access_token = response.get('access_token')
        print(access_token)
        return access_token

    def get_openid(self):
        """
        获取所有粉丝的openid
        """
        next_openid = ''
        url_openid = 'https://api.weixin.qq.com/cgi-bin/user/get?access_token=%s&next_openid=%s' % (self.access_token, next_openid)
        ans = requests.get(url_openid)
        print(ans.content)
        open_ids = json.loads(ans.content)['data']['openid']
        return open_ids

    def sendmsg(self, msg):
        """
        给所有粉丝发送文本消息
        """
        url = "https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={}".format(self.access_token)
        print(url)
        if self.opend_ids != '':
            for open_id in self.opend_ids:
                body = {
                    "touser": open_id,
                    "msgtype":"text",
                    "text":
                    {
                        "content": msg
                    }
                }
                data = bytes(json.dumps(body, ensure_ascii=False).encode('utf-8'))
                print(data)
                response = requests.post(url, data=data)
                # 这里可根据回执code进行判定是否发送成功(也可以根据code根据错误信息)
                #     "errmsg": "response out of time limit or subscription is canceled rid: 6302fda2-07af154f-726924e4" 需要关注用户与公众号互动
                result = response.json()
                print(result)
        else:
            print("当前没有用户关注该公众号！")

if __name__ == "__main__":
    try:
        with open("config.txt", encoding="utf-8") as f:
            config = eval(f.read())
    except FileNotFoundError:
        print("推送消息失败，请检查config.txt文件是否与程序位于同一路径")
    except SyntaxError:
        print("推送消息失败，请检查配置文件格式是否正确")

    data = 'Hello,3Nod!'
    sends = SendMessage()
    sends.sendmsg(data)
    # sends.send_media_to_user("image", './test.png')
