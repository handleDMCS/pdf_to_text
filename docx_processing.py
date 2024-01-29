import pdf_processing
import os
from docx import Document
import image_processing
import cv2

def get_docx(pdf, arg_la):
    # pdf -> img 
    doc = Document()
    page_width, page_height = doc.sections[0].page_width, doc.sections[0].page_height
    content_list = pdf_processing.get_content(pdf, arg_la)
    for pg, content in enumerate(content_list):
        if(isinstance(content, str)):
            doc.add_paragraph(content)
        else:
            img_path = r'temp_image/img.png'
            content_height, content_width = content.shape[:2] 
            cv2.imwrite(img_path, content)
            doc.add_picture(img_path)
            os.remove(img_path)
    return doc
