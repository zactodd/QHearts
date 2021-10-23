from hearts import facts
import numpy as np


# 16 * 52 space
# 0 - 12 is each turn
# 13 given
# 14 recived
# 15 hand
def obs_round_encoder(player, round):
    state = np.zeros((16, 52))
    seat_adj = facts.SEATS.NORTH.value - player.seat.value
    for i, t in enumerate(round.turns):
        for p, c in t.items():
            state[i, facts.DECK.index(c)] = (p.seat.value + seat_adj) % 4

    for c in player.hand:
        state[13, facts.DECK.index(c)] = 1

    if round.gives:
        for c in round.gives[player]:
            state[13, facts.DECK.index(c)] = round.direction.value % 4
        for c in round.gives[round.player_seats[facts.SEATS((player.seat.value - round.direction.value) % 4)]]:
            state[14, facts.DECK.index(c)] = (-round.direction.value) % 4
    return state
