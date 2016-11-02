# -*- coding: utf8 -*-
import shutil
import os
import time
import requests
import bs4
import lxml


def webptt_tilte_crwaler(board_name, eassy_bound=1, push_l_bound=0):
    latest_page_index = get_latest_page_index(board_name)
    print(latest_page_index)
    if latest_page_index:

        res = requests.get(
            "https://www.ptt.cc/bbs/{b_name}/index{index}.html".format(b_name=board_name, index=latest_page_index))
        soup = bs4.BeautifulSoup(res.text, 'lxml')
        urls = []
        for container in soup.select(".r-ent"):
            push_count = 0
            for push_tag in container.select(".hl"):
                try:
                    if push_tag.text == '爆':
                        push_count = 101
                    else:
                        push_count = int(push_tag.text)
                except ValueError:
                    push_count = -1
            if push_count >= push_l_bound:
                for tag in container.find_all('a', href=True):
                    urls.append("https://www.ptt.cc/" + tag["href"])
                """
                for author in contanier.select(".author"):
                    print(author.text)

                """

                # print (index, contanier.text, len(contanier.text))
    else:
        print("no index Error")
        return None

    while latest_page_index > 0 and len(urls) < eassy_bound:
        latest_page_index -= 1
        res = requests.get(
            "https://www.ptt.cc/bbs/{b_name}/index{index}.html".format(b_name=board_name, index=latest_page_index))
        soup = bs4.BeautifulSoup(res.text, 'lxml')
        for container in soup.select(".r-ent"):
            push_count = 0
            for push_tag in container.select(".hl"):
                try:
                    if push_tag.text == '爆':
                        push_count = 101
                    else:
                        push_count = int(push_tag.text)
                except ValueError:
                    push_count = -1
            if push_count >= push_l_bound:
                for tag in container.find_all('a', href=True):
                    urls.append("https://www.ptt.cc/" + tag["href"])
    print(len(urls))
    return urls


def get_latest_page_index(board_name):
    res = requests.get("https://www.ptt.cc/bbs/{}/index.html".format(board_name))
    if res:
        soup = bs4.BeautifulSoup(res.text, 'lxml')
        for i in soup.select(".btn-group"):
            for tag in i.find_all('a', href=True):
                if tag.text == "‹ 上頁":
                    latest_page = 1 + int(tag['href'].split('/')[-1].split('.')[0][5:])
                    return latest_page
    else:
        print("NameError")
        return None


def photo_crwaler(url, direction='photo'):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36'}
    cookies = {'_ts_id': ''}
    res = requests.get(url, headers=headers, cookies=cookies)
    time.sleep(0.1)
    photo_prefixs = ("jpg", "png", "bmp", "gif")
    imgs = []
    if res:
        soup = bs4.BeautifulSoup(res.text, 'lxml')
        for img in soup.find_all('a', href=True):
            if img['href'].split('.')[-1] in photo_prefixs:
                imgs.append(img['href'])
    else:
        return None

    if imgs:
        try:
            for _, i in enumerate(soup.select('.article-metaline')):
                if "標題" in i.text:
                    prefix = i.text[2:]
                    print(i.text)
            if "prefix" not in dir():
                prefix = url.split('/')[-1]

            for img_url in imgs:
                img_res = requests.get(img_url, stream=True)
                img_name = '{}/{}/{}'.format(direction, prefix, img_url.split('/')[-1])
                os.makedirs(os.path.dirname(img_name), exist_ok=True)
                with open(img_name, 'wb') as fw:
                    shutil.copyfileobj(img_res.raw, fw)
        except:
            print("prefix ERROR!!")
            print(url)
        info_file = "{}/{}/info.txt".format(direction, prefix)
        os.makedirs(os.path.dirname(info_file), exist_ok = True)
        with open(info_file, 'w') as fw:
            fw.write(url+'\n')
            fw.write(prefix)

bty_ex = webptt_tilte_crwaler("C_Chat", eassy_bound= 9999999, push_l_bound=99)
for url in bty_ex:
    photo_crwaler(url, direction='C_Chat_all_ex')