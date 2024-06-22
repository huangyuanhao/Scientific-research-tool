from PyPDF2 import PdfWriter, PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io


# 截取pdf指定页面
def Cut():
    input1 = input("输入原始文件路径：")
    pdf_file = PdfReader(open(input1, "rb"))
    print("文件页数为：", len(pdf_file.pages), "页")
    start = input("输入开始页数：")
    end = input("输入结束页数：")
    dir_path = input("输入输出文件路径(包含文件名)：")
    output = PdfWriter()
    for i in range(int(start), int(end)):
        output.add_page(pdf_file.pages[i])
    with open(dir_path, 'wb') as out:
        output.write(out)
    print("Done!")


def AddTop():
    input1 = input("输入原始文件路径：")
    words = input("输入要添加的文字：")
    dir_path = input("输入输出文件路径(包含文件名)：")
    new_pdf = CreatePageWithWords(words, 200, 804)
    OutPutFile(input1, dir_path, new_pdf)
    print("Done!")


def AddBottom():
    input1 = input("输入原始文件路径：")
    words = input("输入要添加的文字：")
    dir_path = input("输入输出文件路径(包含文件名)：")
    new_pdf = CreatePageWithWords(words, 300, 20)
    OutPutFile(input1, dir_path, new_pdf)
    print("Done!")


def AddNumber():
    input1 = input("输入原始文件路径：")
    pdf_file = PdfReader(open(input1, "rb"))
    dir_path = input("输入输出文件路径(包含文件名)：")
    output = PdfWriter()
    for i in range(len(pdf_file.pages)):
        new_pdf = CreatePageWithWords(i + 1, 300, 20)
        page = pdf_file.pages[i]
        page.merge_page(new_pdf.pages[0])
        output.add_page(page)
        print("\r progress:{:.0f}%".format((i + 1) / len(pdf_file.pages) * 100), end="")
    with open(dir_path, 'wb') as out:
        output.write(out)
    print("Done!")


def Merge():
    input1 = input("输入要合并的pdf文件1路径：")
    input2 = input("输入要合并的pdf文件2路径：")
    outpath = input("输入输出文件路径(包含文件名)：")
    output = PdfWriter()
    file1 = PdfReader(open(input1, "rb"))
    file2 = PdfReader(open(input2, "rb"))
    for i in range(len(file1.pages)):
        output.add_page(file1.pages[i])
    for i in range(len(file2.pages)):
        output.add_page(file2.pages[i])
    with open(outpath, 'wb') as out:
        output.write(out)
    print("Done!")


def CreatePageWithWords(words, x, y):
    packet = io.BytesIO()
    # 使用Reportlab创建一个新的PDF，原理是将两个页面叠加起来
    can = canvas.Canvas(packet, pagesize=A4)
    pdfmetrics.registerFont(TTFont("chs", "C:/Windows/Fonts/SimSun.ttc"))
    can.setFont("chs", 12)
    can.drawString(x, y, str(words))
    can.save()
    packet.seek(0)
    return PdfReader(packet)


def OutPutFile(src, dir, addinfo):
    output = PdfWriter()
    srcfile = PdfReader(open(src, "rb"))
    for i in range(len(srcfile.pages)):
        page = srcfile.pages[i]
        page.merge_page(addinfo.pages[0])
        output.add_page(page)
        print("\r progress:{:.0f}%".format((i + 1) / len(srcfile.pages) * 100), end="")
    with open(dir, 'wb') as out:
        output.write(out)


if __name__ == '__main__':
    print("选择功能：")
    print("1.截取pdf指定页面")
    print("2.添加文字到pdf文件顶部")
    print("3.添加文字到pdf文件底部")
    print("4.添加页码")
    print("5.合并pdf文件")
    choice = input("输入功能编号：")
    if choice == "1":
        Cut()
    elif choice == "2":
        AddTop()
    elif choice == "3":
        AddBottom()
    elif choice == "4":
        AddNumber()
    elif choice == "5":
        Merge()
    else:
        print("输入错误！")

