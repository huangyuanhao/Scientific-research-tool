from DrissionPage import ChromiumPage, ChromiumOptions
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
from tqdm import tqdm
import re
import gscholar




# 读取Excel文件
df = pd.read_csv('papers.csv',encoding='gbk')

# 为结果和链接创建空列
df['result'] = ''


# 对每个论文标题进行搜索并更新DataFrame
for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="Searching papers"):
    infos=gscholar.query(row['searchInfo'])

    status_code, result_link = search_googlescholar(page,row['searchInfo'])
    # df.at[index, 'link'] = result_link

    # 更新并写入文件
    df.to_csv('result.csv', index=False,encoding='gbk')
    # 避免频繁请求，根据需要调整延时
    time.sleep(1)
