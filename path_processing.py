import os
import shutil

def init_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def clear_directory_content(dir):
    shutil.rmtree(dir)
    os.makedirs(dir)

def get_path_type(fpath):
    if os.path.isdir(fpath):
        return 'dir'
    elif os.path.isfile(fpath) and fpath.lower().endswith('.pdf'):
        return 'file'
    else:
        return 'none'

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
