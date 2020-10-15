
import numpy


def run(value_queue, flag_queue, unsorted_array, process_id):
    # print("Process " + str(process_id))
    unsorted_array = unsorted_array[process_id]
    # print(unsorted_array)

    while len(unsorted_array) > 0:

        # print("unsorted array : " + str(unsorted_array))

        min_value = float('inf')
        min_index = 0

        for index in range(len(unsorted_array)):
            item = unsorted_array[index]
            if item < min_value:
                min_value = item
                min_index = index

        value_queue.put((min_value, process_id))
        # print("index : " + str(min_index))
        # del unsorted_array[min_index]
        unsorted_array = numpy.delete(unsorted_array, min_index)
        # print("unsorted_array size : " + str(len(unsorted_array)))
        # print()
        # unsorted_array = unsorted_array[0:min_index - 1] + unsorted_array[min_index + 1:-1]


    flag_queue.get()

