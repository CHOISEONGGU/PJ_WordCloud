import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
from konlpy.tag import Okt
from PIL import Image
import time
import glob

# 데이터크롤링
driver = webdriver.Chrome('C:/Users/Playdata/Downloads/chrome/chromedriver')
driver.get('https://www.melon.com/genre/song_list.htm?gnrCode=GN0100')
driver.implicitly_wait(time_to_wait=5)

song_type=[]
frame_list = ['ballad', 'dance', 'rap', 'R&b', 'indi', 'rock', 'trot', 'fork']
dfs = {}
for s in range(1, 9):
        song_type.append(driver.find_element(By.XPATH, (f"//*[@id='conts']/div[2]/ul/li[{s}]/a/span")).text)
        driver.find_element(By.XPATH, (f"//*[@id='conts']/div[2]/ul/li[{s}]/a/span")).click()
        title=[]
        singer=[]
        lyrics=[]
        for h in range(1, 11):
            driver.find_element(By.XPATH, (f"//*[@id='frm']/div/table/tbody/tr[{h}]/td[4]/div/a")).click()
            title.append(driver.find_element(By.XPATH, ("//*[@id='downloadfrm']/div/div/div[2]/div[1]/div[1]")).text)
            try:
                element = driver.find_element(By.XPATH, ("//*[@id='d_video_summary']"))
                lyrics.append(driver.find_element(By.XPATH, ("//*[@id='d_video_summary']")).text)
            except:
                lyrics.append("Null")
            driver.back()
        dfs[frame_list[s-1]] = pd.DataFrame({'title': title, 'lyrics':lyrics})

#저장파일 불러오기
for frame in dfs:
    dfs[frame].to_csv(f"{frame}.csv", index=False, encoding='utf-8-sig')

song_file_list = glob.glob('song_data_*.csv')

df_list = []
for file in song_file_list:
        df = pd.read_csv(file)
        df_list.append(df)
        
df = pd.concat(df_list, ignore_index=True)

df = df[df.lyrics != 'Null']

# 단어 전처리
text = ' '.join(df['lyrics'])

okt = Okt()
nouns = okt.nouns(text) # 명사만 추출

words = [n for n in nouns if len(n) > 1] # 단어의 길이가 1개인 것은 제외

c = Counter(words) # 위에서 얻은 words를 처리하여 단어별 빈도수 형태의 딕셔너리 데이터를 구함
c = str(c.most_common(100))

# 그래프 생성
wc = WordCloud('C:/Windows/Fonts/HMKMMAG', width=400, height=400, scale=2.0, max_font_size=250)

gen = wc.generate(c)
plt.figure()
plt.imshow(gen)

wc.to_file('song_lyrics.png')
