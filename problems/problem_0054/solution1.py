from collections import Counter
from enum import Enum

from read_file import read_file


class Hand(Enum):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    STRAIGHT_FLUSH = 9
    ROYAL_FLUSH = 10

    def __lt__(self, other):
        return self.value < other.value


class Card(Enum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14

    def __lt__(self, other):
        return self.value < other.value

    @classmethod
    def from_string(cls, string):
        return cls(
            {
                "2": cls.TWO,
                "3": cls.THREE,
                "4": cls.FOUR,
                "5": cls.FIVE,
                "6": cls.SIX,
                "7": cls.SEVEN,
                "8": cls.EIGHT,
                "9": cls.NINE,
                "T": cls.TEN,
                "J": cls.JACK,
                "Q": cls.QUEEN,
                "K": cls.KING,
                "A": cls.ACE,
            }[string]
        )


class Suit(Enum):
    DIAMONDS = 1
    CLUBS = 2
    HEARTS = 3
    SPADES = 4

    @classmethod
    def from_string(cls, string):
        return cls(
            {
                "D": cls.DIAMONDS,
                "C": cls.CLUBS,
                "H": cls.HEARTS,
                "S": cls.SPADES,
            }[string]
        )


def get_hand(hand):
    values = sorted([Card.from_string(card[0]) for card in hand])
    occ, values = zip(
        *sorted(((v, k) for k, v in Counter(values).items()), reverse=True)
    )

    is_straight = all(
        values[i].value == values[i + 1].value + 1 for i in range(len(values) - 1)
    )
    is_flush = len(set(card[1] for card in hand)) == 1

    if occ == (4, 1):
        hand = Hand.FOUR_OF_A_KIND
    elif occ == (3, 2):
        hand = Hand.FULL_HOUSE
    elif occ == (3, 1, 1):
        hand = Hand.THREE_OF_A_KIND
    elif occ == (2, 2, 1):
        hand = Hand.TWO_PAIR
    elif occ == (2, 1, 1, 1):
        hand = Hand.ONE_PAIR
    elif is_straight and is_flush and values[0] == Card.ACE:
        hand = Hand.ROYAL_FLUSH
    elif is_straight and is_flush:
        hand = Hand.STRAIGHT_FLUSH
    elif is_flush:
        hand = Hand.FLUSH
    elif is_straight:
        hand = Hand.STRAIGHT
    elif occ == (1, 1, 1, 1, 1):
        hand = Hand.HIGH_CARD
    else:
        raise ValueError("Invalid hand")

    return hand, *values


def poker_hands(file):
    return sum(get_hand(hand[:5]) > get_hand(hand[5:]) for hand in read_file(file))


if __name__ == "__main__":
    print(poker_hands("poker.txt"))
