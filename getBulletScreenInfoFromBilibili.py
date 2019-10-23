import requests
import re
import os
import sys
import json
from lxml import etree
import threading

'''
爬取某一个UP主空间下的所有投递视频中的弹幕数据
api查询自 https://github.com/Vespa314/bilibili-api/blob/master/api.md
'''

# 视频AV号列表
aid_list = []

# 评论用户及其信息
info_list = []

# 弹幕数据
bs_list = []


# 获取指定UP的所有视频的AV号
# uid:用户编号
# size:单次拉取数目
# page:页数
def get_all_video(uid, size, page):
    # 获取UP主视频列表
    for n in range(1, page+1):
        url = "https://space.bilibili.com/ajax/member/getSubmitVideos?mid=" + \
            str(uid) + "&pagesize=" + str(size) + "&page=" + str(n)
        r = requests.get(url)
        text = r.text
        json_text = json.loads(text)
        # 遍历JSON格式信息，获取视频aid
        for item in json_text["data"]["vlist"]:
            aid_list.append(item["aid"])
    return aid_list


# 获取一个AV号视频下所有评论
# aid:AV号
def get_all_comment(aid):
    url = "https://api.bilibili.com/x/reply?type=1&oid=" + \
        str(aid) + "&pn=1&nohot=1&sort=0"
    r = requests.get(url)
    comment_text = r.text
    json_text = json.loads(comment_text)
    comments_count = json_text["data"]["page"]["count"]
    page = comments_count // 20 + 1
    for n in range(1, page):
        url = "https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn=" + \
            str(n)+"&type=1&oid="+str(aid)+"&sort=1&nohot=1"
        req = requests.get(url)
        text = req.text
        json_text_list = json.loads(text)
        for i in json_text_list["data"]["replies"]:
            info_list.append([i["member"]["uname"], i["content"]["message"]])
    save_commit('all_commit', info_list)
    return info_list


# 获取一个AV号视频下的所有弹幕
# url:https://api.bilibili.com/x/v1/dm/list.so?oid=124873045
# 返回值中的cid就是需要的oid
# api:https://api.bilibili.com/x/player/pagelist?aid=73016525&jsonp=jsonp
# aid:AV号
# 在xml文件在转化为某些Ubicode时会报错，将其转化为二进制数据后再用utf-8转码回来可以绕开bug
# r.text返回的是Unicode型的数据，而使用r.content返回的是bytes型的数据。
# 也就是说，在使用r.content的时候，他已经只带了 html = bytes(bytearray(html, encoding='utf-8'))
# 这是python2 的历史遗留问题
def get_cid(aid):
    url = "https://api.bilibili.com/x/player/pagelist?aid=" + \
        str(aid)+"&jsonp=jsonp"
    json_text = json.loads(requests.get(url).text)
    cid = json_text["data"][0]['cid']
    return cid


def get_all_bulletscreen(aid):
    cid = get_cid(aid)
    url = 'https://api.bilibili.com/x/v1/dm/list.so?oid=' + str(cid)
    r = requests.get(url)
    # r.encoding = 'utf-8'
    html = bytes(bytearray(r.text, encoding='iso-8859-1'))
    html = etree.HTML(html)
    info_list = html.xpath("//d")
    for item in info_list:
        info = item.xpath('./text()')
        bs_list.append(info)
    save_dm('all_dm', bs_list)
    return bs_list


# 保存评论文件为txt
def save_commit(f_name, f_content):
    f_name = str(f_name) + ".txt"
    for content in f_content:
        with open(f_name, "a", encoding='utf-8') as txt:
            txt.write(content[0] + ' '+content[1].replace('\n', '') + '\n\n')
        print("评论信息写入中")


# 保存评论文件为txt
def save_dm(f_name, f_content):
    f_name = str(f_name) + ".txt"
    for content in f_content:
        with open(f_name, "a", encoding='utf-8') as txt:
            txt.write(content[0].replace('\n', '') + '\n\n')
        print("弹幕信息写入中")


if __name__ == "__main__":
    # 爬取大可爱神乐Mea的b站信息
    get_all_video('349991143', 30, 10)
    for aid in aid_list:
        info_list.clear()
        bs_list.clear()
        get_all_comment(aid)
        get_all_bulletscreen(aid)
