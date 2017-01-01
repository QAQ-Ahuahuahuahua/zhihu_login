import requests
import random
try:
    import cookielib
except:
    import http.cookiejar as cookielib
from bs4 import BeautifulSoup
from PIL import Image
import time
import os.path


headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Referer': 'https://www.zhihu.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}
timeout = random.choice(range(60, 180))
session = requests.session()

#使用cookie信息加载
session.cookies = cookielib.LWPCookieJar(filename='cookies')
try:
    session.cookies.load(ignore_discard=True)
except:
    print("cookie加载失败")

def isLogin():
    # 通过查看用户个人信息来判断是否已经登录
    url = "https://www.zhihu.com/settings/profile"
    login_code = session.get(url,allow_redirects=False,headers = headers).status_code
    print(login_code)
    if int(x=login_code) == 200:
        return True
    else:
        return False

#验证登录
def login(url):
    res = session.get(url,headers = headers,timeout=timeout).content
    _xsrf = BeautifulSoup(res,'html.parser').find('input',attrs={'name':'_xsrf'})['value']
    print(_xsrf)

    login_data = {
        '_xsrf' : _xsrf,
        'password' : 'pwd',
        'captcha_type' : 'cn',
        'captcha' : get_captcha(),
        'remember_me' : 'true',
        'email' : '1233@qq.com'
    }
    repr = session.post('https://www.zhihu.com/login/email',data=login_data,headers=headers)
    print(repr)
    res = session.get('https://www.zhihu.com',headers=headers)
    print(res.text)
    session.cookies.save()
    #if res.status_code == '200':
        #print('登录成功')
        #print(res.text)
    #else:
        #print('登录失败')

#解析验证码
def get_captcha():
    t = str(int(time.time() * 1000))
    captcha_url = 'http://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
    r = session.get(captcha_url, headers=headers)
    with open('captcha.jpg', 'wb') as f:
        f.write(r.content)
        f.close()
    # 用pillow 的 Image 显示验证码
    # 如果没有安装 pillow 到源代码所在的目录去找到验证码然后手动输入
    try:
        im = Image.open('captcha.jpg')
        im.show()
        im.close()
    except:
        print(u'请到 %s 目录找到captcha.jpg 手动输入' % os.path.abspath('captcha.jpg'))
    captcha = input("please input the captcha\n>")
    return captcha


if __name__ == '__main__':
    url = 'http://www.zhihu.com'
    if isLogin():
        print("已经登录")
    else:
        print("重新登录")
        login(url)
