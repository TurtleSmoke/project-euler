from read_file import read_file


def names_scores(filename):
    names = read_file(filename).sort()
    return sum(
        (i + 1) * sum(ord(c) - ord("A") + 1 for c in name)
        for (i, name) in enumerate(names)
    )


if __name__ == "__main__":
    print(names_scores("given.txt"))
