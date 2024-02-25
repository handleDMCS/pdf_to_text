from multiprocessing import Process
import threading
import easyocr 
import pandas as pd
from pdf_to_text import pdf_to_images
import os

class ThreadRunner(threading.Thread):
    """ This class represents a single instance of a running thread"""
    def __init__(self, name, image, lang = 'en', gpu = False):
        threading.Thread.__init__(self)
        self.name = name
        self.image = image
        self.lang = lang
        self.gpu = gpu
    def run(self):
        print(self.name)
        reader = easyocr.Reader([self.lang], gpu = self.gpu)
        results = reader.readtext(self.image)
        df_results_easyOCR = pd.DataFrame(results, columns=['bbox','text','conf'])
        return df_results_easyOCR

class ProcessRunner:
    """ This class represents a single instance of a running process """
    def runp(self, pdf_file, pid, lang, gpu):
        mythreads = []
        list_pages, index_list, file_name = pdf_to_images(pdf_file)
        for tid in range(len(list_pages)):
            name = "Proc-"+str(tid)
            th = ThreadRunner(name, list_pages[tid], lang, gpu)
            mythreads.append(th) 
        for i in mythreads:
            i.start()
        for i in mythreads:
            i.join()

class ParallelExtractor:    
    def runInParallel(self, pdf_folder, lang = 'en', gpu = False):
        myprocs = []
        prunner = ProcessRunner()
        os.chdir(pdf_folder)
        # Lấy danh sách các tệp trong thư mục
        file_list = os.listdir()
        for pid in range(len(file_list)):
            pr = Process(target=prunner.runp, args=(pid, file_list[pid], lang, gpu)) 
            myprocs.append(pr) 
#        if __name__ == 'parallel_module':    #This didnt work
#        if __name__ == '__main__':              #This obviously doesnt work
#        multiprocessing.freeze_support()        #added after seeing error to no avail
        for i in myprocs:
            i.start()

        for i in myprocs:
            i.join()
