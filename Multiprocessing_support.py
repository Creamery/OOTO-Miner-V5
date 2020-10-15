
import os
import multiprocessing
import time
from multiprocessing import Process
from multiprocessing import Pool
import UIConstants_support as UICS



data = (
    ['a', '2'], ['b', '4'], ['c', '6'], ['d', '8'],
    ['e', '1'], ['f', '3'], ['g', '5'], ['h', '7']
)

def mp_worker((inputs, the_time)):  # The input is a tuple if [inputs, time]
    print " Processs %s\tWaiting %s seconds" % (inputs, the_time)
    time.sleep(int(the_time))
    print " Process %s\tDONE" % inputs
    print("")

def mp_handler():
    p = multiprocessing.Pool(4)
    p.map(mp_worker, data)  # Maps an mp_worker for each entry in data

if __name__ == '__main__':
    mp_handler()

'''
Join and Start
'''
# def info(title):
#     print(title)
#     print('module name:', __name__)
#     print('parent process:', os.getpid())
#     print('process id:', os.getpid())
#
# def f(name):
#     info('function f')
#     print('hello', name)
#     print('hello', name)
#
#
# if __name__ == '__main__':
#     print("ASD")
#     info('main line')
#     p = Process(target = f, args = ('ruby',))
#
#     p1 = Process(target = f, args = ('may',))
#
#     p2 = Process(target = f, args = ('drew',))
#
#     p3 = Process(target = f, args = ('ash',))
#
#     p2.start()
#     p2.join()
#
#     p.start()
#     p.join()
#
#     p1.start()
#     p1.join()
#
#     p3.start()
#     p3.join()



'''
Run multiprocessing
'''
# def run():
#     count_process = UICS.PROCESS_COUNT
#     pool = Pool(processes = count_process)
#
#     manager = multiprocessing.Manager()
#     queue = manager.Queue()
#     queue_flag = manager.Queue()
#     queue_return = manager.Queue()
#
#     for i in range(count_process):
#         queue_flag.put("Done")
#
#
#
#
#     pool.close()
#     pool.join()
#
#     elapsed_time = queue_return.get()
#     sorted_array = queue_return.get()