import re
import requests
import bs4
from bs4 import BeautifulSoup
cnt = 1


def get_html(url):
    try:
        kv = {'user-agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=kv)
        r.encoding = r.apparent_encoding
        r.raise_for_status()
        return r.text
    except:
        return "wrong"


def solve(html, ulist):
    soup = BeautifulSoup(html, 'html.parser')
    for tr in soup.find(id="J_goodsList").contents[0].children:
        if (isinstance(tr, bs4.element.Tag)):
            price = tr.find(class_='p-price')
            name = tr.find(class_='p-name p-name-type-2')
            name = name.find(name='em')  # price 不需要 加这句
            sto_name = re.findall('>.*?<', str(name))
            search_name = ""
            for j in sto_name:
                search_name += j[1:-1]
            search_pri = re.search('<i>(.*?)</i>', str(price))
            if (search_pri and search_name):
                ulist.append([search_name, search_pri.group(1)])

def output(ulist):
    global cnt
    with open("res.txt", 'a', encoding='utf-8') as f:
        for k in range(0, len(ulist)):
            u = ulist[k]
            f.write("{:^10}{:^150}{:^50}\n".format(cnt + k, u[0], u[1], chr(12288)))
    f.close()
    cnt += len(ulist)

def main():
    item = input("input your q: ")
    page = input("输入你想要获取多少页的数据： ")
    page = int(page) + 1
    uinfo = []
    for i in range(1, page):
        insert = i * 2 - 1
        insert = str(insert)
        url = "https://search.jd.com/Search?keyword=" + item + "&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&page=" + insert + "&s=58&click=0"
        # html=get_html("https://search.jd.com/Search?keyword=%E9%BC%A0%E6%A0%87&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E9%BC%A0%E6%A0%87&page=1&s=1&click=0")
        # print(url)
        html = get_html(url)
        if (html == 'wrong'):
            print("出现错误")
        else:
            solve(html, uinfo)
            output(uinfo)


if __name__ == "__main__":
    main()
