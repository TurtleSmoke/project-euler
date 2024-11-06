from read_file import read_file


def is_triangle_number(x):
    return (((1 + 8 * x) ** 0.5 - 1) / 2).is_integer()


def coded_triangle_numbers():
    words = read_file("words.txt")
    return sum(
        is_triangle_number(sum(ord(c) - ord("A") + 1 for c in word)) for word in words
    )


if __name__ == "__main__":
    print(coded_triangle_numbers())
