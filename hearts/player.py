from typing import Set
from hearts import facts


class Player:
    def __init__(self, seat: 'Seat') -> None:
        self.seat: 'Seat' = seat
        self.won: Set['Card'] = set()
        self.hand: Set['Card'] = set()
        self.points: int = 0

    def give(self, p: 'Player', cards: Set['Card']) -> None:
        p.get(cards)
        self.hand -= cards

    def play(self, card: 'Card') -> None:
        self.hand.remove(card)

    def get(self, cards: Set['Card']) -> None:
        self.hand |= cards

    def can_play(self, suit: 'Suit') -> Set['Card']:
        return {c for c in self.hand if c.suit == suit}

    def win(self, cards: Set['Card']) -> None:
        self.won |= cards
        for c in cards:
            if c.suit == facts.SUIT.HEARTS:
                self.points += 1
            elif c.face == facts.FACE.QUEEN and c.suit == facts.SUIT.SPADES:
                self.points += 13

    def end_round(self) -> None:
        self.won = set()
        self.hand = set()
        self.points = 0

    def start_round(self, hand: Set['Card']) -> None:
        self.hand = hand
