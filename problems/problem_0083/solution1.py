from read_file import read_file


def bfs(matrix, source):
    updated = [
        [float("inf") for _ in range(len(matrix[0]))] for _ in range(len(matrix))
    ]
    updated[0][0] = matrix[0][0]
    queue = [source]

    while queue:
        i, j = queue.pop(0)
        for x, y in [(i, j + 1), (i, j - 1), (i + 1, j), (i - 1, j)]:
            if 0 <= x < len(matrix) and 0 <= y < len(matrix[0]):
                alt = updated[i][j] + matrix[x][y]
                if alt < updated[x][y]:
                    updated[x][y] = alt
                    queue.append((x, y))

    return updated


def path_sum_four_ways(filename="matrix.txt"):
    matrix = read_file(filename)
    return bfs(matrix, (0, 0))[-1][-1]


if __name__ == "__main__":
    print(path_sum_four_ways())
