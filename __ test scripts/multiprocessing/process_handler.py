#
# import multiprocessing
# from multiprocessing import Pool
# from admin_process import run as admin_run
# from process import run as process_run
# import array_splitter
# from functools import partial
# from numba import jit
#
#
# @jit(forceobj = True)
# def run(unsorted_array):
#     count_process = 8
#
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
#     admin_function_0 = partial(admin_run, queue)
#     admin_function_1 = partial(admin_function_0, queue_flag)
#     admin_function_2 = partial(admin_function_1, queue_return)
#     iterable = [count_process]
#     total_time = pool.map_async(admin_function_2, iterable)
#
#     unsorted_arrays = array_splitter.split(unsorted_array, count_process)
#     unsorted_tuples = []
#     for item in unsorted_arrays:
#         unsorted_tuples.append(tuple(item))
#
#     process_id = range(count_process)
#     worker_partial_1 = partial(process_run, queue)
#     worker_partial_2 = partial(worker_partial_1, queue_flag)
#     worker_partial_3 = partial(worker_partial_2, unsorted_tuples)
#     pool.map(worker_partial_3, process_id)
#
#     pool.close()
#     pool.join()
#
#     elapsed_time = queue_return.get()
#     sorted_array = queue_return.get()
#     # print("Elapse Time : " + str(elapsed_time))
#     # print("Sorted Array :")
#     # print(sorted_array)
#
#     return elapsed_time, sorted_array
