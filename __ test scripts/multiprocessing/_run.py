from parallel import process_handler


def run(unsorted_array):
    elapsed_time, sorted_array = process_handler.run(unsorted_array)

    return elapsed_time, sorted_array
