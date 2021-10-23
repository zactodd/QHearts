from hearts import facts
from hearts.player import Player
from typing import Dict
from collections import Counter
from itertools import cycle
from hearts.round import Round


class Game:
    def __init__(self) -> None:
        self._seat_players: Dict['Seat': Player] = {s: Player(s) for s in facts.SEATS}
        self._seat_score = Counter({s: 0 for s in facts.SEATS})
        self.players = set(self._seat_players.values())

    def get_player(self, seat: 'Seat') -> 'Player':
        return self._seat_players[seat]

    def score_round(self):
        update = {}
        for p in self.players:
            if p.score == 26:
                update = {p.seat: 26 for p in self.players}
                update[p.seat] = 0
                break
            else:
                update[p] = p.score
        self._seat_score += update

        for p in self.players:
            p.end_round()

    def play_game(self, verbose=True):
        directions = cycle(iter(facts.DIRECTION))
        rounds = 0
        while all(s < 100 for s in self._seat_score.values()):
            Round(self.players, next(directions)).play_round(False)
            self.score_round()
            if verbose:
                print(f'{rounds}: {self}')
                rounds += 1

    def __repr__(self) -> str:
        return ', '.join(f'{s.name}: {self._seat_score[self.get_player(s)]}' for s in facts.SEATS)


