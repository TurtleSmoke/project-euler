import itertools

from sympy import isprime


def spiral_primes():
    res = 0
    for i in itertools.count(3, 2):
        res += (
            isprime(i**2)
            + isprime(i**2 - (i - 1))
            + isprime(i**2 - 2 * (i - 1))
            + isprime(i**2 - 3 * (i - 1))
        )
        if res < (2 * i - 1) / 10:
            return i


if __name__ == "__main__":
    print(spiral_primes())
