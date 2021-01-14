
import sys
import multiprocessing
from multiprocessing import Pool
from functools import partial


def f(a, b, c):
    print("{} {} {}".format(a, b, c))
    return None


def main():
    iterable = [1, 2, 3, 4, 5]
    count_process = 5
    pool = Pool(processes = count_process)

    a = "hi"
    b = "there"

    func = partial(f, a, b)
    pool.map(func, iterable)
    pool.close()
    pool.join()


if __name__ == '__main__':
    main()


