import requests
import re
import os
import shutil
from tqdm import tqdm
from PyPDF2 import PdfFileMerger

url=input('输入阅读器页面地址：')
page=requests.get(url).text
result=re.search('fileMark = "(.*?)".*?userMark = "(.*?)".*?fileName = "(.*?)".*?total = (\d+);',page,re.S)
fileMark=result.group(1)
userMark=result.group(2)
fileName=result.group(3)
total=int(result.group(4))
result=re.search("'(&pages=.*?)'",page,re.S)
base='https://pdfssj.sslibrary.com/download/getFile?fileMark=' + fileMark + '&userMark=' + userMark + result.group(1) #文件基址
headers={
    'Referer':'https://ssj.sslibrary.com/',
    'referrer':'https://ssj.sslibrary.com',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36 Edg/94.0.992.31'
    }
if not os.access('tmp',os.F_OK):
    os.mkdir('tmp')
tqdm.write('pdf下载中……')
for cpage in tqdm(range(1,total+1),ncols=70,leave=False): #下载pdf的每一页
    url=base+"&cpage=" + str(cpage)
    page=requests.get(url,headers=headers)
    if(len(page.content)<5000):
        tqdm.write('被检测到爬虫，只能爬取一部分页面！')
        break
    with open('.\\tmp\\'+str(cpage)+'.pdf','wb') as fd:
        fd.write(page.content)
        
target_path = '.\\tmp' #收集下载好的片段
pdf_lst = [int(f[:-4]) for f in os.listdir(target_path) if f.endswith('.pdf')]
pdf_lst.sort()
tqdm.write('pdf合成中……') #将下载的每一页合并
for i in tqdm(range(0,len(pdf_lst)),ncols=70,leave=False):
    pdf_lst[i]=str(pdf_lst[i])+'.pdf'
pdf_lst = [os.path.join(target_path, filename) for filename in pdf_lst]
file_merger = PdfFileMerger()
for pdf in pdf_lst:
    file_merger.append(pdf)
#file_merger.write(".\\"+fileName+'.pdf')
file_merger.write(".\\自动机器学习入门与实践.pdf")
file_merger.close()
shutil.rmtree('.\\tmp') #删除临时文件
