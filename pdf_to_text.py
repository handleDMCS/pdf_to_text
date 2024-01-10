import pdf2image
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
from docx import Document
import argparse
import os 

# sua lai pytesseract.pytesseract.tesseract_cmd
pytesseract.pytesseract.tesseract_cmd =r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def get_path_type(fpath):
    if os.path.isdir(fpath):
        return 'dir'
    elif os.path.isfile(fpath) and fpath.lower().endswith('.pdf'):
        return 'file'
    else:
        return 'none'

def get_docx(pdf_file):
    # pdf -> img 
    doc = Document()
    # sua lai poppler_path
    images = pdf2image.convert_from_path(pdf_path=pdf_file, poppler_path=r'C:\Release-23.11.0-0\poppler-23.11.0\Library\bin')
    for pg, img in enumerate(images):
        text = pytesseract.image_to_string(img, lang=args.la)
        doc.add_paragraph(text)
    return doc

def check_op():
    op = args.op
     
    if(op != ''):
        op_ty = get_path_type(op)
        if(op_ty != 'dir'):
            print("-op must be an existing folder !")
            return False
    
    return True

def get_f_name(par, fname, ex = ''):
    output_f = f"{par}\{fname}{ex}"
    if os.path.exists(output_f):
        count = 1
        while True:
            new_output_f = f"{par}\{fname}({count}){ex}"
            if not os.path.exists(new_output_f):
                output_f = new_output_f
                break
            count += 1
    return output_f

def handle_file():
    if(check_op() == False):
        return
    
    ip, op = args.ip, args.op
    if(op == ''):
        op = os.path.dirname(ip)

    doc = get_docx(ip)
    res_path = get_f_name(par=op, fname=os.path.basename(ip)[:-4], ex='.docx') 
    print(f"Your output file is saved at : {res_path}")
    doc.save(res_path)    

def handle_dir():
    if(check_op() == False):
        return
    
    ip, op = args.ip, args.op
    if(op == ''):
        op = get_f_name(fname=f'{os.path.basename(ip)}_to_docx', par=ip)
    else:
        op = get_f_name(fname=f'{os.path.basename(ip)}_to_docx', par=op)
    os.makedirs(op)

    for file in os.listdir(ip):
        path = os.path.join(ip, file)
        if get_path_type(path) == 'file':
            print(file)
            doc = get_docx(path)
            doc.save(f'{op}\{file[:-4]}.docx')
    print(f'Your output files are saved at: {op}')
    
parser = argparse.ArgumentParser(description='convert PDF to docx')
parser.add_argument('ip', type=str)
parser.add_argument('-op', type=str, default='')
parser.add_argument('-la', choices=['eng', 'vie'], default='vie')
args = parser.parse_args()

match get_path_type(args.ip):
    case 'file':
        handle_file()
    case 'dir':
        handle_dir()
    case 'none':
        print("Input must be a folder or a PDF file !")


# get_docx(r"C:\Users\PC\Downloads\sample.pdf")