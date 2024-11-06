def sub_string_divisibility():
    digits = "0123456789"
    items = [
        x + y for x in digits for y in digits if x != y
    ]  # Permutations of 2 digits

    for d in [17, 13, 11, 7, 5, 3, 2]:
        items = [
            y + x
            for x in items
            for y in digits
            if int((y + x)[:3]) % d == 0 and y not in x
        ]  # Concatenation at the beginning

    items = [
        int(y + x) for x in items for y in digits[1:] if y not in x
    ]  # Last concatenation

    return sum(items)


if __name__ == "__main__":
    print(sub_string_divisibility())
