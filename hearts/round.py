from hearts import utils, facts


class Round:
    def __init__(self, game: 'Game', direction: 'DIRECTION') -> None:
        self.game = game
        self.direction = direction
        self.broken_hearts: bool = False

    def play_round(self, verbose: bool = True) -> None:
        self._deal_cards(verbose=verbose)
        self._give(verbose=verbose)
        lead_seat = next((p.seat for p in self.game.players if facts.TWO_OF_CLUBS in p.hand))
        seat = self._turn(lead_seat, True, verbose=verbose)
        for _ in range(12):
            seat = self._turn(seat, verbose=verbose)

        if verbose:
            print('Round Score: ' + ', '.join(f'{s.name}: {self.game.get_player(s).score}' for s in facts.SEATS))

    def _deal_cards(self, verbose: bool = True) -> None:
        d = utils.shuffle_deck()
        for i, s in enumerate(facts.SEATS):
            i *= 13
            hand = set(d[i:i + 13])

            if verbose:
                print(f'{s.name}: {sorted(hand)}')

            self.game.get_player(s).start_round(hand)

    def _give(self, verbose: bool = True):
        if verbose:
            print(f'{self.direction.name}:')

        if self.direction == facts.DIRECTION.KEEP:
            self.gives = tuple()
        else:
            self.gives = tuple((s, self.direction.value) for s in facts.SEATS)

        give_cards = []
        for g, dr in self.gives:
            s = facts.SEATS((g.value + dr) % 4)
            give_cards.append((g, s, self.game.get_player(g).select_give(s)))

        for g, r, cards in give_cards:
            self.game.get_player(g).give(self.game.get_player(r), cards)
            if verbose:
                print(f'\t{g.name} -> {r.name}: {sorted(cards)}')

    def _turn(self, lead_seat: 'Seat', is_first: bool = False, verbose: bool = True) -> 'Seat':
        starting_player = self.game.get_player(lead_seat)
        card = starting_player.select_play(None, self.broken_hearts, is_first)

        if verbose:
            print(f'{lead_seat.name}, Starting\n'
                  f'\tHand: {sorted(starting_player.hand)}\n'
                  f'\tValid: {sorted(starting_player.can_play(None, self.broken_hearts, is_first))}\n'
                  f'\t\t-> {card}')

        starting_player.play(card)

        lead_suit = card.suit
        played_cards = {starting_player: card}
        for i in range(1, 4):
            seat = facts.SEATS((i + lead_seat.value) % 4)

            player = self.game.get_player(seat)
            card = player.select_play(lead_suit, self.broken_hearts, is_first)

            if verbose:
                print(f'{seat.name}, Played: {sorted(played_cards.values())}\n'
                      f'\tHand: {sorted(player.hand)}\n'
                      f'\tValid: {sorted(player.can_play(lead_suit, self.broken_hearts, is_first))}\n'
                      f'\t\t-> {card}')

            player.play(card)
            played_cards.update({player: card})

        if not self.broken_hearts:
            self.broken_hearts = any(c.face == facts.SUIT.HEARTS for c in played_cards.values())

        winner = max(self.game.players, key=lambda p: utils.score_card(lead_suit, played_cards[p]))
        winner.win(set(played_cards.values()))

        if verbose:
            print(f'Won: {winner.seat.name} -> {played_cards[winner]}, {sorted(played_cards.values())}')

        return winner.seat












