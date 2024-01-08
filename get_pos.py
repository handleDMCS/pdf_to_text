import pdf2image
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import cv2
import numpy as np

pytesseract.pytesseract.tesseract_cmd =r'C:\Program Files\Tesseract-OCR\tesseract.exe'

img_path = r"C:\Users\PC\Downloads\wordsworthwordle1.jpg"
sample_img = cv2.imread(img_path)
content = pytesseract.image_to_string(sample_img, lang='eng')
print(type(content))
print(content)  
print('==============')
data = pytesseract.image_to_data(sample_img, output_type='dict', lang='eng')

# def get_all_box(img):
#     boxes = len(data['level'])
#     for i in range(boxes ):
#         (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
#         img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

def isLang(text):
    import unicodedata
    try:
        text = unicode(text, 'utf-8')
    except NameError:
        pass
    text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode("utf-8")
    for char in text:
        if ('a' <= char <= 'z') or ('A' <= char <= 'Z') or ('1' <= char <= '9'):
            return True
    return False


def get_box(img, id):
    if(id >= len(data['level'])):
        print("out of bound")
        return
    # if(isLang(data['text'][id]) == True):
    #     return
    (x, y, w, h) = (data['left'][id], data['top'][id], data['width'][id], data['height'][id])
    img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    print(id, ' : ', data['text'][id])


# get_all_box(sample_img)
l = 0
r = len(data['level'])-1
for i in range(l, r+1):
    get_box(sample_img, i) 
cv2.imshow('Image', sample_img)
cv2.waitKey(0) 