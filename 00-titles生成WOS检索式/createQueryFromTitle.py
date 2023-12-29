import csv

def create_wos_search_query_from_csv(file_path):
    try:
        # 读取CSV文件
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            titles = [row[0] for row in reader]  # 假设标题在第一列

        # 生成检索语句
        search_query = " OR ".join(f'TI=("{title.strip()}")' for title in titles if title.strip())
        return search_query
    except Exception as e:
        return f"Error: {e}"

# 假设文件路径为 'title.csv'
file_path = 'title.csv'
search_query = create_wos_search_query_from_csv(file_path)
print(search_query)

with open('search_query.txt', 'w', encoding='utf-8') as f:
    f.write(search_query)
