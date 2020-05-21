import os
import requests
import json
import time
import random

import numpy as np
import jieba
import matplotlib.pyplot as plt
from PIL import Image
from wordcloud import WordCloud

COMMENTS_FILE_PATH = 'jd_comments.txt'
WC_MASK_IMG = 'wawa.jpg'
WC_FONT_PATH = '/Library/Fonts/simkai.ttf'

def spider_comments(page=0):
    """
    京东评论数据
    """
    url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv4646&productId=1263013576' \
          '&score=0&sortType=5&page=%s&pageSize=10&isShadowSku=0&fold=1' % page
    kv = {'user-agent': 'Mozilla/5.0', 'Referer': 'https://item.jd.com/1263013576.html'}
    try:
        r = requests.get(url, headers=kv)
        r.raise_for_status()
    except:
        print('get data error')

    # print(r)
    r_json_str = r.text[26:-2]
    r_json_obj = json.loads(r_json_str)
    r_json_comments = r_json_obj['comments']
    for oneData in r_json_comments:
        with open(COMMENTS_FILE_PATH, 'a+', encoding='utf-8') as file:
            file.write(oneData['content'] + '\n')
        # print(oneData['content'])

def batch_spider_comments(n):
    """
    批量爬取
    """
    if os.path.exists(COMMENTS_FILE_PATH):
        os.remove(COMMENTS_FILE_PATH)
    for i in range(n):
        print('第%s页' % i)
        spider_comments(i)
        time.sleep(random.random() * 5)

def cut_word():
    """
    对数据分词
    """
    with open(COMMENTS_FILE_PATH, 'r', encoding='utf-8') as file:
        comments_text = file.read()
        word_list = jieba.cut(comments_text, cut_all=True)
        result = " ".join(word_list)
        # print(result)
        return result
        
def create_word_cloud():
    """
    生成词云
    """
    wc_mask = np.array(Image.open(WC_MASK_IMG))
    wc = WordCloud(background_color='white', max_words=2000, mask=wc_mask, scale=4, max_font_size=50, random_state=42, font_path=WC_FONT_PATH)

    words = cut_word()
    wc.generate(words)
    plt.imshow(wc, interpolation='bilinear')
    # plt.axis("off")
    # plt.figure()
    plt.show()


if __name__ == "__main__":
    #1.spider data
    # batch_spider_comments(100)

    #2.词云
    create_word_cloud()