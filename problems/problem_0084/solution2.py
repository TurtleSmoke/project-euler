import numpy as np

# Define constants
NUM_SQUARES = 40
NUM_DICE_SIDES = 4
NUM_SIMULATIONS = 1000000

# Define square indices
GO = 0
JAIL = 10
G2J = 30
C1 = 11
E3 = 24
H2 = 39
R1 = 5
CC = [2, 17, 33]
CH = [7, 22, 36]
RAILWAY = [5, 15, 25, 35]
UTILITY = [12, 28]


def roll_dice():
    return np.random.randint(1, NUM_DICE_SIDES + 1, 2)


def next_square(position, squares):
    for square in squares:
        if square > position:
            return square
    return squares[0]  # Wrap around to the first square if we've passed the last one


def next_railway(position):
    return next_square(position, RAILWAY)


def next_utility(position):
    return next_square(position, UTILITY)


def community_chest(position):
    card = np.random.randint(16)
    if card == 0:
        return GO
    elif card == 1:
        return JAIL
    return position


def chance(position):
    card = np.random.randint(16)
    if card == 0:
        return GO
    elif card == 1:
        return JAIL
    elif card == 2:
        return C1
    elif card == 3:
        return E3
    elif card == 4:
        return H2
    elif card == 5:
        return R1
    elif card == 6 or card == 7:
        return next_railway(position)
    elif card == 8:
        return next_utility(position)
    elif card == 9:
        return (position - 3) % NUM_SQUARES
    return position


def simulate_move(position):
    dice = roll_dice()
    doubles_count = 1 if dice[0] == dice[1] else 0
    new_position = (position + sum(dice)) % NUM_SQUARES

    if new_position in CC:
        new_position = community_chest(new_position)
    elif new_position in CH:
        new_position = chance(new_position)
    elif new_position == G2J:
        new_position = JAIL

    return new_position, doubles_count


def run_simulation():
    position = GO
    doubles_count = 0
    visits = np.zeros(NUM_SQUARES, dtype=int)

    for _ in range(NUM_SIMULATIONS):
        new_position, new_doubles = simulate_move(position)

        if new_doubles:
            doubles_count += 1
            if doubles_count == 3:
                new_position = JAIL
                doubles_count = 0
        else:
            doubles_count = 0

        visits[new_position] += 1
        position = new_position

    return visits


visit_counts = run_simulation()
probabilities = visit_counts / NUM_SIMULATIONS
top_3_indices = np.argsort(probabilities)[-3:][::-1]
modal_string = "".join(f"{index:02d}" for index in top_3_indices)

print(f"The six-digit modal string is: {modal_string}")
print("\nTop 10 most visited squares:")
for i, index in enumerate(np.argsort(probabilities)[-10:][::-1], 1):
    print(f"{i}. Square {index:02d}: {probabilities[index]:.2%}")
