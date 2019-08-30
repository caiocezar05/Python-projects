pdfpath = r"C:\Users\caio.santos\Desktop\teste"
docspath = r"C:\Users\caio.santos\Desktop\teste\DOCS"

import docx
import os
import xlsxwriter
import time
import io
from PIL import Image
import pytesseract
from wand.image import Image as wi
import fnmatch

pytesseract.pytesseract.tesseract_cmd = r"C:\Users\caio.santos\AppData\Local\Tesseract-OCR\tesseract.exe"

def Get_text_from_image(pdf_path, out):
    doc = docx.Document()
    pdf=wi(filename=pdf_path,resolution=300)
    pdfImg=pdf.convert('jpeg')
    imgBlobs=[]

    for img in pdfImg.sequence:
        page=wi(image=img)
        imgBlobs.append(page.make_blob('jpeg'))

    for imgBlob in imgBlobs:
        im=Image.open(io.BytesIO(imgBlob))
        text=pytesseract.image_to_string(im,lang='por')
        text.replace("\n", "")
        doc.add_paragraph(text)

    doc.save(out +'.docx')


def trainprepare(path):
    os.chdir(path)
    excel = xlsxwriter.Workbook('contract term.xlsx')
    sh = excel.add_worksheet()
    row = 0
    ndoc = 0
    for d in os.listdir():
        doc = docx.Document(d)
        ndoc += 1
        npara = 0
        for p in doc.paragraphs:
            npara += 1
            col = 0
            row += 1
            sh.write(row, col, 'Doc: ' + str(ndoc))
            col += 1
            sh.write(row, col, 'Para: ' + str(npara))
            col += 1
            sh.write(row, col, p.text)
            col += 1

    excel.close()


print(os.listdir())


