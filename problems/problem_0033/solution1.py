from math import gcd


def is_curious_fraction(numerator, denominator):
    if numerator % 10 == denominator // 10:
        return (
            abs((numerator / denominator) - (numerator // 10 / (denominator % 10)))
            < 0.0000001
        )
    elif numerator // 10 == denominator % 10:
        return (
            abs((numerator / denominator) - (numerator % 10 / (denominator // 10)))
            < 0.0000001
        )
    return False


def digit_cancelling_fractions():
    final_numerator, final_denominator = 1, 1
    for numerator in range(10, 100):
        for denominator in range(numerator + 1, 100):
            if numerator % 10 == 0 or denominator % 10 == 0:
                continue
            if is_curious_fraction(numerator, denominator):
                final_numerator *= numerator
                final_denominator *= denominator

    return final_denominator // gcd(final_numerator, final_denominator)


if __name__ == "__main__":
    print(digit_cancelling_fractions())
