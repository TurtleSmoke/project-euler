def coin_sums(n=200):
    coins = [1, 2, 5, 10, 20, 50, 100, 200]

    def coin_sums_rec(accumulator, minimum_piece):
        if accumulator == n:
            return 1
        if accumulator > n:
            return 0

        return sum(
            coin_sums_rec(accumulator + coins[new_piece], new_piece)
            for new_piece in range(minimum_piece, len(coins))
        )

    return coin_sums_rec(0, 0)


if __name__ == "__main__":
    print(coin_sums(200))
