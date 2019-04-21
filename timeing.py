from time import time


def timeit(func):
    def wrapper(*args, **kwargs):
        s_time = time()
        result = func(*args, **kwargs)
        e_time = time()

        delta = e_time - s_time
        print(f'Executed in {delta}s')

        return result

    return wrapper
