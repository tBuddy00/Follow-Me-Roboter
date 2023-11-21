from multiprocessing import Process, Value, Array
from multiprocessing.managers import BaseManager
from time import sleep

import image_startup
from print_test import print_test1
from storage import shared_storage


if __name__ == '__main__':
    BaseManager.register('shared_storage', shared_storage)      # https://stackoverflow.com/questions/3671666/sharing-a-complex-object-between-processes
    manager = BaseManager()
    manager.start()
    storage_1 = manager.shared_storage()

    print2 = print_test1(storage_1)
    ir_process = image_startup.run_ir(storage_1)


    p1 = Process(target=ir_process.test1)
    p2 = Process(target=print2.print1)

      
    p1.start()
    p2.start()

    p1.join()
    p2.join()
    