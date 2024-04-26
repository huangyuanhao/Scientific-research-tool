import PyPDF2
import pandas as pd


def extract_bookmarks(pdf_path):
    # 打开PDF文件
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        # 确保文档中存在书签
        if not reader.outline:
            print("No bookmarks found.")
            return

        bookmarks = []

        def scan_item(outline, level=0):
            # 迭代处理每个书签节点
            for item in outline:
                if isinstance(item, PyPDF2.generic.Destination):  # 确保对象是书签
                    title = item.title
                    page_num = reader.get_page_number(item.page) + 1  # 页面索引从0开始，输出时加1
                    bookmarks.append({'Title': title, 'Page Number': page_num, 'Level': level})
                elif hasattr(item, 'children'):  # 如果项目有子项
                    scan_item(item.children, level + 1)

        scan_item(reader.outline)
        return bookmarks


def save_bookmarks_to_excel(bookmarks, output_file):
    if bookmarks:
        # 将书签数据转换为DataFrame
        df = pd.DataFrame(bookmarks)
        # 使用ExcelWriter写入Excel文件
        with pd.ExcelWriter(output_file) as writer:
            df.to_excel(writer, index=False)


# 调用函数并输出结果到Excel
pdf_path = '附件材料.pdf'  # 替换为你的PDF文件路径
output_excel = 'bookmarks.xlsx'  # 输出的Excel文件名
bookmarks = extract_bookmarks(pdf_path)
save_bookmarks_to_excel(bookmarks, output_excel)
print("Bookmarks have been saved to Excel.")
