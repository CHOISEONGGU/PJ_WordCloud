from selenium import webdriver
import pandas as pd
import numpy as np
from PIL import Image
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from konlpy.tag import Okt
okt = Okt()
from collections import Counter
import os
os.chdir('C:/Users/Playdata/Downloads/chrome/chromedriver')
driver = webdriver.Chrome('chromedriver')
driver.implicitly_wait(2)
driver.get('https://www.melon.com/genre/song_list.htm?gnrCode=GN0100')
def generate_word_cloud(genre):
    # 마스크 이미지 가져오기
    mask = np.array(Image.open(f'{genre}.png'))
    for m in range(len(mask)):
        for n in range(len(mask[m])):
            if mask[m][n]==0:
                mask[m][n] = 1
            else:
                mask[m][n] = 255
    # 워드클라우드 설정
    font_path = 'C:/WINDOWS/Fonts/malgunsl.ttf'
    background_color = 'white'
    # 전처리
    wc = WordCloud(font_path=font_path, background_color=background_color, mask=mask)
    lyrics = globals()[genre]['lyric']
    merge_lyric = ' '.join(lyrics)
    okt_lyric = okt.nouns(merge_lyric)
    okt_lyric = [word for word in okt_lyric if len(word) >= 2]
    count = Counter(okt_lyric)
    noun_list = count.most_common(100)
    noun_list = str(noun_list)
    noun_list = noun_list.replace("'", "")
    wc.generate(noun_list)
    # 이미지 파일 저장
    plt.figure(figsize=(50,50))
    plt.axis("off")
    plt.imshow(wc)
    plt.savefig(f'result_{genre}.png')
# 크롤링
genres = ['ballad', 'dance', 'rap', 'soul', 'indie', 'rock', 'trot', 'folk']
for k in range(1,9):
    driver.find_element_by_xpath(f'//*[@class="wrap_tabmenu01 type08"]/ul/li[{k}]/a').click()
    name = []
    lyric = []
    for i in range(1,51):
        driver.find_element_by_xpath(f'//*[@class="service_list_song  d_song_list"]/table/tbody/tr[{i}]/td[4]/div/a').click()
        try:
            name.append(driver.find_element_by_xpath('//*[@class="song_name"]').text)
        except:
            name.append('null')
        try:
            lyric.append(driver.find_element_by_xpath('//*[@class="lyric"]').text.replace('\n'," "))
        except:
            lyric.append('null')
        driver.back()
    globals()[genres[k-1]] = pd.DataFrame({'name':name, 'lyric':lyric})
# 생성
for j in genres:
    generate_word_cloud(j)