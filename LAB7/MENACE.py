import random

class MENACE:
    def __init__(self):
        self.matchboxes = {}
        self.learning_rate = 1  
        self.game_history = [] 

    def get_state(self, board):
        return tuple(board)

    def choose_move(self, game):
        board = game.board
        state = self.get_state(board)
        
        if state not in self.matchboxes:
            possible_moves = game.get_possible_moves()
            self.matchboxes[state] = {move: 3 for move in possible_moves} 

        moves = list(self.matchboxes[state].keys())
        beads = list(self.matchboxes[state].values())
        move = random.choices(moves, weights=beads, k=1)[0]
        
        self.game_history.append((state, move))
        return move

    def update_matchboxes(self, result):
        reward = self.learning_rate if result == 'win' else -self.learning_rate if result == 'lose' else 0
        
        for state, move in self.game_history:
            if move in self.matchboxes[state]:
                self.matchboxes[state][move] = max(1, self.matchboxes[state][move] + reward)
        
        self.game_history.clear()

    def reset(self):
        self.game_history = []

class TicTacToe:
    def __init__(self):
        self.board = [0] * 9 
        self.winner = None

    def display_board(self):
        symbols = {0: ' ', 1: 'X', 2: 'O'}
        for row in range(3):
            print("|".join(symbols[self.board[i]] for i in range(row * 3, (row + 1) * 3)))
            if row < 2:
                print("-----")

    def make_move(self, position, player):
        if self.board[position] == 0:
            self.board[position] = player
            return True
        return False

    def check_winner(self):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  
            [0, 3, 6], [1, 4, 7], [2, 5, 8], 
            [0, 4, 8], [2, 4, 6]  
        ]
        
        for combo in winning_combinations:
            if self.board[combo[0]] != 0 and self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]]:
                self.winner = self.board[combo[0]]
                return self.winner
        
        if 0 not in self.board:
            self.winner = 0
            return 0
        
        return None

    def get_possible_moves(self):
        return [i for i, value in enumerate(self.board) if value == 0]

    def reset(self):
        self.board = [0] * 9
        self.winner = None

def play_game(menace, opponent_random=True):
    game = TicTacToe()
    current_player = 1  
    menace.reset()

    while game.winner is None:
        if current_player == 1:
            move = menace.choose_move(game)
            game.make_move(move, current_player)
        else:
            if opponent_random:
                available_moves = game.get_possible_moves()
                move = random.choice(available_moves)
                game.make_move(move, current_player)

        game.check_winner()
        current_player = 3 - current_player  

    if game.winner == 1:
        menace.update_matchboxes('win')
    elif game.winner == 2:
        menace.update_matchboxes('lose')
    else:
        menace.update_matchboxes('draw')

    return game.winner

menace = MENACE()

for episode in range(1000):
    result = play_game(menace)
    if episode % 10 == 0:
        print(f"Game {episode}: Result = {'MENACE wins' if result == 1 else 'Opponent wins' if result == 2 else 'Draw'}")
