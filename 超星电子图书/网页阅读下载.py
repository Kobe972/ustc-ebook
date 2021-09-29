import requests
import re
import os
import shutil
import json
import img2pdf
url=input('输入阅读器页面地址：')
total_page=1
page=requests.get(url).text
result=re.search('<title>(.*?)</title>.*?var pages = (\\[.*?\\]);.*?jpgPath: "(.*?)"',page,re.S)
title=result.group(1)
pages=json.loads(result.group(2))
jpgPath=result.group(3)
base='http://img.sslibrary.com'+jpgPath #文件基址
headers={
    'Referer':'http://img.sslibrary.com/',
    'Host':'npng1.5read.com',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36 Edg/94.0.992.31'
    }
if not os.access('tmp',os.F_OK):
    os.mkdir('tmp')
print('jpg下载中……')
prefix=['bok','leg','fow','!','']
for i in range(1,6):
    for cpage in range(1,pages[i][1]+1):
        pageType=prefix[i-1]+(6-len(prefix[i-1])-len(str(cpage)))*'0'+str(cpage)
        url=base+pageType+'?zoom=0'
        page=requests.get(url)
        with open('.\\tmp\\'+str(total_page)+'.jpg','wb') as fd:
            fd.write(page.content)
        total_page+=1
target_path = '.\\tmp' #收集下载好的片段
jpg_lst = [int(f[:-4]) for f in os.listdir(target_path) if f.endswith('.jpg')]
jpg_lst.sort()
print('pdf合成中……') #将下载的每一页合并
for i in range(0,len(jpg_lst)):
    jpg_lst[i]=str(jpg_lst[i])+'.jpg'
jpg_lst = [os.path.join(target_path, filename) for filename in jpg_lst]
with open(".\\"+title+'.pdf', "wb") as f:
    f.write(img2pdf.convert(jpg_lst))
shutil.rmtree('.\\tmp') #删除临时文件
