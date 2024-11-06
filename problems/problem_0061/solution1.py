def find_cycle(first_two_digits, is_polygonals, cycle):
    if not is_polygonals:
        if cycle[0] // 100 == cycle[-1] % 100:
            return cycle
        return []

    for last_two_digits in range(10, 100):
        p = first_two_digits * 100 + last_two_digits
        for i, is_polygonal in enumerate(is_polygonals):
            if is_polygonal(p):
                new_cycle = find_cycle(
                    last_two_digits,
                    is_polygonals[:i] + is_polygonals[i + 1 :],
                    cycle + [p],
                )
                if new_cycle:
                    return new_cycle

    return []


def cyclical_figurate_numbers():
    is_triangular = lambda n: ((1 + (1 + 8 * n) ** 0.5) / 2).is_integer()
    is_square = lambda n: (n**0.5).is_integer()
    is_pentagonal = lambda n: ((1 + (1 + 24 * n) ** 0.5) / 6).is_integer()
    is_hexagonal = lambda n: ((1 + (1 + 8 * n) ** 0.5) / 4).is_integer()
    is_heptagonal = lambda n: ((3 + (9 + 40 * n) ** 0.5) / 10).is_integer()
    is_octagonal = lambda n: ((1 + (1 + 3 * n) ** 0.5) / 3).is_integer()
    is_polygonals = [
        is_triangular,
        is_square,
        is_pentagonal,
        is_hexagonal,
        is_heptagonal,
        is_octagonal,
    ]

    for i in range(10, 100):
        cycle = find_cycle(i, is_polygonals, [])
        if cycle:
            return sum(cycle)

    return []


if __name__ == "__main__":
    print(cyclical_figurate_numbers())
