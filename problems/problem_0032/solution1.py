def is_pandigital(multiplicand, multiplier, product):
    return sorted(str(multiplicand) + str(multiplier) + str(product)) == list(
        "123456789"
    )


def is_pandigital2(multiplicand, multiplier, product):
    digits = []
    for n in (multiplier, multiplicand, product):
        while n:
            digits.append(n % 10)
            n //= 10

    return 0 not in digits and len(digits) == 9 and len(set(digits)) == 9


def is_pandigital3(multiplicand, multiplier, product):
    digits = 0
    for n in (multiplicand, multiplier, product):
        while n:
            if digits & (1 << (n % 10)):
                return False
            digits |= 1 << (n % 10)
            n //= 10

    return digits == 0b1111111110


def pandigital_products():
    products = set()
    for i in range(1, 100):
        for j in range(100 if i > 9 else 1000, 10000 // i + 1):
            if is_pandigital3(i, j, i * j):
                products.add(i * j)

    return sum(products)


if __name__ == "__main__":
    print(pandigital_products())
