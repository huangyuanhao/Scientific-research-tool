import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
from tqdm import tqdm

def search_paperswithcode(title):
    """
    在paperswithcode网站上搜索给定的论文标题，并返回第一个搜索结果的标题和链接。
    """
    base_url = "https://paperswithcode.com/search?q_meta=&q_type=&q="
    search_url = base_url + title
    response = requests.get(search_url)

    if response.status_code != 200:
        print(f"network Error fetching '{title}': Status code {response.status_code}")
        return response.status_code, None

    soup = BeautifulSoup(response.text, 'html.parser')
    search_results = soup.find('meta', {'property': 'og:description'})

    if '0 search results' == search_results.get('content'):
        # print(f"No results found for '{title}'") #没有找到结果时打印输出
        return None, None

    print(f"Found results for '{title}'")

    return None, search_url

# 读取Excel文件
df = pd.read_csv('paperTitle.csv')

# 为结果和链接创建空列
df['networkStatus'] = ''
df['link'] = ''

# 对每个论文标题进行搜索并更新DataFrame
for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="Searching papers"):
    status_code, result_link = search_paperswithcode(row['title'])
    df.at[index, 'networkStatus'] = status_code
    df.at[index, 'link'] = result_link

    # 更新并写入文件
    df.to_csv('paperTitle.csv', index=False)
    # 避免频繁请求，根据需要调整延时
    time.sleep(1)
