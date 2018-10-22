# -*-coding:utf-8 -*-
# 使用Pthon2，因为PIL只支持Python2
# 翻墙下载对于的chromedriver，win下载32位的：https://chromedriver.storage.googleapis.com/index.html

# 参考链接：https://blog.csdn.net/kk185800961/article/details/78747595
# https://www.cnblogs.com/zhaof/p/6953241.html



from selenium import webdriver
import time
from PIL import Image
import os
from verifyCaptcha import get_local_captcha
from uuid import uuid4
import requests

img_save = './imgs/guazi/'
try:
    os.makedirs(img_save)
except Exception as e:
    pass

img_name = str(uuid4())[:5]
# 声明浏览器对象
driver = webdriver.Chrome(r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver\chromedriver.exe")
driver.get("https://staff.guazi.com/Account/LogIn?returnUrl=https://ams.guazi.com/admin")
# text = browser.page_source    # 网页源码
input_userName = driver.find_element_by_xpath('//*[@id="userName"]')
input_password = driver.find_element_by_xpath('//*[@id="password"]')
input_loginvcode = driver.find_element_by_xpath('//*[@id="loginvcode"]')
input_userName.send_keys("username")
input_password.send_keys("123456")

cookies = driver.get_cookies()
session = cookies[0]['value']
# cookie = cookies[0]

# 浏览器页面截屏
vcode_element = driver.find_element_by_xpath('//*[@id="vcode"]')
# 保存的验证码路径
img_file = r'{}\{}.png'.format(img_save, img_name)
driver.get_screenshot_as_file(img_file)

# 定位验证码位置及大小
location = vcode_element.location
size = vcode_element.size
left = location['x']
top = location['y']
right = location['x'] + size['width']
bottom = location['y'] + size['height']

# 从文件读取截图，截取验证码位置再次保存
img = Image.open(img_file).crop((left,top,right,bottom))
img.save(img_file)

print(img_file)

captcha = int(input('captcha: '))
headers = {'cookie': 'session={}'.format(session)}
valid_url = r'https://staff.guazi.com/account/valid'
data = {'username': 'zhangbin123', 'password': '123456', 'loginvcode': str(captcha)}
res4 = requests.post(valid_url, data, headers)
print(res4.text)



#
# balance, captcha = get_local_captcha(img_file)
# print('[{}] -> [{}]'.format(balance, captcha))
#
# time.sleep(3)
# input_loginvcode.send_keys(captcha)

# 登陆
# button = driver.find_element_by_xpath('//*[@id="clickBtn"]')
# button.click()







# valid_url = r'https://staff.guazi.com/account/valid?returnUrl=https://ams.guazi.com/admin'
# headers = {'cookie': session}
# data = {'username': 'zhangbin', 'password': '123456', 'loginvcode': {}.fromkeys(captcha)}
# res4 = requests.post(valid_url, data, headers)
# print(res4.text)







# print(driver.current_url)
# text = driver.page_source
# print(text)
# time.sleep(2)
# driver.close()








