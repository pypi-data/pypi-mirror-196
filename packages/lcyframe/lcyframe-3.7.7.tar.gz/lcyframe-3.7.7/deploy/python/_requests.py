import requests, time, json, random
from urllib.parse import urlparse
from loguru import logger
from requests.adapters import HTTPAdapter
from uagen.uagen import random_ua

"""
request.session重试请求
"""
# url格式化: ParseResult(scheme='http', netloc='baidu.com', path='', params='', query='', fragment='')
r = urlparse("www.baidu.com")
scheme = r.scheme
path = r.path
query = r.query
port = r.port
hostname = r.hostname

s = requests.Session()
s.mount('http://', HTTPAdapter(max_retries=3))
s.mount('https://', HTTPAdapter(max_retries=3))
mark_dic = {
    'mark': 1
}
headers = {"Content-Type": "application/json; charset=UTF-8"}
try:
    resuls = s.post("www.baidu.com", headers=headers, data=json.dumps(mark_dic), timeout=6, verify=False)
    if resuls.status_code == 200:
        logger.log('INFO', f'任务结束')
except Exception as e:
    logger.log('ERROR', f'结束命令发送失败:{e}')

# 流下载
r = requests.session()
r.mount('http://', HTTPAdapter(max_retries=3))
r.mount('https://', HTTPAdapter(max_retries=3))
url = "http://www.baidu.com"
s = time.time() * 1000
chunk_size = 1024
try:
    head = r.request("head", url, stream=True, timeout=3, headers={"Accept-Encoding": "identity"})
    status_code = head.status_code
    response_ts = head.elapsed.total_seconds() * 1000

    if status_code == 200:
        # 超过20M的页面，不下载.某些页面不能返回Content-Length
        content_size = has_size = int(head.headers.get("Content-Length", 0))
        if content_size <= 10 * 2**20:
            response = r.request("get", url, stream=True, timeout=3)
            response_ts = response.elapsed.total_seconds() * 1000
            if status_code == 200:
                # self.log.debug('[%s 页面大小]: %0.2f MB' % (url, content_size / chunk_size / 1024))
                d = time.time() * 1000
                for data in response.iter_content(chunk_size=chunk_size):
                    if has_size == 0:
                        content_size += len(data)
                download_ts = time.time() * 1000 - d
        else:
            msg = "页面过大，已超过20M，无法监控，请减少页面数据"
    connection_ts = time.time() * 1000 - s
except Exception as e:
    status_code = 500
    msg = str(e)



# 请求头
class MyRequest(object):

    def gen_random_ip(self):
        """
        生成随机IP字符串
        """
        while True:
            ip = ipaddress.IPv4Address(random.randint(0, 2 ** 32 - 1))
            if ip.is_global:
                return ip.exploded

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
        ip = self.gen_random_ip()
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
            'X-Forwarded-For': ip,
            'X-Real-IP': ip
        }
        return headers

    def get_proxy(self):
        return random.choice(
            [{'http': 'socks5h://127.0.0.1:10808'}]
        )

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
                                proxies=self.get_proxy(),
                                timeout=30,
                                verify=False,  # 请求SSL验证
                                **kwargs)
        except Exception as e:
            return None

        return resp.status_code == 200 and resp.content

"""
跳转请求

方法1：
你现在知道如何获取跳转后的URL了吗，直接从responseheader，获取Location即可。
在request.header中返回header的key是不区分大小写的， 所以全小写也是可以正确取值的。
"""
def request_jd():
    url = 'http://jd.com/'
    response = requests.get(url=url, allow_redirects=False, headers=MyRequest().gen_fake_header())
    # return response.headers.get('location')
    return response.headers.get('Location')

"""
方法2：
其实默认情况下， requests会自动跳转，如果发生了重定向，会自动跳到location指定的URL，我们只需要访问URL， 获取response， 然后
response.url就可以获取到真实的URL啦。
"""

def request_jd2():
    url = 'http://jd.com/'
    response = requests.get(url=url, headers=MyRequest().gen_fake_header())
    return response.url