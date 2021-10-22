from enum import Enum
from hearts.card import Card


class SUIT(Enum):
    CLUBS = 'CLUBS'
    SPADES = 'SPADES'
    HEARTS = 'HEARTS'
    DIAMONDS = 'DIAMONDS'


class FACE(Enum):
    ACE = 'A'
    TWO = '2'
    THREE = '3'
    FOUR = '4'
    FIVE = '5'
    SIX = '6'
    SEVEN = '7'
    EIGHT = '8'
    NINE = '9'
    TEN = '10'
    JACK = 'J'
    QUEEN = 'Q'
    KING = 'K'


DECK = tuple(Card(f, s) for f in FACE for s in SUIT)
