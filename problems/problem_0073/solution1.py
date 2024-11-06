def stern_brocot_tree(a, b, c, d):
    if b + d > 12000:
        return 0

    return (
        1
        + stern_brocot_tree(a, b, a + c, b + d)
        + stern_brocot_tree(a + c, b + d, c, d)
    )


def counting_fractions_in_a_range():
    return stern_brocot_tree(1, 3, 1, 2)


if __name__ == "__main__":
    print(counting_fractions_in_a_range())
