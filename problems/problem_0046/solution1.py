import itertools

from sympy import isprime


def is_odd_goldbach(n):
    return any(
        isprime(i) and (((n - i) / 2) ** 0.5).is_integer() for i in range(1, n + 1)
    )


def goldbachs_other_conjecture():
    for i in itertools.count(7, 2):
        if not is_odd_goldbach(i):
            return i


if __name__ == "__main__":
    print(goldbachs_other_conjecture())
