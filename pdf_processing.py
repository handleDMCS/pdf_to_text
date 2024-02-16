import pytesseract
import cv2
import numpy as np
import image_processing
import pdf2image
import re

pytesseract.pytesseract.tesseract_cmd =r'pytessaract\tesseract.exe'

img = None
width, height = None, None
txt, data = None, None
la = None
include_pic = None

def get_box_paragraph():
    curr_box = 0
    curr_text = set(data['text'][curr_box].split())
    box_list = []
    paragraph_list = re.split(r"(?:\r?\n){2,}", txt.strip())
    for paragraph in paragraph_list:
        min_x, min_y, max_x, max_y = 0, 0, 0, 0
        word_list = paragraph.split()
        for word in word_list:
            while(word not in curr_text):
                curr_box += 1
                if(curr_box == len(data['level'])):
                    box_list.append((min_x, min_y, max_x, max_y))        
                    return box_list
                curr_text = set(data['text'][curr_box].split())
            (x, y, w, h) = (data['left'][curr_box], data['top'][curr_box], data['width'][curr_box], data['height'][curr_box])    
            if((max_x-min_x)*(max_y-min_y) == 0):
                min_x, min_y, max_x, max_y = x, y, x+w, y+h
            else:
                min_x = min(min_x, x)
                min_y = min(min_y, y)
                max_x = max(max_x, x+w)
                max_y = max(max_y, y+h)
        box_list.append((paragraph, (min_x, min_y, max_x, max_y)))
    return box_list

def add_pic(page, bbox):
    if not include_pic:
        return
    if(image_processing.has_content(img, bbox)):
        page.append(image_processing.crop(img, bbox))

def get_page():
    global width, height, txt, data
    height, width = img.shape[:2]
    txt = pytesseract.image_to_string(img, lang=la)
    data = pytesseract.image_to_data(img, output_type='dict', lang=la)

    paragraph_box_list = get_box_paragraph()
    prev = 0
    page = []
    for (paragraph, bbox) in paragraph_box_list:
        (min_x, min_y, max_x, max_y) = bbox
        gap = (0, prev, width, min_y)
        add_pic(page, gap)
        page.append(paragraph)
        prev = max_y
    gap = (0, prev, width, height)
    add_pic(page, gap)
        
    return page

def get_content(path, args):
    global img, la, include_pic
    la = args.la
    content_list = []
    include_pic = bool(args.pic)
    images = pdf2image.convert_from_path(pdf_path=path, poppler_path=r'poppler/bin')
    first_page = cv2.cvtColor(np.array(images[0]), cv2.COLOR_RGB2BGR)
    for pg, elem in enumerate(images):
        img = image_processing.PIL_to_cv2(elem)
        page = get_page()
        content_list.extend(page)
    return content_list