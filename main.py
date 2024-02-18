import argparse
from pdf_to_text import handle_file, handle_dir, check_match
import pdf_to_text as P2T
import multiprocessing as mp
from multiprocessing import Process, Queue
import os

parser = argparse.ArgumentParser(description='convert PDF to docx')
parser.add_argument('ip', type=str)
parser.add_argument('-op', type=str, default='')
parser.add_argument('-la', choices=['eng', 'vie'], default='vie')
parser.add_argument('-pic', choices=[0, 1], default=1, type=int)
args = parser.parse_args()

if __name__ == "__main__":
    match check_match(args):
        case 'file':
            print("Run singer file")
            handle_file(args)
        case 'dir':
            print("Run list files")
            org_list = os.listdir(args.ip)
            l1, l2, l3, l4 = P2T.split_list(org_list)
            output = P2T.make_output(args)
            print(output)
            proc_1 = Process(target= handle_dir, args=(args, output, l1))
            proc_2 = Process(target= handle_dir, args=(args, output, l2))
            proc_3 = Process(target= handle_dir, args=(args, output, l3))
            proc_4 = Process(target= handle_dir, args=(args, output, l4))

            proc_1.start()
            proc_2.start()
            proc_3.start()
            proc_4.start()
            
            proc_1.join()
            proc_2.join()
            proc_3.join()
            proc_4.join()
            
        case 'none':
            print("Input must be a folder or a PDF file !")