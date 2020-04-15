import requests
import time
import os
import json


header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362"
        }

def getHTMLtext(url):
    try:
        r = requests.get(url, headers=header, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        jsonFile = json.loads(r.content)
        return jsonFile
    except:
        return "error"

def create_folder(hero):
    now = os.path.join(os.getcwd() + '\\LOL' + '\\')
    os.mkdir(now + hero)
    now_path = os.path.join(os.getcwd() + '\\LOL\\' + hero + '\\')
    return now_path

# https://game.gtimg.cn/images/lol/act/img/skin/big2005.jpg

def main():
    x = 0  # 用于记录下载的图片张数
    start = time.time()  # 程序开始时间
    url = "https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js"
    json_flie = getHTMLtext(url)
    # print(json_flie['hero'])
    for m in range(len(json_flie['hero'])):
        # print(json_flie['hero'][m])
        n = 1
        heroId = json_flie['hero'][m]['heroId']  # 编号
        name = json_flie['hero'][m]['name']  # 英雄名字
        hero_dir = create_folder(name)
        # 下载图片,构造图片网址
        for bigskin in range(0, 21):
            urlPicture = 'https://game.gtimg.cn/images/lol/act/img/skin/big' + str(int(heroId)*1000+bigskin) + '.jpg'
            # print(urlPicture)
            picture_mode = requests.get(urlPicture).status_code
            picture = requests.get(urlPicture).content  # 获取图片的二进制信息
            if picture_mode == 200:
                with open(hero_dir + name + "-" + str(n) + '.jpg', 'wb') as f:  # 保存图片
                    f.write(picture)
                    n = n + 1
                    x = x + 1
                    print("正在下载....第" + str(x) + "张")
            else:
                pass
    end = time.time()  # 程序结束时间
    time_second = end - start  # 执行时间
    print("共下载" + str(x) + "张,共耗时" + str(time_second) + "秒")

if __name__ == "__main__":
    main()