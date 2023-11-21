from multiprocessing import Process, Value, Array
from time import sleep

class shared_storage:
    relativ_coordinate = Array('i',range(2))
    dimensions = Array('i',range(2))
    
    value1 = Value('i',0)
    

    def set_value1(self,new):
        shared_storage.value1.value = new

    def get_value1(self):
        return shared_storage.value1.value
