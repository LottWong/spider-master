
import os
import re
import time
import random
import requests

from PIL import Image
import jieba
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud


s = requests.Session()
COMMENTS_FILE_PATH = 'douban_comments.txt'
WC_MASK_IMG = 'Emile.jpg'
WC_FONT_PATH = '/Library/Fonts/simkai.ttf'

def login():
    url = "https://accounts.douban.com/j/mobile/login/basic"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0", "Referer": "https://accounts.douban.com/passport/login"}
    data = {'name':'18408249676', 'password':'wdd941107', "remember": "false"}
    try:
        r = s.post(url, headers=headers, data=data)
        r.raise_for_status()
    except:
        print('name or password error')
        return 0
    print(r.text)
    return 1

def spider_comments(page=0):
    print('第%d页' %int(page))
    start = int(page * 20)
    url = "https://movie.douban.com/subject/1820156/comments?start=%d&limit=20&sort=new_score&status=P" % start
    try:
        r = s.get(url)
        r.raise_for_status()
    except:
        print('第%d页爬取失败或已经爬取完' %page)
        return 0
    comments = re.findall('<span class="short">(.*)</span>', r.text)
    if not comments:
        print('爬取完毕0')
        return 0
    with open(COMMENTS_FILE_PATH, 'a+', encoding='utf-8') as file:
        file.writelines('\n'.join(comments))
    return 1

def batch_spider_comments():
    if os.path.exists(COMMENTS_FILE_PATH):
        os.remove(COMMENTS_FILE_PATH)
    page = 0
    while spider_comments(page):
        page +=1
        time.sleep(random.random() * 5)
    print('爬取完毕1')

def cut_word():
    with open(COMMENTS_FILE_PATH, encoding='utf-8') as file:
        comment_txt = file.read()
        world_list = jieba.cut(comment_txt, cut_all=True)
        wl = " ".join(world_list)
        # print(wl)
        return wl

def create_word_cut():
    wc_mask = np.array(Image.open(WC_MASK_IMG))
    stop_words = ['就是', '不是', '但是', '还是', '只是', '这样', '这个', '一个', '什么', '电影', '没有']
    wc = WordCloud(background_color="white", max_words=50, mask=wc_mask, scale=4,
                   max_font_size=50, random_state=42, stopwords=stop_words, font_path=WC_FONT_PATH)
    wc.generate(cut_word())
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.figure()
    plt.show()

if __name__ == "__main__":
    # if login():
    #     batch_spider_comments()
    create_word_cut()