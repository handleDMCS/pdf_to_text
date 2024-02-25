import easyocr 
from pdf_to_text import pdf_to_images
import pandas as pd
import os

reader = easyocr.Reader(['en'], gpu = False)

# Sử dụng hàm với tệp PDF đầu vào và thư mục đầu ra
pdf_folder = r'F:\Projects\datatest' # Thay đổi path
# output_folder = r'F:\Projects\datatest\output'
file_list = os.listdir(pdf_folder)

for file in file_list:
    if not file.endswith('.pdf'):
        file_list.remove(file)

list_contents = []
list_index = []
list_name = []

for i, file in enumerate(file_list):
    print("Index:",i ,"-",file)
    print(f"{pdf_folder}\{file}")
    list_pages, index_list, file_name = pdf_to_images(f"{pdf_folder}\{file}")
    list_contents.append(list_pages)
    list_index.append(index_list)
    list_name.append(file_name)

# for content, index, name in zip(list_contents, list_index, list_name):
#     print(name, "-", index)
#     print(content)




# list_pages, index_list, file_name = pdf_to_images(pdf_file)

# results = reader.readtext(list_pages[0])

# df_results_easyOCR = pd.DataFrame(results, columns=['bbox','text','conf'])

# print(df_results_easyOCR)