import jieba.analyse
import jieba
import sys
import importlib
import os
from wordcloud import WordCloud, ImageColorGenerator
from os import path
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import cv2
importlib.reload(sys)


if __name__ == "__main__":
    word_list = []
    word_dict = {}
    key_list = []
    order_list = []
    tags = []
    for line in open('dm.txt', encoding='UTF-8'):  # 2.txt是需要分词统计的文档
        item = jieba.analyse.extract_tags(line, topK=1)  # jieba分词 每一行选出一个关键词
        for i in range(len(item)):
            tags.append(item[i])
    tag_text = "/".join(tags)
    color_mask = cv2.imread("aq.png")  # 读取背景图片
    cloud = WordCloud(
        # 设置字体，不指定就会出现乱码
        font_path="simsun.ttf",
        # 设置背景色
        background_color='white',
        # 词云形状
        mask=color_mask,
        # 允许最大词汇
        max_words=300,
        # 最大号字体
        max_font_size=80,
        # 配色方案数量
        random_state=5
    )

    word_cloud = cloud.generate(tag_text)  # 产生词云
    # # 改变字体颜色
    # img_colors = ImageColorGenerator(color_mask)
    # # 字体颜色为背景图片的颜色
    # word_cloud.recolor(color_func=img_colors)
    word_cloud.to_file("pjl_cloud3.jpg")  # 保存图片
    #  显示词云图片
    plt.imshow(word_cloud)
    plt.axis('off')
    plt.show()
    # for t in tags:
    #     word_list.append(t)
    # print(word_list)
    # for item in word_list:
    #     if item not in word_dict:
    #         word_dict[item] = 1
    #     else:
    #         word_dict[item] += 1
    #     order_list = list(word_dict.values())
    #     order_list.sort(reverse=True)
    # with open("wordCount.txt", 'w') as wf2:  # 打开文件
    #     for i in range(len(order_list)):
    #         for key in word_dict:
    #             if word_dict[key] == order_list[i]:
    #                 wf2.write(key+' '+str(word_dict[key])+'\n')  # 写入txt文档
    #                 key_list.append(key)
    #                 word_dict[key] = 0
