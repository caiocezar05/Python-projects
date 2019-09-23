import docx
import os
import pandas as pd
import io
from PIL import Image
import pytesseract
from wand.image import Image as wi
import fnmatch
import re

pdfpath = r"C:\Users\caio.santos\Desktop\teste\teste construdecor"
docspath = r"C:\Users\caio.santos\Desktop\teste\docs"
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\caio.santos\AppData\Local\Tesseract-OCR\tesseract.exe"

def get_pdf_text(pdf_path, out):
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
        doc.add_paragraph(text)

    doc.save(out +'.docx')

def trainprepare(path):
    os.chdir(path)

    ndoc = 0
    docnum = []
    clausula = []
    text = []
    # -QUINTA —
    rex = re.compile(r"CLÁUSULA")
    for d in fnmatch.filter(os.listdir(), '*.docx'):
        doc = docx.Document(d)
        ndoc += 1
        cl = 0
        stringx = []
        for p in doc.paragraphs:
            stringx.append(p.text)

        for string in re.split(rex, ''.join(stringx)):
            cl += 1
            docnum.append(ndoc)
            clausula.append(cl-1)
            text.append(string)

    data = {'Doc': docnum, 'clausula': clausula, 'Text': text}
    df = pd.DataFrame(data=data)
    return df

def trainprepareDF(dataf):
    docnum = []
    clausula = []
    text = []
    # PARÁGRAFO 1º
    # OBJETO:1.1.
    # LOCAÇÃO:2.1.
    # PRAZO4.
    # rex = re.compile(r"PARÁGRAFO\s\d+?º")
    rex = re.compile(r"(PARÁGRAFO\s\d+?º)|(\w+?:\d+?\.\d+?\.)")

    for i in range(0, 21):
        ndoc = dataf.iloc[i][0]
        cl = 0
        stringx = dataf.iloc[i][2]

        for string in re.split(rex, stringx):
            cl += 1
            docnum.append(ndoc)
            clausula.append(cl - 1)
            text.append(string)

    data = {'Doc': docnum, 'clausula': clausula, 'Text': text}
    dff = pd.DataFrame(data=data)
    return dff

df = trainprepare(docspath)

df.to_excel(docspath + '\\traintest contract.xlsx')






