from multiprocessing import Process, Value, Array
from time import sleep


Storage = Value('i',0)

def f(n):
    x = 0
    while True:
        x += 1
        n.value = x        
        sleep(5)
        

def print1(n):
    while True:
        print(n.value)
        sleep(1)
    

if __name__ == '__main__':
    p1 = Process(target=f, args=(Storage,))
    p2 = Process(target=print1, args=(Storage,))
        
    p1.start()
    p2.start()

    p1.join()
    p2.join()
    
