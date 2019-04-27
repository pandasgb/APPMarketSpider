import requests
import lxml.html
import re
import time
import json
import pandas as pd
import os
import datetime


class YYB:
    def __init__(self,fpath1):
        self.pagecontextindex = 0
        self.nocontentindex = 0
        self.gameflag = 1
        self.fpath = fpath1

    def run(self):
        for gameflag in [1,2]:
            self.gameflag = gameflag
            initurl = 'https://sj.qq.com/myapp/category.htm?orgame='+str(self.gameflag)
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
            r =requests.get(initurl,headers=headers)
            print(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'), initurl, r,)
            html1 = lxml.html.fromstring(r.text)
            cataid = html1.xpath('//ul[@class="menu"]/li/ul/li/@id')
            cataid = [re.sub('-','',a,1) for a in cataid]
            cataid = [a.split('cate')[1] for a in cataid]
            for id in cataid:
                self.pagecontextindex = 0
                self.nocontentindex = 0
                self.get_page_context(id)
        self.delete_dupi()

    def get_page_context(self,id):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/69.0.3497.100 Safari/537.36'}
        pagecontext = 0
        if self.nocontentindex > 0:
            pagecontext = self.pagecontextindex
        contentall = []
        while 1:
            pageurl = 'https://sj.qq.com/myapp/cate/appList.htm?orgame='+str(self.gameflag)+'&categoryId='+id+'&pageSize=20&pageContext='+str(pagecontext)
            time.sleep(2)
            r = requests.get(pageurl, headers=headers)
            print(datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S'),pageurl,r,len(r.text))
            content = json.loads(r.text)
            contentlist = content['obj']

            if contentlist:
                self.nocontentindex = 0
                self.pagecontextindex = 0
                contenttemp = pd.DataFrame(contentlist)
                contentall.append(contenttemp)
                # print(contentall)
                if contenttemp.shape[0] < 20:
                    print('this pagecontent < 20')
                    break
                else:
                    pagecontext += 20
            else:
                print('current page has no content')
                if pagecontext == 0:
                    time.sleep(2)
                    self.get_page_context(id)
                    break
                pagecontext += 1

                self.pagecontextindex = pagecontext

                self.nocontentindex += 1
                print('index=',self.pagecontextindex,self.nocontentindex)
                if self.nocontentindex < 3:
                    self.get_page_context(id)
                    break
                else:
                    break
        if contentall:
            contentdf = pd.concat(contentall,ignore_index=True)
            fpath = self.fpath
            if os.path.exists(fpath):
                contentdf.to_csv(fpath, mode='a', encoding='utf-8-sig', index=False, header=False)
            else:
                contentdf.to_csv(fpath, encoding='utf-8-sig', index=False)
            print('write to:', fpath,contentdf.shape[0])

    def delete_dupi(self):
        temp = pd.read_csv(self.fpath)
        temp1 = temp.drop_duplicates(subset='pkgName',keep='first')
        temp1.to_csv(self.fpath,encoding='utf-8-sig')


if __name__ == "__main__":
    a = YYB('C:/Users/Administrator/Desktop/testapp.csv')
    a.run()

