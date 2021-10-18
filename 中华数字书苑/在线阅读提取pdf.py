import requests
import re
import os
import shutil
import json
import img2pdf
url=input('输入阅读器页面地址：')
total_page=int(input('输入总页数：'))
center=re.search('(\\?metaid=.*)&page=.*?(&.*)',url,re.S)
center=center.group(1)+center.group(2)
base='http://cebxol.apabiedu.com/api/getservice'+center+'&width=1200&height=1200&ServiceType=imagepage&page='
if not os.access('tmp',os.F_OK):
    os.mkdir('tmp')
print('jpg下载中……')
for i in range(1,total_page+1):
    url=base+str(i)
    page=requests.get(url)
    if(len(page.content)<2000):
        i-=1
        continue
    with open('.\\tmp\\'+str(i)+'.jpg','wb') as fd:
        fd.write(page.content)
target_path = '.\\tmp' #收集下载好的片段
jpg_lst = [int(f[:-4]) for f in os.listdir(target_path) if f.endswith('.jpg')]
jpg_lst.sort()
print('pdf合成中……') #将下载的每一页合并
for i in range(0,len(jpg_lst)):
    jpg_lst[i]=str(jpg_lst[i])+'.jpg'
jpg_lst = [os.path.join(target_path, filename) for filename in jpg_lst]
with open(".\\final.pdf", "wb") as f:
    f.write(img2pdf.convert(jpg_lst))
shutil.rmtree('.\\tmp') #删除临时文件
