import random
import numpy as np

# Define card suits and ranks
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

# Create a deck of cards
deck = [(rank, suit) for suit in suits for rank in ranks]


# Define the Hearts game environment
class HeartsGame:
    def __init__(self, num_players):
        self.num_players = num_players
        self.player_hands = [deck[i::num_players] for i in range(num_players)]
        self.trick = []
        self.trick_suit = None
        self.current_player = 0

    def play_card(self, card_idx):
        played_card = self.player_hands[self.current_player].pop(card_idx)
        self.trick.append(played_card)

        if not self.trick_suit:
            self.trick_suit = played_card[1]

        self.current_player = (self.current_player + 1) % self.num_players

    def get_legal_moves(self):
        legal_moves = []
        for card_idx, card in enumerate(self.player_hands[self.current_player]):
            if not self.trick_suit or card[1] == self.trick_suit:
                legal_moves.append(card_idx)
        if len(legal_moves) == 0:
            legal_moves = list(range(len(self.player_hands[self.current_player])))
        return legal_moves

    def get_state(self):
        state = tuple(sorted(self.player_hands[self.current_player], key=lambda card: (card[1], card[0])))
        return state


# Define a Q-learning based agent
class QLearningAgent:
    def __init__(self, num_actions, learning_rate=0.1, discount_factor=0.9, exploration_prob=0.1):
        self.num_actions = num_actions
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_prob = exploration_prob
        self.q_table = {}

    def choose_move(self, state, legal_moves):
        if random.uniform(0, 1) < self.exploration_prob:
            return random.choice(legal_moves)
        else:
            q_values = [self.q_table.get((state, action), 0) for action in range(self.num_actions)]
            return np.argmax(q_values)

    def update_q_table(self, state, action, reward, next_state):
        current_q = self.q_table.get((state, action), 0)
        max_next_q = max([self.q_table.get((next_state, next_action), 0) for next_action in range(self.num_actions)])
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * max_next_q - current_q)
        self.q_table[(state, action)] = new_q


# Create the Hearts game environment
game = HeartsGame(num_players=4)
num_actions = len(game.player_hands[0])

# Create a Q-learning agent
agent = QLearningAgent(num_actions)
num_episodes = 1000

# Main training loop
for episode in range(num_episodes):
    game = HeartsGame(num_players=4)

    for _ in range(13):  # Play 13 rounds (one for each card)
        for _ in range(game.num_players):
            legal_moves = game.get_legal_moves()
            state = game.get_state()
            chosen_move = agent.choose_move(state, legal_moves)

            game.play_card(chosen_move)
            next_state = game.get_state()

            # Calculate reward (for a simple example, reward could be -1 for each card played)
            reward = -1

            agent.update_q_table(state, chosen_move, reward, next_state)

        # Determine winner of the trick
        winning_card = max(game.trick, key=lambda card: (card[1] == game.trick_suit, ranks.index(card[0])))
        trick_winner = game.trick.index(winning_card)
        print(f"Player {trick_winner + 1} wins the trick!")

        game.trick = []
        game.trick_suit = None

    print(f"Episode {episode + 1} completed.")

print("Training complete! Game over.")