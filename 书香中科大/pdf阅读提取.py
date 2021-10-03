import requests
import re
import os
import shutil
import json
import img2pdf
from tqdm import tqdm

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC

req_timeout=20 #隐式等待时限（秒）
username=input('输入用户名：')
password=input('输入密码：')
url=input('输入阅读器页面地址：')

print('正在登录……')
option = webdriver.ChromeOptions()
option.add_argument('headless')# 添加无头模式
option.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=option)
driver.implicitly_wait(req_timeout)

driver.get('http://sxzkdx.chineseall.cn/sso/login.jsps?redirectUrl=http://sxzkdx.chineseall.cn')

driver.find_element_by_name('userName').send_keys(username)
driver.find_element_by_name('userPass').send_keys(password)
driver.find_element_by_id('loginBt').click()

while driver.title!='中国科学技术大学':
    pass
cookies_1=driver.get_cookies()
cookies={}
for i in cookies_1:
    cookies[i["name"]]=i["value"]
driver.close()
session=requests.Session()
source=session.get(url).text
name=re.search('input name="bname".*?value="(.*?)"',source,re.S).group(1)
total_page=int(re.search('html\(pageIndex\+"/"\+(\d*?)\)',source,re.S).group(1))
base='http://sxzkdx.chineseall.cn'+re.search("Reader.url = '(.*?pdf/)",source,re.S).group(1)
if not os.access('tmp',os.F_OK):
    os.mkdir('tmp')
print('jpg下载中……')
for i in tqdm(range(1,total_page+1),ncols=70,leave=False):
    url=base+str(i)
    page=session.get(url,cookies=cookies)
    with open('.\\tmp\\'+str(i)+'.jpg','wb') as fd:
        fd.write(page.content)
target_path = '.\\tmp' #收集下载好的片段
jpg_lst = [int(f[:-4]) for f in os.listdir(target_path) if f.endswith('.jpg')]
jpg_lst.sort()
print('pdf合成中……') #将下载的每一页合并
for i in tqdm(range(0,len(jpg_lst)),ncols=70,leave=False):
    jpg_lst[i]=str(jpg_lst[i])+'.jpg'
jpg_lst = [os.path.join(target_path, filename) for filename in jpg_lst]
with open(".\\"+name+".pdf", "wb") as f:
    f.write(img2pdf.convert(jpg_lst))
shutil.rmtree('.\\tmp') #删除临时文件

