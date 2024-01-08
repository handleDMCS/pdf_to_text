import pdf2image
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
from docx import Document

pytesseract.pytesseract.tesseract_cmd =r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def get_docx(pdf_file):
    # pdf -> img 
    doc = Document()
    images = pdf2image.convert_from_path(pdf_path=pdf_file, poppler_path=r'C:\Release-23.11.0-0\poppler-23.11.0\Library\bin')
    print(len(images))
    for pg, img in enumerate(images):
        text = pytesseract.image_to_string(img)
        print(text)
        doc.add_paragraph(text)
    doc.save('demo.docx')


get_docx(r"C:\Users\PC\Downloads\sample.pdf")