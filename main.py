import argparse
from pdf_to_text import handle_file, handle_dir, check_match

parser = argparse.ArgumentParser(description='convert PDF to docx')
parser.add_argument('ip', type=str)
parser.add_argument('-op', type=str, default='')
parser.add_argument('-la', choices=['eng', 'vie'], default='vie')
parser.add_argument('-pic', choices=[0, 1], default=1, type=int)
args = parser.parse_args()

match check_match(args):
    case 'file':
        print("Run files")
        handle_file(args)
    case 'dir':
        print("Run files")
        handle_dir(args)
    case 'none':
        print("Input must be a folder or a PDF file !")