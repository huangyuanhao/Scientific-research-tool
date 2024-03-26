from DrissionPage import ChromiumPage, ChromiumOptions
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
from tqdm import tqdm
import re

def search_googlescholar(page,excel):

    # 访问网页
    url = 'https://scholar.google.com.hk/scholar?hl=zh-CN&as_sdt=0%2C5&q=&btnG='
    page.get(url)
    page.ele('#gs_hdr_tsi').input(excel['searchInfo'])
    page.ele('#gs_hdr_tsb').click()
    # result_number_info=page.ele('条结果')
    # result_number = re.search(r"\d+", result_number_info.text)
    # result_number = int(result_number.group()) if result_number else None
    # if result_number==1:
    time.sleep(1)

    try:
        papers_info = page.ele('#gs_res_ccl_mid')
        # one_paper = papers_info.ele('.gs_r gs_or gs_scl')
        one_paper = papers_info.ele('@data-rp=0')
        title = one_paper.ele('tag:h3@@class=gs_rt').ele('a').text
    except:
        print('no result:'+excel['searchInfo'])
        return 'no result',None,None,None

    try:
        doi = one_paper.ele('.paper-info').attrs['paper_id']
    except:
        print('no doi:'+excel['searchInfo'])

    if title in excel['searchInfo']:
        return '', doi, title, 'match'
    else:
        return '', doi, title, 'no_match'


# 读取Excel文件
df = pd.read_csv('papers.csv',encoding='gbk')


page = ChromiumPage()

# 对每个论文标题进行搜索并更新DataFrame
for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="Searching papers"):

    status, doi, title, is_match = search_googlescholar(page,row)
    df.at[index, 'status'] = status
    df.at[index, 'doi'] = doi
    df.at[index, 'title'] = title
    df.at[index, 'is_match'] = is_match

    # 更新并写入文件
    df.to_csv('result.csv', index=False,encoding='gbk')
    # 避免频繁请求，根据需要调整延时
    time.sleep(1)
