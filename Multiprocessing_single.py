
import os
import multiprocessing
import time
from multiprocessing import Process
from multiprocessing import Pool
import UIConstants_support as UICS

import AutomatedMining_RUN as AM_R

# data = (
#     ['a', '2'], ['b', '4'], ['c', '6'], ['d', '8'],
#     ['e', '1'], ['f', '3'], ['g', '5'], ['h', '7']
# )

def mp_worker((inputs, the_time)):  # The input is a tuple if [inputs, time]
    print " Processs %s\tWaiting %s seconds" % (inputs, the_time)
    time.sleep(int(the_time))
    print " Process %s\tDONE" % inputs
    print("")

def mp_handler(parameters):
    p = multiprocessing.Pool(4)
    p.map(mp_worker, parameters)  # Maps an mp_worker for each entry in data


# def runAutomatedMining(parameters):
#     handlerAutomatedMining(parameters)


# def handlerAutomatedMining(parameters):
#     p = multiprocessing.Pool(4)
#     p.map(AM_R.runAutomatedMining, parameters)  # Maps an mp_worker for each entry in data







def workerAM(procnum, return_dict,
             df_raw_dataset, df_dataset, ftr_names):
    """worker function"""
    print(ftr_names)
    print(str(procnum) + " represent!")
    return_dict[procnum] = procnum


def runAutomatedMining(df_raw_dataset, df_dataset, ftr_names):
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    jobs = []
    for i in range(1):
        p = multiprocessing.Process(target = workerAM,
                                    args = (i, return_dict, df_raw_dataset, df_dataset, ftr_names))
        jobs.append(p)
        p.start()

    for procedure in jobs:
        procedure.join()

    print("RETURN VALUES")
    print(return_dict.values())





# from threading import Thread
# from time import sleep
#
# def threaded_function(arg):
#     while True:
#         print("in")
#     # for i in range(arg):
#     #     print("running")
#     #     sleep(1)
#
# def startThread():
#     # if __name__ == "__main__":
#     thread = Thread(target = threaded_function, args = (10, ))
#     thread.start()
#     # thread.join()
#     print("thread finished...exiting")



