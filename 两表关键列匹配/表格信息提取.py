import pandas as pd
import numpy as np

def read_file(filename):
    # 根据文件扩展名判断文件类型
    if filename.endswith('.csv'):
        return pd.read_csv(filename)
    elif filename.endswith('.xlsx'):
        return pd.read_excel(filename, engine='openpyxl')
    elif filename.endswith('.xls'):
        return pd.read_excel(filename, engine='xlrd')
    else:
        raise ValueError("Unsupported file format")

# 读取数据
source_data = read_file('表A.xlsx')  # 替换为您的文件名
lookup_table = read_file('表B.xlsx')  # 替换为您的文件名

# 定义源数据表和查找表中的关键列名
key_column_source = '文献标题'  # 源数据表中的关键列名
key_column_lookup = '文献标题'  # 查找表中的关键列名

# 创建一个空的DataFrame用于存储最终结果
result_table = pd.DataFrame(columns=source_data.columns)

# 遍历查找表的每个关键列值
for key in lookup_table[key_column_lookup]:
    # 在源数据表中查找匹配的行
    match = source_data[source_data[key_column_source] == key]

    # 如果找到匹配的行，则添加到result_table中
    if not match.empty:
        result_table = result_table.append(match)
    else:
        # 如果没有找到匹配的行，则添加一个包含空值的行
        result_table = result_table.append(pd.Series(dtype=np.float64), ignore_index=True)

# 将结果保存到新的Excel文件
result_table.to_excel('提取结果.xlsx', index=False)