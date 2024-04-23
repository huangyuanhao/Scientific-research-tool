import pandas as pd

# 加载Excel文件
file_path = 'savedrecs.xls'

# 定义要提取的列及其新名称
columns_to_extract = {
    'Article Title': '文献标题',
    'Authors': '作者简称',
    'Author Full Names': '作者全称',
    'Reprint Addresses': '通讯作者',
    'Publication Year': '发表年',
    'Publication Date': '发表日期',
    'Publication Type': '发表类型',
    'Document Type': '文献类型',
    'Source Title': '文献来源',
    'Conference Title': '会议标题',
    'Times Cited, All Databases': '被引次数',
    'Volume': '卷',
    'Issue': '期',
    'Start Page': 'Start Page',
    'End Page': 'End Page',
    'DOI': 'DOI',
    'DOI Link': 'DOI Link',
    'UT (Unique WOS ID)': 'WOS ID',
    'Web of Science Record': 'WOS页面',
    'Abstract': '摘要'
}

# 月份缩写到数字的映射
month_map = {
    'JAN': '01', 'FEB': '02', 'MAR': '03', 'APR': '04', 'MAY': '05', 'JUN': '06',
    'JUL': '07', 'AUG': '08', 'SEP': '09', 'OCT': '10', 'NOV': '11', 'DEC': '12'
}

# 更新 "发表日期" 列
def format_date(date_str):
    if isinstance(date_str, str) and date_str.strip() != '':
        for abbrev, num in month_map.items():
            date_str = date_str.replace(abbrev, num)
        date_parts = date_str.split(' ')
        if len(date_parts) == 2:
            month, day = date_parts
            month= month.zfill(2)  # 确保月为两位数字
            day = day.zfill(2)  # 确保日为两位数字
            return '-'.join([month, day])
        return date_str.replace(' ', '-')



# 读取Excel文件并提取指定列
data_full = pd.read_excel(file_path,keep_default_na=False)
data_selected = data_full[columns_to_extract.keys()].copy()
data_selected.rename(columns=columns_to_extract, inplace=True)


data_selected['发表日期'] = data_selected['发表日期'].astype(str).apply(format_date)

data_selected['DOI Link'] = 'http://dx.doi.org/' + data_selected['DOI'].astype(str)

data_selected['WOS页面'] = 'https://webofscience.clarivate.cn/wos/woscc/full-record/' + data_selected['WOS ID'].astype(str)

# 保存处理后的数据到新的Excel文件
output_file_path = '.\WOS信息过滤后.xlsx'

with pd.ExcelWriter(output_file_path, engine='xlsxwriter') as writer:
    data_selected.to_excel(writer, index=False)
