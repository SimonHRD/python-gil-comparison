import pytest

from src.prime_counter import is_prime, count_primes, threaded_count_primes
 
  
@pytest.mark.parametrize("n,expected", [(4, False), (5, True), (2, True), (0, False)])
def test_is_prime(n, expected):
    assert is_prime(n) == expected

@pytest.mark.parametrize("n,expected", [(10, 4), (1000, 168)])
def test_count_primes(n, expected):
    assert count_primes(1,n) == expected

@pytest.mark.parametrize("n,threads,expected", [(10, 1, 4), (1000, 1, 168), (10, 3, 4), (1000, 4, 168)])
def test_threaded_count_primes(n, threads, expected):
    assert threaded_count_primes(n, threads) == expected
