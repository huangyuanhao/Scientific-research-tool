import requests
import csv
import time
import pandas as pd
from tqdm import tqdm


#该代码运行的时候不能使用代理，否则会报错
#未经身份验证的请求的主要速率限制为每小时 60 个请求，使用token每小时 5,000 个请求
# 如果只延迟1秒的时候总出现返回403错误，

token = '' # 请替换为您的GitHub个人访问令牌
headers = {'Authorization': f'token {token}'}
if token =='':
    headers = ''

def search_github(title):
    """
    在github网站上搜索给定的论文标题，并返回第一个搜索结果的标题和链接。
    """
    results = {}
    # 搜索每个标题
    url = f"https://api.github.com/search/repositories?q={title}"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"network Error fetching '{title}': Status code {response.status_code}")
        return response.status_code, None

    results = response.json()
    if results['total_count'] == 0:
        return None, None

    print(f"Found related results for '{title}' with {results['total_count']} numbers ")
    return None, url

# 读取Excel文件
df = pd.read_csv('paperTitle.csv',encoding='gbk')

# 为结果和链接创建空列
df['networkStatus'] = ''
df['link'] = ''

# 对每个论文标题进行搜索并更新DataFrame
for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="Searching papers"):
    status_code, result_link = search_github(row['title'])
    df.at[index, 'networkStatus'] = status_code
    df.at[index, 'link'] = result_link

    # 更新并写入文件
    df.to_csv('paperTitle.csv', index=False,encoding='gbk')
    # 避免频繁请求，根据需要调整延时
    time.sleep(2)

