import requests
import json
import pandas as pd
import time


def main(type):
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit'
                          '/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        }
    contentall = []
    if type == "app":
        catas = list(range(1,16))
        catas.append(27)
    elif type == "game":
        catas = list(range(16,30))
        catas.remove(27)
        catas.remove(24)
    else:
        print("Wrong type")
        return

    for cata in catas:
        cpage = 0
        while 1:
            time.sleep(1)
            try:
                txt = getPageContent(cata, cpage, headers)
                if not txt.empty:
                    contentall.append(txt)
                    cpage += 1
                    continue
                else:
                    print(cata, cpage, '无内容')
                    break
            except:
                print('request fail regetting...')
                time.sleep(60)
                cpage += 1
                continue
    final_df = pd.concat(contentall, ignore_index=True)
    final_df = final_df.drop_duplicates()
    final_df.to_csv('C:/Users/Administrator/Desktop/xiaomiGTags.csv', encoding='utf-8-sig', index=False)


def getPageContent(cata, cpage, headers):
    pageurl = 'http://app.mi.com/categotyAllListApi?page=' + str(cpage) + '&categoryId=' + str(cata) + '&pageSize=30'
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), pageurl)
    rs = requests.get(pageurl, headers=headers)
    r = json.loads(rs.text)
    contenttemp = r['data']
    templist = []
    for i in contenttemp:
        templist.append([i['displayName'], i['packageName'], i['level1CategoryName']])
    df = pd.DataFrame(templist, columns=['name', 'package','cata'])
    return df


#app & game
main("game")
