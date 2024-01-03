from DrissionPage import ChromiumPage
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
from tqdm import tqdm

def search_codeocean(page,title):

    # 访问网页
    url = 'https://www.catalyzex.com/s/' + title
    page.get(url)
    page.wait.load_complete()

    if page.ready_state != 'complete':
        print(f"network Error fetching '{title}'")
        return "network Error", None

    result = page('No results found')
    if result:
        return None, None

    print(f"Found results for '{title}'")

    return None, page.url



# 读取Excel文件
df = pd.read_csv('paperTitle.csv')

# 为结果和链接创建空列
df['networkStatus'] = ''
df['link'] = ''


# 创建页面对象
page = ChromiumPage()


# 对每个论文标题进行搜索并更新DataFrame
for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="Searching papers"):
    status_code, result_link = search_codeocean(page,row['title'])
    df.at[index, 'networkStatus'] = status_code
    df.at[index, 'link'] = result_link

    # 更新并写入文件
    df.to_csv('paperTitle.csv', index=False)
    # 避免频繁请求，根据需要调整延时
    time.sleep(1)
