
import time


def run(value_queue, flag_queue, return_queue, process_count):
    start_time = time.clock()

    sorted_array = []

    while not flag_queue.empty():
        while not value_queue.empty():
            tuple = value_queue.get()
            value = tuple[0]

            if len(sorted_array) == 0:
                sorted_array.append(value)
            else:
                pointer_index = len(sorted_array) - 1
                pointer_value = sorted_array[pointer_index]

                while value < pointer_value and pointer_index > -1:
                    pointer_index = pointer_index - 1
                    pointer_value = sorted_array[pointer_index]

                pointer_index = pointer_index + 1

                # print("ptr val : " + str(pointer_value))
                sorted_array.insert(pointer_index, value)
                # print("sorted array contents : ")
                # print(sorted_array)
                # print()

    end_time = time.clock()
    total_time = end_time - start_time

    return_queue.put(total_time)
    return_queue.put(sorted_array)


