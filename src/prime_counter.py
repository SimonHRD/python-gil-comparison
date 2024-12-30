import threading
import time


def main():
    UPPER_LIMIT = 10**6  # Maximum number to check
    NUM_THREADS = 4
    
    # Single threaded
    start_time = time.time()
    result = count_primes(0, UPPER_LIMIT)
    end_time = time.time()
    print(f"Single-threaded execution time: {end_time - start_time:.2f} seconds, primes found: {result}")
    
    # Multi threaded
    start_time = time.time()
    result = threaded_count_primes(UPPER_LIMIT, NUM_THREADS)
    end_time = time.time()
    print(f"Multi-threaded ({NUM_THREADS} threads) execution time: {end_time - start_time:.2f} seconds, primes found: {result}")

    
def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


def count_primes(start: int, end: int) -> int:
    return sum([is_prime(i) for i in range(start, end)])


def threaded_count_primes(n: int, num_threads: int) -> int:
    threads = []  # List to store thread objects
    results = [0] * num_threads  # Shared list to store results from each thread

    # Worker function to count primes in a given range
    def count_primes_in_range(start: int, end: int, index: int) -> None:
        results[index] = count_primes(start, end)

    # Helper function to calculate ranges for each thread
    def calculate_ranges(n: int, num_threads: int):
        step = n // num_threads
        for i in range(num_threads):
            start = i * step
            # Ensure the last thread includes any leftover range
            end = (i + 1) * step if i != num_threads - 1 else n
            yield start, end, i

    # Create and start threads for each range
    for start, end, index in calculate_ranges(n, num_threads):
        thread = threading.Thread(target=count_primes_in_range, args=(start, end, index))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Sum the results from all threads
    return sum(results)


if __name__ == '__main__':
    main()
