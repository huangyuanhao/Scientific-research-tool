import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, Label, Entry, Button, Text
import numpy as np
import os





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
    key_content_lookup = entry_key_content_lookup.get("1.0", "end-1c")  # 获取文本框中的所有文本

    try:
        source_data = read_data(source_file)

        if key_content_lookup.strip():
            lookup_values = key_content_lookup.splitlines()  # 按行分割文本
        else:
            lookup_table = read_data(lookup_file)
            key_column_lookup = entry_key_column_lookup.get()
            if not key_column_lookup:
                key_column_lookup = lookup_table.columns[0]
            lookup_values = lookup_table[key_column_lookup].unique()

        if not key_column_source:
            key_column_source = source_data.columns[0]

        temp_results = []
        for key in lookup_values:
            match = source_data[source_data[key_column_source] == key]
            if not match.empty:
                temp_results.append(match)
            else:
                # 如果在源数据中未找到匹配项，则创建一个包含查找键的新行
                missing_row = pd.DataFrame({key_column_source: [key]})
                temp_results.append(missing_row)

        result_table = pd.concat(temp_results, ignore_index=True)

        desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
        result_table.to_excel(desktop+'\\提取结果.xlsx', index=False)
        messagebox.showinfo("成功", "数据提取完成，保存在'提取结果.xlsx'")
    except Exception as e:
        messagebox.showerror("错误", str(e))

# 创建窗口
root = tk.Tk()
root.title("数据提取工具")
root.geometry("600x300")  # 调整窗口大小

# 添加说明文字
Label(root, text="根据查找表B中的某一列，在源数据表A中匹配并提取。\n如果不填写列名，就根据两个表的第一列进行匹配。\n如果填写表B关键列内容，就不用添加表B路径", wraplength=400, justify="left").grid(row=0, columnspan=3)

# 创建标签、文本框和文件选择按钮
Label(root, text="源数据表A文件路径:").grid(row=1, column=0)
entry_source_file = Entry(root, width=50)
entry_source_file.grid(row=1, column=1)
Button(root, text="浏览", command=lambda: choose_file(entry_source_file)).grid(row=1, column=2)

# 使用Text组件替代原来的Entry组件用于多行输入
Label(root, text="查找表B关键列内容（如果有）:").grid(row=2, column=0)
entry_key_content_lookup = Text(root, height=4, width=50)  # 设置高度为4行
entry_key_content_lookup.grid(row=2, column=1)

Label(root, text="查找表B文件路径:").grid(row=3, column=0)
entry_lookup_file = Entry(root, width=50)
entry_lookup_file.grid(row=3, column=1)
Button(root, text="浏览", command=lambda: choose_file(entry_lookup_file)).grid(row=3, column=2)

Label(root, text="源数据表A关键列名:").grid(row=4, column=0)
entry_key_column_source = Entry(root, width=20)
entry_key_column_source.grid(row=4, column=1)

Label(root, text="查找表B关键列名:").grid(row=5, column=0)
entry_key_column_lookup = Entry(root, width=20)
entry_key_column_lookup.grid(row=5, column=1)



# 创建“提取数据”按钮
Button(root, text="提取数据", command=extract_data).grid(row=6, column=1)


# 运行主循环
root.mainloop()
