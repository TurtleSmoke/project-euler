import itertools

from sympy import divisors


def is_pentagonal(n):
    return ((1 + (1 + 24 * n) ** 0.5) / 6).is_integer()


def get_divisors(n):
    return filter(
        lambda x: x < n and x % 3 == n % 3, divisors(n * (3 * n - 1))
    )  # Equation 1 and 2


def pentagon_numbers():
    pn = lambda n: n * (3 * n - 1) // 2
    for d in itertools.count(4):
        for r1 in get_divisors(d):  # Equation 4
            r2 = d * (3 * d - 1) // r1
            if r2 % 3 == 2:  # Equation 3
                i = (r1 + (r2 + 1) // 3) / 2
                if i.is_integer():  # Equation 0
                    j = i - r1
                    if is_pentagonal(pn(i) + pn(j)):
                        return pn(d)


if __name__ == "__main__":
    print(pentagon_numbers())
