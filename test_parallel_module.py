import parallel_module

if __name__ == '__main__':    
    extractor = parallel_module.ParallelExtractor()
    extractor.runInParallel(numProcesses=3, numThreads=4)