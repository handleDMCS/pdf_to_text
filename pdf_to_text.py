from pdf2image import convert_from_path
import numpy as np
import matplotlib.pyplot as plt
import os 

def pdf_to_images(pdf_file):
    # Chuyển đổi từ tệp PDF thành danh sách các ảnh
    images = convert_from_path(pdf_path=pdf_file, poppler_path=r'poppler/bin')
    name_file = os.path.basename(pdf_file)
    list_pages = []
    index_list = []
    # Lưu từng ảnh vào thư mục đầu ra
    for i, image in enumerate(images):
        list_pages.append(np.array(image))
        index_list.append(i)

    return list_pages, index_list, name_file

# Thư mục làm việc hiện tại là F:\Projects\pdf_to_text
# Thư mục chứa dữ liệu là F:\Projects\datatest
# Thư mực sẽ chứa các kết quả:  F:\Projects\datatest\output

# # Sử dụng hàm với tệp PDF đầu vào và thư mục đầu ra
# pdf_file = r'F:\Projects\datatest\file-sample_150kB.pdf'
# # output_folder = r'F:\Projects\datatest\output'
# list_pages, index_list, file_name = pdf_to_images(pdf_file)
# print(file_name)
# for i in range(len(index_list)):
#     print(f"Page:",index_list[i])
#     print(list_pages[i])