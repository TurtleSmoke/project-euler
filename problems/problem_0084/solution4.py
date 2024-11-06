import numpy as np

# Constants
NUM_SQUARES = 40
NUM_DICE_SIDES = 4

# Square indices
GO, JAIL, G2J = 0, 10, 30
C1, E3, H2, R1 = 11, 24, 39, 5
CC = [2, 17, 33]
CH = [7, 22, 36]
RAILWAY = [5, 15, 25, 35]
UTILITY = [12, 28]

def next_square_in_list(position, squares):
    for square in squares:
        if square > position:
            return square
    return squares[0]


def create_transition_matrix():
    P = np.zeros((NUM_SQUARES, NUM_SQUARES))

    for i in range(NUM_SQUARES):
        for j in range(2, 2 * NUM_DICE_SIDES + 1):
            next_square = (i + j) % NUM_SQUARES
            prob = sum(
                1
                for d1 in range(1, NUM_DICE_SIDES + 1)
                for d2 in range(1, NUM_DICE_SIDES + 1)
                if d1 + d2 == j
            ) / (NUM_DICE_SIDES ** 2)

            if next_square in CC:
                P[i, GO] += prob * (1 / 16)
                P[i, JAIL] += prob * (1 / 16)
                P[i, next_square] += prob * (14 / 16)
            elif next_square in CH:
                P[i, GO] += prob * (1 / 16)
                P[i, JAIL] += prob * (1 / 16)
                P[i, C1] += prob * (1 / 16)
                P[i, E3] += prob * (1 / 16)
                P[i, H2] += prob * (1 / 16)
                P[i, R1] += prob * (1 / 16)
                P[i, next_square] += prob * (6 / 16)

                P[i, next_square_in_list(next_square, RAILWAY)] += prob * (2 / 16)
                P[i, next_square_in_list(next_square, UTILITY)] += prob * (1 / 16)
                P[i, next_square - 3] += prob * (1 / 16)
            elif next_square == G2J:
                P[i, JAIL] += prob
            else:
                P[i, next_square] += prob

    # Adjust for "Go to Jail" on three consecutive doubles
    doubles_prob = 1 / NUM_DICE_SIDES
    triple_doubles_prob = doubles_prob ** 3
    for i in range(NUM_SQUARES):
        P[i, JAIL] += triple_doubles_prob
        P[i, :] *= 1 - triple_doubles_prob

    return P


def power_method(P, max_iter=1000, tol=1e-8):
    x = np.ones(NUM_SQUARES) / NUM_SQUARES
    for _ in range(max_iter):
        x_new = x @ P
        if np.allclose(x, x_new, rtol=tol):
            return x_new
        x = x_new
    return x


# Create the transition matrix
P = create_transition_matrix()
# Print sum of row
print(np.sum(P, axis=1))

stationary_distribution = power_method(P)
top_3_indices = np.argsort(stationary_distribution)[-3:][::-1]
modal_string = "".join(f"{index:02d}" for index in top_3_indices)
print(f"\nThe six-digit modal string is: {modal_string}")
for i, index in enumerate(np.argsort(stationary_distribution)[::-1], 1):
    print(f"{i}. Square {index:02d}: {stationary_distribution[index]:.2%}")
