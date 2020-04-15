# -*- coding:utf-8 -*-

import requests
import json
import os
import time

def getHTMLtext(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        jsonFile = json.loads(r.content)  # 提取json
        return jsonFile
    except:
        print("error")

def create_folder(hero):
    now = os.path.join(os.getcwd() + '\\hero' + '\\')
    os.mkdir(now + hero)
    now_path = os.path.join(os.getcwd() + '\\hero\\' + hero + '\\')
    return now_path

def main():
    x = 0  # 用于记录下载的图片张数
    start = time.time()  # 程序开始时间
    url = "http://pvp.qq.com/web201605/js/herolist.json"
    jsonFile = getHTMLtext(url)
    # print(jsonFile)
    for m in range(len(jsonFile)):
        ename = jsonFile[m]['ename']  # 编号
        cname = jsonFile[m]['cname']  # 英雄名字
        try:
            skinName = jsonFile[m]['skin_name'].split('|')  # 切割皮肤的名字，用于计算每个英雄有多少个皮肤
            skinNumber = len(skinName)
            hero_dir = create_folder(cname)
            # 下载图片,构造图片网址
            for bigskin in range(1, skinNumber + 1):
                urlPicture = 'http://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/' + str(ename) + '/' + str(
                    ename) + '-bigskin-' + str(bigskin) + '.jpg'
                picture = requests.get(urlPicture).content  # 获取图片的二进制信息
                with open(hero_dir + cname + "-" + skinName[bigskin - 1] + '.jpg', 'wb') as f:  # 保存图片
                    f.write(picture)
                    x = x + 1
                    print("正在下载....第" + str(x) + "张")
        except:
            pass
    end = time.time()  # 程序结束时间
    time_second = end - start  # 执行时间
    print("共下载" + str(x) + "张,共耗时" + str(time_second) + "秒")

if __name__ == "__main__":
    main()