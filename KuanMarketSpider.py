import requests
from bs4 import BeautifulSoup
import re
import lxml.html
import csv

def main(type):
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            # 'Cookie': 
        }
    baseurl = 'https://www.coolapk.com'

    # 获取类型页面
    catapages = get_catapage(baseurl,headers,type)
    # 从类型页面的第一页开始到最后一页 访问每一页 循环
    # print(catapages)
    for catapage in catapages:
        cata = catapage.split("/")[-1]
        catapage_pagelist = get_catapage_pagelist(baseurl,catapage,headers)
        for catapage in catapage_pagelist:
            print('spidering...',catapage)
        # 通过某一页类型页面获取每页的应用链接 循环
            apkpages = get_apkpage(catapage,baseurl,headers)
            for apkpage in apkpages:
                print(apkpage)
            # 通过应用链接访问应用 获取包名名称类型标签循环
                ans = get_apk_attr(apkpage,headers)
                if ans:
                    ans.append(cata)
                    save_to_csv(ans)


def save_to_csv(content):
    with open('C:/Users/Administrator/Desktop/kuanTags.csv', 'a',encoding='utf-8-sig') as csvf:
        writer = csv.writer(csvf,lineterminator='\n')
        writer.writerow(content)


def get_apk_attr(apkpage,headers):
    rs = requests.get(apkpage, headers=headers)
    bs = BeautifulSoup(rs.text, 'lxml')
    r = re.compile("应用包名：")
    xx = re.compile("出错了")
    if bs.find_all(string=xx):
        return
    apk = bs.find_all(string=r)[0]
    apk = apk.split("：")[1]
    # print("apk",apk)
    appname = bs.find('p', attrs={'class': 'detail_app_title'}).get_text()
    appname = appname.split()[0]
    # print("appname", appname)
    tags = []
    cats = bs.find_all('span', attrs={'class': 'apk_left_span2'})
    for cat in cats:
        tags.append(cat.get_text())
    # print("tags", tags)
    ans = []
    ans.append(appname)
    ans.append(apk)
    #ans.append(tags)
    # print(ans,'ans')
    return ans


def get_apkpage(catapage,baseurl,headers):
    rs =requests.get(catapage,headers=headers)
    html = lxml.html.fromstring(rs.text)
    apkpage = html.xpath('//div[@class="app_list_left"]/a/@href')
    for i in range(len(apkpage)):
        apkpage[i] = baseurl + apkpage[i]
    return apkpage


def get_catapage_pagelist(baseurl,catapage,headers):
    rs = requests.get(catapage,headers=headers)
    html = lxml.html.fromstring(rs.text)
    last = html.xpath('//div[@class="panel-footer ex-card-footer text-center"]//li/a/@href')[-1]
    if last != "javascript:void(0);":
        page_base_url = last.split("=")[0]
        last_page_num = int(last.split("=")[1])+1
        catapage_pagelist = []
        for i in range(1,last_page_num):
            catapage_pagelist.append(baseurl+page_base_url+"="+str(i))
        return catapage_pagelist
    else:
        catapage = [catapage]
        return catapage
    # return last


def get_catapage(baseurl,headers,type):
    rs = requests.get(baseurl+'/'+str(type),headers=headers)
    html = lxml.html.fromstring(rs.text)
    content = html.xpath('//div[@class="app_right"]/div')
    for i in content[1:3]:
        print(i.xpath('//p[@class="type_title"]/a/@href'))
        print(i.xpath('//p[@class="type_tag"]/a/@href'))
    # content = html.xpath('//div[@class="app_right"]/div[@class="type_list"]/p[@class="type_title"]/a/@href')
    content = html.xpath('//div[@class="app_right"]/div[@class="type_list"]/p[@class="type_tag"]/a/@href')
    for i in range(len(content)):
        content[i] = baseurl + content[i]
    return content


# game or apk
main('apk')
