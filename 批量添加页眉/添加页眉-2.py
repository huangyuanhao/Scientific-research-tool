import pandas as pd
from PyPDF2 import PdfWriter, PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io

def create_page_with_text(words, x, y):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    pdfmetrics.registerFont(TTFont("chs", "C:/Windows/Fonts/SimSun.ttc"))  # 确保路径正确
    can.setFont("chs", 12)
    can.drawString(x, y, str(words))
    can.save()
    packet.seek(0)
    return PdfReader(packet)

def add_headers_from_excel(pdf_path, excel_path, output_path):
    df = pd.read_excel(excel_path)
    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    for i in range(len(reader.pages)):
        page = reader.pages[i]
        page_number = i + 1
        if page_number in df['Page Number'].values:
            header_text = df.loc[df['Page Number'] == page_number, 'Header'].iloc[0]
            header_pdf = create_page_with_text(header_text, 50, 820)  # 调整x, y以定位文本
            page.merge_page(header_pdf.pages[0])
        writer.add_page(page)

    with open(output_path, 'wb') as out:
        writer.write(out)
    print("Headers added successfully!")

if __name__ == '__main__':
    pdf_path = "附件材料1.pdf"
    excel_path = "页眉.xlsx"
    output_path = "test.pdf"
    add_headers_from_excel(pdf_path, excel_path, output_path)