import multiprocessing as mp
import time

def do_something():
    print(f"Sleep 1 second!!!")
    time.sleep(1)
    print("Done")
    
    
def plus(a,b,q):
    q.put(a + b)

def multi(a,b,q):
    q.put(a * b)
    
if __name__ == '__main__':
    start = time.time()

    q1 = mp.Queue()
    q2 = mp.Queue()

    p1 = mp.Process(target=plus, args=(1, 2, q1))
    p2 = mp.Process(target=multi, args=(1, 2, q2))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    result_plus = q1.get()
    result_multi = q2.get()

    end = time.time()

    print(f"Result of plus: {result_plus}")
    print(f"Result of multi: {result_multi}")
    print(f"Time lost: {round(end - start, 2)}")
