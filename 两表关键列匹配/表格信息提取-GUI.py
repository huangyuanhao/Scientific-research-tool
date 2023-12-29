import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, Label, Entry, Button
import numpy as np

def choose_file(entry):
    """ 弹出文件选择对话框并更新文本框内容 """
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls"), ("CSV files", "*.csv")])
    if file_path:
        entry.delete(0, tk.END)
        entry.insert(0, file_path)

def read_data(file_path):
    """ 根据文件扩展名读取数据 """
    if file_path.endswith('.csv'):
        return pd.read_csv(file_path)
    else:  # 对于xlsx和xls
        return pd.read_excel(file_path)

def extract_data():
    # 从输入字段获取文件路径和列名
    source_file = entry_source_file.get()
    lookup_file = entry_lookup_file.get()
    key_column_source = entry_key_column_source.get()
    key_column_lookup = entry_key_column_lookup.get()

    try:
        source_data = read_data(source_file)
        lookup_table = read_data(lookup_file)

        # 如果未指定关键列，则使用第一列
        if not key_column_source:
            key_column_source = source_data.columns[0]
        if not key_column_lookup:
            key_column_lookup = lookup_table.columns[0]

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

        # 保存结果
        result_table.to_excel('提取结果.xlsx', index=False)
        messagebox.showinfo("成功", "数据提取完成，保存在'提取结果.xlsx'")
    except Exception as e:
        messagebox.showerror("错误", str(e))

# 创建窗口
root = tk.Tk()
root.title("数据提取工具")

# 添加说明文字
Label(root, text="根据查找表B中的某一列，在源数据表A中匹配并提取，如果不填写列名，就根据两个表的第一列进行匹配", wraplength=400, justify="left").grid(row=0, columnspan=3)

# 创建标签、文本框和文件选择按钮
Label(root, text="源数据表A文件路径:").grid(row=1, column=0)
entry_source_file = Entry(root, width=50)
entry_source_file.grid(row=1, column=1)
Button(root, text="浏览", command=lambda: choose_file(entry_source_file)).grid(row=1, column=2)

Label(root, text="查找表B文件路径:").grid(row=2, column=0)
entry_lookup_file = Entry(root, width=50)
entry_lookup_file.grid(row=2, column=1)
Button(root, text="浏览", command=lambda: choose_file(entry_lookup_file)).grid(row=2, column=2)

Label(root, text="源数据表A关键列名:").grid(row=3, column=0)
entry_key_column_source = Entry(root, width=20)
entry_key_column_source.grid(row=3, column=1)

Label(root, text="查找表B关键列名:").grid(row=4, column=0)
entry_key_column_lookup = Entry(root, width=20)
entry_key_column_lookup.grid(row=4, column=1)

# 创建“提取数据”按钮
Button(root, text="提取数据", command=extract_data).grid(row=5, column=1)

# 运行主循环
root.mainloop()
