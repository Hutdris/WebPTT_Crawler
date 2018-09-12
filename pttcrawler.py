# -*- coding: utf8 -*-
import shutil
import os
import time
import requests
import bs4
import re

#InsecureRequestWarning: Unverified HTTPS request is being made. Adding certificate verification is strongly advised.
#urllib3.disable_warnings()   #需要用certifi驗證連線 待補


def ptt_request(url):
    """舊寫法from大數學堂，感覺有點冗
    res = requests.get(url)
    if ("警告︰您即將進入之看板內容需滿十八歲方可瀏覽。" in res.text):
        payload = {
            "from": url[18:],
            "yes": "yes"
        }
        rs = requests.session()
        res = rs.post("https://www.ptt.cc/ask/over18", verify=False, data=payload)
        res = rs.get(url, verify=False)
    """
    return requests.get(
        url=url,
        cookies={'over18': '1'}, verify=True
        )
def webptt_title_crawler(board_name, title_keywords, search_depth=100):
    """

    :param board_name:
    :param title_keywords: tuple of key words, using and
    :param search_depth: backward search pages
    :return:
    """

    idx = get_latest_page_index(board_name)
    current_depth = 0
    urls = []
    if not idx:
        print("no index Error")
        return None

    while current_depth < search_depth:
        try:
            url = "https://www.ptt.cc/bbs/{b_name}/index{index}.html".format(b_name=board_name, index=idx)
            res = ptt_request(url)

        except:
            print('Request error')
            return None
        soup = bs4.BeautifulSoup(res.text, 'lxml')
        for index, container in enumerate(soup.select(".r-ent")):
            for title in container.select(".title"):
                if title_keywords in title.text:
                    for tag in title.find_all('a', href=True):
                        urls.append("https://www.ptt.cc/" + tag["href"])
        current_depth += 1
        idx -= 1
        print("{} result in {} pages...".format(len(urls), current_depth))

    print(urls)
    return urls
"""
        for push_tag in container.select(".hl"):
            try:
                if push_tag.text == '爆':
                    push_count = 101
                else:
                    push_count = int(push_tag.text)
            except ValueError:
                push_count = -1
        if push_count >= push_l_bound and title_key_words:
            for tag in container.find_all('a', href=True):
                urls.append("https://www.ptt.cc/" + tag["href"])

    while latest_page_index > 0 and len(urls) < eassy_bound:
        latest_page_index -= 1
        url = "https://www.ptt.cc/bbs/{b_name}/index{index}.html".format(b_name=board_name, index=latest_page_index)
        res = ptt_request(url)
        soup = bs4.BeautifulSoup(res.text, 'lxml')
        for container in soup.select(".r-ent"):
            push_count = 0
            for push_tag in container.select(".hl"):
                try:
                    if push_tag.text == '爆':
                        push_count = 101
                    else:
                        push_count = int(push_tag.text)
                except ValueError: #XX判斷 待補
                    push_count = -1
            if push_count >= push_l_bound:
                for tag in container.find_all('a', href=True):
                    urls.append("https://www.ptt.cc/" + tag["href"])
    print("#urls:{}".format(len(urls)))
    return urls
"""

def price_extrater(urls, price_patten=r"""交易價格]：.*\d*[.,]*\d{3,}"""):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36'}
    cookies = {'_ts_id': ''}
    price_patten = re.compile(price_patten)
    digits_patten = re.compile(r'\d+')
    reports = [] #(price, title, url)
    for url in urls:
        try:
            res = ptt_request(url)
        except:
            print("Invalid url!: ".format(url))
        time.sleep(0.1)
        soup = bs4.BeautifulSoup(res.text, 'lxml')
        match = re.search(price_patten, soup.prettify())
        if match:
            digits = digits_patten.findall(match.group())
            reports.append(("".join(digits), soup.title.text, url))
    return reports


def webptt_push_crwaler(board_name, eassy_bound=1, push_l_bound=0):
    latest_page_index = get_latest_page_index(board_name)
    if not latest_page_index:
        print("no index Error")
        return None
    try:
        url = "https://www.ptt.cc/bbs/{b_name}/index{index}.html".format(b_name=board_name, index=latest_page_index)
        res = ptt_request(url)

    except:
        print('Request error')
        return None

    soup = bs4.BeautifulSoup(res.text, 'lxml')
    urls = []
    for index, container in enumerate(soup.select(".r-ent")):

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

    while latest_page_index > 0 and len(urls) < eassy_bound:
        latest_page_index -= 1
        url = "https://www.ptt.cc/bbs/{b_name}/index{index}.html".format(b_name=board_name, index=latest_page_index)
        res = ptt_request(url)
        soup = bs4.BeautifulSoup(res.text, 'lxml')
        for container in soup.select(".r-ent"):
            push_count = 0
            for push_tag in container.select(".hl"):
                try:
                    if push_tag.text == '爆':
                        push_count = 101
                    else:
                        push_count = int(push_tag.text)
                except ValueError: #XX判斷 待補
                    push_count = -1
            if push_count >= push_l_bound:
                for tag in container.find_all('a', href=True):
                    urls.append("https://www.ptt.cc/" + tag["href"])
    print("#urls:{}".format(len(urls)))
    return urls


def get_latest_page_index(board_name):
    url = "https://www.ptt.cc/bbs/{}/index.html".format(board_name)
    res = ptt_request(url)
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


def photo_crawler(url, direction='photo'):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36'}
    cookies = {'_ts_id': ''}
    try:
        res = ptt_request(url)
    except:
        print("Invalid url!")
        return None
    time.sleep(0.1)
    photo_prefixs = ("jpg", "png", "bmp", "gif")
    invalid_char = tuple([i for i in "*/\[]:;|=,.?<> "])
    imgs = []
    soup = bs4.BeautifulSoup(res.text, 'lxml')
    for img in soup.find_all('a', href=True):
        if img['href'].split('.')[-1] in photo_prefixs:
            imgs.append(img['href'])

    if imgs:
        for _, i in enumerate(soup.select('.article-metaline')):
            if "標題" in i.text:
                prefix = i.text[2:]
                title = i.text
                print(i.text)
        if "prefix" not in dir():
            prefix = url.split('/')[-1]
            title = prefix

        for i in invalid_char:
            if i in prefix:
                prefix = prefix.replace(i, '')
        for index, img_url in enumerate(imgs):
            try:
                img_res = requests.get(img_url, stream=True)
            except:
                print('request fail, skip this img.{}'.format(prefix))
                break
            img_name = '{}/{}/{:03d}.{}'.format(direction, prefix,index, img_url.split('.')[-1])
            try:
                os.makedirs('{}/{}'.format(direction, prefix), exist_ok=True)
                with open(img_name, 'wb') as fw:
                    shutil.copyfileobj(img_res.raw, fw)
            except Exception as e:
                print('ERROR!!')
                print(img_name, url)
                print(str(e))

        if os.path.exists('{}/{}'.format(direction, prefix)):
            info_file = "{}/{}/info.txt".format(direction, prefix)
            with open(info_file, 'w', encoding='utf8') as fw:
                fw.write(url+'\n')
                fw.write(title)
            #except:
            #    print('WriteFile Error', info_file)
def report2csv(report, path='./report.csv'):
    with open(path, 'w', encoding='utf8') as fw:
        for pair in sorted(report, key=lambda x: x[0]):
            line = ",".join(pair)
            print(line)
            fw.write(line+'\n')

def crawler(board, push_bound = 10, eassy_bound = 10):
    urls = webptt_push_crwaler(board, push_bound, eassy_bound)
    for url in urls:
        photo_crawler(url, direction='{}_{}_{}'.format(board, eassy_bound, push_bound))
#photo_crawler('https://www.ptt.cc/bbs/Gossiping/M.1478099361.A.AF8.html', direction='test')

