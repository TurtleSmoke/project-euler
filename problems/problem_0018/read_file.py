def read_file(filename):
    with open(filename, "r") as file:
        return [
            [int(x) for x in line.split(" ")] for line in file.read().split("\n")[:-1]
        ]
