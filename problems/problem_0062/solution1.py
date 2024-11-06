import itertools


def is_cube(n):
    return (round(n ** (1 / 3)) ** 3) == n


def cubic_permutations():
    for cube in (i**3 for i in itertools.count(1)):  # Condition 1
        cubes = {cube}

        for p in itertools.permutations(str(cube)):  # Condition 2
            new_cube = int("".join(p))
            if (
                p[0] != "0" and is_cube(new_cube) and new_cube not in cubes
            ):  # Condition 3
                cubes.add(new_cube)
        if len(cubes) >= 5:  # Condition 4
            return min(cubes)


if __name__ == "__main__":
    print(cubic_permutations())
