from hearts import facts
import numpy as np


# 16 * 52 space
# 0 - 12 is each turn
# 13 given
# 14 recived
# 15 hand
# def obs_round_encoder(player, round):
#     state = np.zeros((16, 52))
#     seat_adj = facts.SEATS.NORTH.value - player.seat.value
#     for i, t in enumerate(round.turns):
#         for p, c in t.items():
#             state[i, facts.DECK.index(c)] = (p.seat.value + seat_adj) % 4
#
#     for c in player.hand:
#         state[15, facts.DECK.index(c)] = 1
#
#     if round.gives:
#         if player in round.gives:
#             for c in round.gives[player][1]:
#                 state[13, facts.DECK.index(c)] = round.direction.value % 4
#         p = round.player_seats[facts.SEATS((player.seat.value - round.direction.value) % 4).value]
#         for c in round.gives[p][1]:
#             state[14, facts.DECK.index(c)] = (-round.direction.value) % 4
#     return state


# 2 * 52
# 1 round played
# 2 0-3: card played, 4-7: card give, 8-11: card received, 12: card in hand.
def obs_round_encoder(player, round):
    state = np.zeros((2, 52))
    seat_adj = facts.SEATS.NORTH.value - player.seat.value
    for i, t in enumerate(round.turns):
        for p, c in t.items():
            state[[0, 1], facts.DECK.index(c)] = i, (p.seat.value + seat_adj) % 4

    if round.gives:
        if player in round.gives:
            for c in round.gives[player][1]:
                state[1, facts.DECK.index(c)] = 8 + (round.direction.value % 4)
        p = round.player_seats[facts.SEATS((player.seat.value - round.direction.value) % 4).value]
        for c in round.gives[p][1]:
            state[1, facts.DECK.index(c)] = 4 + ((-round.direction.value) % 4)

    for c in player.hand:
        state[1, facts.DECK.index(c)] = 12
    return state
