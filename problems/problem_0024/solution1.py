def lexicographic_permutations(s):
    if len(s) <= 1:
        yield s
    else:
        for i in range(len(s)):
            for p in lexicographic_permutations(s[:i] + s[i + 1 :]):
                yield s[i] + p


if __name__ == "__main__":
    print(
        next(
            res
            for i, res in enumerate(lexicographic_permutations("0123456789"))
            if i == 999999
        )
    )
