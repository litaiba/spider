import requests
import bs4
import time
import os
import json
from lxml import etree
from selenium.webdriver import Chrome,ChromeOptions


header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362"
        }

def getJSONtext(url):
    try:
        r = requests.get(url, headers=header, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        jsonFile = json.loads(r.content)
        return jsonFile
    except:
        return "error"

def create_folder(hero):
    now = os.path.join(os.getcwd() + '\\new' + '\\')
    os.mkdir(now + hero)
    now_path = os.path.join(os.getcwd() + '\\new\\' + hero + '\\')
    return now_path

# https://game.gtimg.cn/images/lol/act/img/skin/big2005.jpg

def main():
    option = ChromeOptions()
    # option.add_argument("--headless")  # 隐藏浏览器
    option.add_argument("--no-sandbox")  # linux系统下禁用sandbox
    browser = Chrome(options=option)  # 自动打开Chrome浏览器
    x = 0  # 用于记录下载的图片张数
    start = time.time()  # 程序开始时间
    url = "https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js"
    json_flie = getJSONtext(url)
    for m in range(len(json_flie['hero'])):
        heroId = json_flie['hero'][m]['heroId']  # 编号
        name = json_flie['hero'][m]['name']  # 英雄名字
        hero_dir = create_folder(name)
        new_url = "https://lol.qq.com/data/info-defail.shtml?id=" + str(heroId)
        # print(new_url)
        browser.get(new_url)
        time.sleep(1)  # 等待1秒
        button = browser.find_element_by_xpath('//*[@id="skinNAV"]/li[2]/a/img')
        button.click()
        time.sleep(1)  # 等待1秒

        img = browser.find_elements_by_xpath('//*[@id="skinBG"]/li/img')
        name = browser.find_elements_by_xpath('//*[@id="skinBG"]/li')
        for i in range(len(name)):
            # print(img[i].get_attribute("src"))
            # print(name[i].get_attribute("title"))
            try:
                picture = requests.get(img[i].get_attribute("src")).content  # 获取图片的二进制信息
                with open(hero_dir + str(name[i].get_attribute("title")) + '.jpg', 'wb') as f:  # 保存图片
                    f.write(picture)
                    x = x + 1
                    print("正在下载....第" + str(x) + "张")
            except:
                pass
        time.sleep(2)  # 等待1秒
    browser.close()
    end = time.time()  # 程序结束时间
    time_second = end - start  # 执行时间
    print("共下载" + str(x) + "张,共耗时" + str(time_second) + "秒")

    # end = time.time()  # 程序结束时间
    # time_second = end - start  # 执行时间
    # print("共下载" + str(x) + "张,共耗时" + str(time_second) + "秒")

if __name__ == "__main__":
    main()