from multiprocessing import Process, Value, Array
from time import sleep

import storage

class run_ir:
    def __init__(self, storage1):
        self.storage1 = storage1

    
    def test1(self):
        x = 0
        while True:
            x += 1
            self.storage1.set_value1(x)        
            sleep(5)