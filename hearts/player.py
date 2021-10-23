from typing import Set, Tuple, Callable
from hearts import facts, utils
from hearts.card import Card

# Methods for giving and playing
# Give
THREE_CARDS = Tuple['Card', 'Card', 'Card']
GIVE_F = Callable[['Player', 'Player'], THREE_CARDS]


def input_give(self, player: 'Player') -> THREE_CARDS:
    print(f'Hand: {self.hand}')
    give = None
    while give is None:
        s = input(f'Input three cards as separated by a space to give to {player.seat}.\\'
                  f'For example, "CA HQ S10" would give the Ace of Clubs, Queen of Hearts and the 10 of spades.')
        try:
            cards = utils.str_to_card(s)
            if len(cards) == 3 and all(c in self.hand for c in cards):
                give = tuple(cards)
        except:
            print("Invalid input.")
    return give


def random_give(self, player: 'Player') -> THREE_CARDS:
    return tuple(self.hand)[:3]


# Play
PLAY_F = Callable[['Suit', bool, bool], 'card']


def input_move(self, lead: 'Suit', broke_hearts: bool, is_first: bool) -> 'Card':
    play = None
    print(f'Hand: {self.hand}')
    valid_cards = self.can_play(lead, broke_hearts, is_first)
    print(f'Valid: {valid_cards}')
    while play is None:
        s = input(f'Input a valid card from your hand to play.\\For example, "HQ" would give the Queen of Hearts.')
        try:
            card = utils.str_to_card(s)
            if len(card) == 1 and card[0] in valid_cards:
                play, *_ = card
        except:
            print("Invalid input.")
    return play


def random_play(self, lead: 'Suit', broke_hearts: bool, is_first: bool) -> 'Card':
    return next(iter(self.can_play(lead, broke_hearts, is_first)))


class Player:
    def __init__(self, seat: 'Seat', play_func: PLAY_F = random_play, give_func: GIVE_F = random_give) -> None:
        self.seat: 'Seat' = seat
        self.won: Set['Card'] = set()
        self.hand: Set['Card'] = set()
        self.score: int = 0

        self.select_play: PLAY_F = play_func
        self.select_give: GIVE_F = give_func

    def give(self, p: 'Player', cards: Set['Card']) -> None:
        p.get(cards)
        self.hand -= cards

    def play(self, card: 'Card') -> None:
        self.hand.remove(card)

    def get(self, cards: Set['Card']) -> None:
        self.hand |= cards

    def can_play(self, broke_hearts: bool, suit: 'Suit', first_turn: bool = False) -> Set['Card']:
        if suit is None:
            if first_turn:
                assert facts.TWO_OF_CLUBS in self.hand, "Two of Clubs not in hand."
                cards = {facts.TWO_OF_CLUBS}
            elif broke_hearts:
                cards = self.hand
            else:
                cards = {c for c in self.hand if c.suit != facts.SUIT.HEARTS}
        else:
            cards = {c for c in self.hand if c.suit == suit}
            if len(cards) == 0:
                cards = {c for c in self.hand if c.suit != facts.SUIT and c != facts.QUEEN_OF_SPADES}
                if len(cards) == 0:
                    cards = self.hand
        return cards

    def win(self, cards: Set['Card']) -> None:
        self.won |= cards
        for c in cards:
            if c.suit == facts.SUIT.HEARTS:
                self.score += 1
            elif c == facts.QUEEN_OF_SPADES:
                self.score += 13

    def end_round(self) -> None:
        self.won = set()
        self.hand = set()
        self.score = 0

    def start_round(self, hand: Set['Card']) -> None:
        self.hand = hand
