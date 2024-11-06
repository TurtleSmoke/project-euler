def totient_list(n):
    tlist = list(range(n))
    for i in range(1, n):
        p = tlist[i]
        for j in range(2 * i, n, i):
            tlist[j] -= p
    return tlist


def totient_permutation(limit=10000001):
    totatives = totient_list(limit)
    totatives = (
        (n, t)
        for n, t in enumerate(totatives)
        if sorted(str(n)) == sorted(str(t)) and n > 1
    )
    return min(totatives, key=lambda x: x[0] / x[1])[0]


if __name__ == "__main__":
    print(totient_permutation())
