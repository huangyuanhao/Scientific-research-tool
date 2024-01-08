#%%
from DrissionPage import ChromiumPage
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
from tqdm import tqdm

page = ChromiumPage()

# 登录账号
page.get("https://tysf.cponline.cnipa.gov.cn/am/#/user/login")

#查询
page.get("https://cpquery.cponline.cnipa.gov.cn/chinesepatent/index")

# 爬取专利信息
df = pd.DataFrame(columns=['申请号_专利号','发明名称','申请人','申请日','授权公告号','法律状态','案件状态','授权公告日'])

for patent in page.eles('.table_info'):
    # print(patent.text)
    spans = patent.ele('xpath://span')

    Application_OR_Patent_Number = patent.eles('.hover_active')[0].text
    title = patent.eles('xpath://span/span')[0].text
    Applicant = spans[6].text
    ApplicationDate= spans[10].text
    AuthorizationAnnouncementNumber= spans[14].text
    legalStatus= spans[16].text
    CaseStatus= spans[18].text
    AuthorizationAnnouncementDate= spans[20].text

    df = df.append({
        '申请号_专利号':Application_OR_Patent_Number,
        '发明名称':title,
        '申请人':Applicant,
        '申请日':ApplicationDate,
        '授权公告号':AuthorizationAnnouncementNumber,
        '法律状态':legalStatus,
        '案件状态':CaseStatus,
        '授权公告日':AuthorizationAnnouncementDate
    },ignore_index=True)

    df.to_csv(' 专利信息.csv',index=False)