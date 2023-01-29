import http.cookiejar
import re
import zlib
from urllib import request, parse, error

import urllib3

# 获取Cookiejar对象（存在本机的cookie消息）
cookie = http.cookiejar.CookieJar()

# 使用HTTPCookieProcessor创建cookie处理器，
handler = request.HTTPCookieProcessor(cookie)

# 构建opener对象
opener = request.build_opener(handler)

# 安装opener,此后调用urlopen()时都会使用安装过的opener对象
request.install_opener(opener)

# data = request.urlopen(url)

home_url = 'http://bj.lianjia.com/'
auth_url = 'https://clogin.lianjia.com/login?service=https%3A%2F%2Fwww.lianjia.com%2Fuser%2Fchecklogin%3Fredirect%3Dhttps%253A%252F%252Fbj.lianjia.com%252Fchengjiao%252Fqinghe11%252Fpg1bp450ep455%252F'
# auth_url = 'https://bj.lianjia.com/ershoufang/'
chengjiao_url = 'http://bj.lianjia.com/chengjiao/'

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'clogin.lianjia.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0'
}

# 获取lianjia_uuid
req = request.Request('http://bj.lianjia.com/')
opener.open(req)
# 初始化表单
req = request.Request(auth_url, headers=headers)
result = request.urlopen(req).read()


# 获取cookie和lt值
pattern = re.compile(r'JSESSIONID=(.*)')
jsessionid = pattern.findall(result.info().getheader('Set-Cookie').split(';')[0])[0]

html_content = result.read()
gzipped = result.info().getheader('Content-Encoding')
if gzipped:
    html_content = zlib.decompress(html_content, 16 + zlib.MAX_WBITS)
pattern = re.compile(r'value=\"(LT-.*)\"')
lt = pattern.findall(html_content)[0]
pattern = re.compile(r'name="execution" value="(.*)"')
execution = pattern.findall(html_content)[0]

# data
data = {
    'username': '13261328159',  # 替换为自己账户的用户名
    'password': 'atCJcvd8QwJkzEU',  # 替换为自己账户的密码
    'execution': execution,
    '_eventId': 'submit',
    'lt': lt,
    'verifyCode': '',
    'redirect': '',
}

# urllib进行编码
post_data = parse.urlencode(data)

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'passport.lianjia.com',
    'Origin': 'https://passport.lianjia.com',
    'Pragma': 'no-cache',
    'Referer': 'https://passport.lianjia.com/cas/login?service=http%3A%2F%2Fbj.lianjia.com%2F',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
    'Upgrade-Insecure-Requests': '1',
    'X-Requested-With': 'XMLHttpRequest',
}

req = request.Request(auth_url, post_data, headers)

try:
    result = opener.open(req)
except error.HTTPError as e:
    print(e.getcode())
    print(e.reason)
    print(e.geturl())
    print(e.info())
    req = request.Request(e.geturl())
    result = opener.open(req)
    req = request.Request(chengjiao_url)
    result = opener.open(req).read()
    print(result)
