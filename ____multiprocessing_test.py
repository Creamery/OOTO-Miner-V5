

from multiprocessing import Pool
from functools import partial


def f(fa, fb, fc):
    print("{} {} {}".format(fa, fb, fc[1]))
    return None


if __name__ == "__main__":
    iterable = [("1.1", "1.2", "1.3"),
                ("2.1", "2.2", "2.3"),
                ("3.1", "3.2", "3.3")]

    count_process = 5
    pool = Pool(processes = count_process)

    a = "hi"
    b = "there"

    func = partial(f, a, b)
    pool.map(func, iterable)
    pool.close()
    pool.join()


