from multiprocessing import Process, Value, Array
from time import sleep

import storage

class print_test1:
    def __init__(self, storage1):
        self.storage1 = storage1

    def print1(self):
        while True:
            print(self.storage1.get_value1())
            sleep(1)