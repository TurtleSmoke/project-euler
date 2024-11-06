import itertools


def ring_to_string(inner, outer):
    start = outer.index(min(outer))
    return "".join(
        (
            str(outer[i % 5]) + str(inner[i % 5]) + str(inner[(i + 1) % 5])
            for i in range(start, start + 5)
        )
    )


def is_gon_valid(inner, outer):
    return len(set(inner[i] + inner[(i + 1) % 5] + outer[i] for i in range(5))) == 1


def magic_5_gon_ring():
    all_gons = itertools.permutations(range(1, 11))  # Condition 1
    valid_gons = filter(
        lambda gon: is_gon_valid(gon[:5], gon[5:]), all_gons
    )  # Condition 2
    string_gons = map(lambda gon: ring_to_string(gon[:5], gon[5:]), valid_gons)
    string_gons = filter(lambda gon: len(gon) == 16, string_gons)  # Condition 3
    res = max(string_gons)  # Condition 4
    return res


if __name__ == "__main__":
    print(magic_5_gon_ring())
