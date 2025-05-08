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
    return sum(is_prime(i) for i in range(start, end))


def threaded_count_primes(n: int, num_threads: int) -> int:
    threads = []  # List to store thread objects
    results = [0] * num_threads  # Shared list to store results from each thread

    # Worker function
    def count_primes_in_range(thread_id: int) -> None:
        count = 0
        for i in range(thread_id, n, num_threads):  # Round-robin allocation
            if is_prime(i):
                count += 1
        results[thread_id] = count

    # Create and start threads
    for i in range(num_threads):
        thread = threading.Thread(target=count_primes_in_range, args=(i,))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Sum the results from all threads
    return sum(results)


if __name__ == '__main__':
    main()
