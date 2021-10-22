from typing import Set, Tuple
from hearts import facts, utils


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

    def input_give(self, player: 'Player') -> Tuple['Card', 'Card', 'Card']:
        give = None
        while give is None:
            s = input(f'Input three cards as separated by a space to give to {player.seat}.\\'
                      f'For example, "CA HQ S10" would give the Ace of Clubs, Queen of Hearts and the 10 of spades.')
            try:
                cards = utils.str_to_card(s)
                if len(cards) == 3:
                    give = tuple(cards)
            except:
                pass
        return give

    def random_give(self, player: 'Player') -> Tuple['Card', 'Card', 'Card']:
       return tuple(self.hand)[:3]


