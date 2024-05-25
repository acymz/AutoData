import json
import requests
import re
import os
import time

spn=1
name=''

print('请先CD到json文件所在目录，再执行python clan.py，否则目录不对')

l_jar,lj_url=[],[]
l1,l2=[],[]
 #文件下载函数，github网站的资源爬取讲究有点多，请注意设为自己电脑可用代理服务器，或者可以直连的话，将代理行删除或注释掉。
def down(lf,i,fn):
    global l_jar,lj_url,l1
    url=i[2]
    wjn=fn+'/'+i[1]
    try:
        s = requests.Session()
        s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0'
        s.keep_alive = False
        #s.proxies = {"https": "192.168.3.54:7890", "http": "192.168.3.54:7890"}  #设置代理
        print('正在请求：'+url)
        if not url in lj_url:
            res=s.get(url,timeout=5)
            print('初始请求状态码'+str(res))
            res.close()  #关闭请求，避免请求过多被github封IP
            if str(res)=='<Response [200]>':
                print(wjn)
                with open(wjn,'wb') as f:
                    f.write(res.content)
                del res #删除请求数据释放内存（应该没啥必要）
                l_jar.append(i)
                lj_url.append(i[2])
                time.sleep(0.5)
            else:
                print('请求失败')
                lf.append(i)
                time.sleep(0.5)
        else:
            l1[l1.index(i)][1]=l_jar[lj_url.index(i[2])][1]
            print('该爬虫包已下载')
    except:
        print('请求失败')
        lf.append(i)
        time.sleep(1)

#json文件逐行分析，取jar爬虫包及每个站点的独立json文件信息列表  ： [ 行索引 ，文件名 ， 指向地址]
def http_urls(ti):
    ext,jar,spider='','',''
    try:
        ext=re.findall('"ext":"http.+"',ti.replace(' ',''))[0].split('"')[3]
        if ext.endswith('.vod'):
            ext=''
    except:
        pass
    try:
        jar=re.findall('"jar":"http.+"',ti.replace(' ',''))[0].split('"')[3]
    except:
        pass
    try:
        spider=re.findall('"spider":"http.+"',ti.replace(' ',''))[0].split('"')[3]
    except:
        pass
    return [ext,jar,spider]

def clean(filename:str):
    invalid_chars='[\\\/:*?"<>|]'
    replace_char=''
    return re.sub(invalid_chars,replace_char,filename)

def names(ti):
    global name
    try:
        n=re.findall('"name":".+"',ti.replace(' ',''))[0].split('"')[3].strip()
        if n:
            name=clean(n)
    except:
        pass
    return name

def parse2(ti,num):
    global l1,l2,t1,spn
    urls=http_urls(ti)
    print(num,ti)
    print(urls)
    wjn=names(ti)
    if urls[0]:
        print(wjn)
        if wjn:
            wjn=wjn+'.json'
            l2.append([num,wjn,urls[0]])
    if urls[1]:
        name=urls[1].split('/')[-1]
        name=clean(name)
        if name.endswith(('.jar','.zip')):
            l1.append([num,name,urls[1]])
        else:
            name='spider'+str(spn)+'.jar'
            l1.append([num,name,urls[1]])
            spn+=1
    if urls[2]:
        name=urls[2].split('/')[-1]
        name=clean(name)
        if name.endswith(('.jar','.zip')):
            l1.append([num,name,urls[2]])
        else:
            name='spider'+str(spn)+'.jar'
            l1.append([num,name,urls[2]])
            spn+=1

def rp_n(l1,l2,t1,wj):
    for i in l1:
        ss='http://127.0.0.1:8001/'+wj+'/jar/'+i[1]
        t1[i[0]]=t1[i[0]].replace(i[2],ss)
    for i in l2:
        ss=ss='http://127.0.0.1:8001/'+wj+'/sites/'+i[1]
        t1[i[0]]=t1[i[0]].replace(i[2],ss)
    t='\n'.join(t1)
    with open('./'+wj+'/'+'local-'+wj+'.json','w',encoding='utf-8') as f:
        f.write(t)

def qc(l4,l5):
    for i in l4:
        if i in l5:
            del l4[l4.index(i)]

wj=input('请输入json完整文件名（不含.json）：')
flag=1
while flag:
    try:
        fn='./'
        j=fn+wj+'.json'
        with open(j,'r',encoding='utf-8') as f:
            t=f.read()
        try:
            os.mkdir('./'+wj)
            os.mkdir('./'+wj+'/jar')
            os.mkdir('./'+wj+'/sites')
        except:
            pass
        flag=0
    except:
        print('无此文件名，请重新输入，或确认文件目录是否正确')
        wj=input('请输入json完整文件名（不含.json）：')


t1=t.split('\n')

for i in range(len(t1)):
    if t1[i].startswith(('#','//')):  #过滤注释行
        continue
    parse2(t1[i],i)

lf=[]
for i in l1:
    sn=fn+wj+'/'+'jar'
    down(lf,i,sn)

for i in l2:
    jn=fn+wj+'/'+'sites'
    down(lf,i,jn)

print('以下网址获取文件失败')
for i in lf:
    print(i)

failed_wj=fn+wj+'/请求失败网址列表.txt'
try:
    failed=''
    for i in lf:
        ff=','.join([str(i[0]),i[1],i[2]])
        failed=failed+ff+'\n'
except:
    pass

with open(failed_wj,'w',encoding='utf-8') as f:
    f.write(failed)

if lf:
    qc(l1,lf)
    qc(l2,lf)

rp_n(l1,l2,t1,wj)

pz='http://127.0.0.1:8001/'+wj+'/'+wj+'.json'
with open('./'+wj+'/'+'配置地址.txt','w') as f:
    f.write(pz)


end=input('回车后结束')





