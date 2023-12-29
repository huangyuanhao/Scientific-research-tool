import requests
import csv
import time
import pandas as pd
from tqdm import tqdm
from github import Github

# 替换为您的 GitHub 个人访问令牌
g = Github("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")

# 替换为您想搜索的论文题目
paper_title = "Example Paper Title"
# 读取Excel文件
df = pd.read_csv('paperTitle.csv')

# 为结果和链接创建空列
df['networkStatus'] = ''
df['link'] = ''

# 对每个论文标题进行搜索并更新DataFrame
for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="Searching papers"):
    repositories = g.search_repositories(query=f"{row['title']} in:name,description,readme ")
    if repositories.totalCount>0:
        print(row['title'])


    # df.at[index, 'networkStatus'] = status_code
    # df.at[index, 'link'] = result_link

    # 更新并写入文件
    df.to_csv('paperTitle.csv', index=False)
    # 避免频繁请求，根据需要调整延时
    time.sleep(2)




