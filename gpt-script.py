import argparse
import os 

def get_path_type(path):
    if os.path.isdir(path):
        return 'dir'
    elif os.path.isfile(path):
        return 'file'
    else:
        return 'none'

def valid():
    ip, op = args.ip, args.op

    ip_ty = get_path_type(ip)
    if(ip_ty == 'none'):
        print("Input must be a folder or a PDF file !")
        return False
    if(ip_ty != args.ty):
        print("-ty doesn't match the input path")
        return False
     
    if(op != ''):
        op_ty = get_path_type(op)
        if(op_ty != 'dir'):
            print("-op must be an existing folder !")
            return False
    
    return True

def handle_file():
    if(valid() == False):
        return
    print(get_path_type(args.ip))

def handle_folder():
    if(valid() == False):
        return
    # ip, op = args.ip, args.op
    # if(op == ''):
    #     op = os.path.dirname(ip)
    print('folder')

parser = argparse.ArgumentParser(description='convert PDF to docx')
parser.add_argument('ip', type=str)
parser.add_argument('-op', type=str, default='')
parser.add_argument('-ty', choices=['file', 'dir'], default='file')
parser.add_argument('-la', choices=['eng', 'vie'], default='vie')
args = parser.parse_args()

match args.ty:
    case 'file':
        handle_file()
    case 'folder':
        handle_folder()