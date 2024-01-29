import pdf2image
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
from docx import Document
import argparse
import os
import docx_processing
import path_processing

def check_op():
    op = args.op
     
    if(op != ''):
        op_ty = path_processing.get_path_type(op)
        if(op_ty != 'dir'):
            print("-op must be an existing folder !")
            return False
    
    return True

def handle_file():
    if(check_op() == False):
        return
    
    ip, op = args.ip, args.op
    if(op == ''):
        op = os.path.dirname(ip)

    doc = docx_processing.get_docx(ip, args.la)
    res_path = path_processing.get_f_name(par=op, fname=os.path.basename(ip)[:-4], ex='.docx') 
    print(f"Your output file is saved at : {res_path}")
    doc.save(res_path)    

def handle_dir():
    if(check_op() == False):
        return
    
    ip, op = args.ip, args.op
    if(op == ''):
        op = path_processing.get_f_name(fname=f'{os.path.basename(ip)}_to_docx', par=ip)
    else:
        op = path_processing.get_f_name(fname=f'{os.path.basename(ip)}_to_docx', par=op)
    os.makedirs(op)

    for file in os.listdir(ip):
        path = os.path.join(ip, file)
        if path_processing.get_path_type(path) == 'file':
            print(file)
            doc = docx_processing.get_docx(path, args.la)
            doc.save(f'{op}\{file[:-4]}.docx')
    print(f'Your output files are saved at: {op}')
    
parser = argparse.ArgumentParser(description='convert PDF to docx')
parser.add_argument('ip', type=str)
parser.add_argument('-op', type=str, default='')
parser.add_argument('-la', choices=['eng', 'vie'], default='vie')
args = parser.parse_args()

match path_processing.get_path_type(args.ip):
    case 'file':
        handle_file()
    case 'dir':
        handle_dir()
    case 'none':
        print("Input must be a folder or a PDF file !")
