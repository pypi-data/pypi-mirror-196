import requests, time, json, random
from urllib.parse import urlparse
# from loguru import logger
from requests.adapters import HTTPAdapter
# from uagen.uagen import random_ua

# 请求头
class MyRequest(object):


    def gen_fake_header(self):
        """
        生成伪造请求头
        """
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/68.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) '
            'Gecko/20100101 Firefox/68.0',
            'Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/68.0']
        ua = random.choice(user_agents)
        headers = {
            'Accept': 'text/html,application/xhtml+xml,'
                      'application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Referer': 'https://www.google.com/',
            'Upgrade-Insecure-Requests': '1',
            # from uagen.uagen import random_ua    内置随机浏览器头
            # 'User-Agent': random_ua(),
            'User-Agent': ua,
            # 'X-Forwarded-For': ip,
            # 'X-Real-IP': ip
        }
        return headers

    # def get_proxy(self):
    #     return random.choice(
    #         [{'http': 'socks5h://127.0.0.1:10808'}]
    #     )

    def get(self, url, params=None, check=True, **kwargs):
        """
        自定义get请求

        :param str url: 请求地址
        :param dict params: 请求参数
        :param bool check: 检查响应
        :param kwargs: 其他参数
        :return: requests响应对象
        """
        try:
            resp = requests.get(url,
                                params=params,
                                cookies=None,
                                headers=self.gen_fake_header(),
                                # proxies=self.get_proxy(),
                                timeout=30,
                                verify=False,  # 请求SSL验证
                                **kwargs)
        except Exception as e:
            return None

        return resp.status_code == 200 and resp.content

a = MyRequest()
result = a.get("https://cloud.ningsuan.com.cn", headers=a.gen_fake_header())
print(result)