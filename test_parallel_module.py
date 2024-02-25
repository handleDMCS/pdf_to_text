import parallel_module

if __name__ == '__main__':    
    extractor = parallel_module.ParallelExtractor()
    pdf_file = r'F:\Projects\datatest'
    extractor.runInParallel(pdf_file)