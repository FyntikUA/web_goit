import multiprocessing
from time import time

def factorize_single_core(*numbers):
    factors_list = []
    for num in numbers:
        factors = []
        for i in range(1, num + 1):
            if num % i == 0:
                factors.append(i)
        factors_list.append(factors)
    return factors_list



def factorize_single(number):
    factors = []
    for i in range(1, number + 1):
        if number % i == 0:
            factors.append(i)
    return factors

def factorize(*numbers):
    num_cores = multiprocessing.cpu_count()
    print(num_cores)
    pool = multiprocessing.Pool(processes=num_cores)
    results = pool.map(factorize_single, numbers)
    pool.close()
    pool.join()
    return results

if __name__ == "__main__":
    start_time = time()
    a, b, c, d = factorize(128, 255, 99999, 10651060)
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
    end_time = time()
    print("Execution time multi:", end_time - start_time, "seconds")

    start_time = time()
    a, b, c, d = factorize_single_core(128, 255, 99999, 10651060)
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
    end_time = time()
    print("Execution time factorize_single_core:", end_time - start_time, "seconds")