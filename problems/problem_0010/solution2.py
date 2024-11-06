from sympy import sieve
from math import sqrt, floor


def phi(x):
    return x * (x + 1) // 2


def tk(n, k, primes):
    pk = primes[k - 1]
    t0 = phi(floor(n / pk))
    tn = sum(tk(n / pk, i, primes) for i in range(1, k))
    return pk * (t0 - tn)


def summation_of_primes(limit=2000):
    primes = list(sieve.primerange(floor(sqrt(limit)) + 1))

    return (
        phi(limit)
        - sum(tk(limit, i + 1, primes) for i in range(len(primes)))
        + sum(primes)
        - 1
    )


if __name__ == "__main__":
    print(summation_of_primes())
