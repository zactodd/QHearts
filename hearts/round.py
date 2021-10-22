from hearts import utils, facts


class Round:
    def __init__(self, game: 'Game', direction: 'DIRECTION') -> None:
        self.game = game
        self.direction = direction

        d = utils.shuffle_deck()
        for i, p in enumerate(facts.SEATS):
            i *= 13
            game.player(p).start_rounf(set(d[i:i + 13]))

        if self.direction == facts.DIRECTION.KEEP:
            self.gives = tuple()
        else:
            self.gives = tuple((s, self.direction.value) for s in facts.SEATS)

        give_cards = []
        for g, dr in self.gives:
            s = facts.SEATS((g.value + dr) % 4)
            # give_cards.append(game.player(s).input_give())
            give_cards.append((g, s, game.player(s).random_give()))

        for g, r, cards in give_cards:
            game.player(g).give(r, cards)

        

