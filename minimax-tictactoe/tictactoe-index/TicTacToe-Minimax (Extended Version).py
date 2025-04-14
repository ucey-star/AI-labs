import numpy as np
import random
import copy
import tkinter as tk
from tkinter import messagebox
from tkinter import font

# Define a TicTacToe reinforcement learning agent
# Define a TicTacToe agent using the minimax algorithm
class TicTacToe_Minimax_Agent:

    # Initialize the agent with a given search depth for the minimax algorithm
    def __init__(self, max_depth=4):
        self.max_depth = max_depth

    # Get a list of available actions (empty cells) in the current state
    @staticmethod
    def get_available_actions(state):
        available_actions = []
        for i in range(4):
            for j in range(4):
                if state[i][j] == 0:
                    available_actions.append((i, j))
        return available_actions

    # Check if the given player has won the game in the current state
    @staticmethod
    def check_winner(state, player):
        for row in state:
            if np.all(row == player):
                return True
        for col in state.T:
            if np.all(col == player):
                return True
        if np.all(np.diag(state) == player) or np.all(np.diag(np.fliplr(state)) == player):
            return True
        return False

    # Update the state by performing an action for the given player
    @staticmethod
    def perform_action(state, action, player):
        new_state = copy.deepcopy(state)
        new_state[action[0]][action[1]] = player
        return new_state

    # Select the best action for the current state using the minimax algorithm
    def make_move(self, state):
        best_action = None
        for depth in range(1, self.max_depth + 1):
            _, current_best_action = self.minimax(state, depth, True, -float("inf"), float("inf"))
            if current_best_action is not None:
                best_action = current_best_action

            # Stop searching if a winning move is found
            if self.eval(self.perform_action(state, best_action, 1)) == 10:
                break

        return best_action
    def heuristic_eval(self, state):
        scores = [0, 0]  # [score for player 1, score for player -1]

        for player in [1, -1]:
            for row in state:
                if np.sum(row == player) == 3 and np.sum(row == 0) == 1:
                    scores[player == 1] += 1

            for col in state.T:
                if np.sum(col == player) == 3 and np.sum(col == 0) == 1:
                    scores[player == 1] += 1

            for diag in [np.diag(state), np.diag(np.fliplr(state))]:
                if np.sum(diag == player) == 3 and np.sum(diag == 0) == 1:
                    scores[player == 1] += 1

        return scores[0] - scores[1]

    # Implementation of the minimax algorithm with alpha-beta pruning
    def minimax(self, state, depth, maximizing_player, alpha, beta):
        if depth == 0 or self.check_winner(state, 1) or self.check_winner(state, -1) or not self.get_available_actions(state):
            return self.eval(state), None

        if maximizing_player:
            max_eval = -float("inf")
            best_action = None
            for action in self.get_available_actions(state):
                new_state = self.perform_action(state, action, 1)
                eval_score, _ = self.minimax(new_state, depth - 1, False, alpha, beta)
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_action = action
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval, best_action
        else:
            min_eval = float("inf")
            best_action = None
            for action in self.get_available_actions(state):
                new_state = self.perform_action(state, action, -1)
                eval_score, _ = self.minimax(new_state, depth - 1, True, alpha, beta)
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_action = action
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval, best_action

    # Evaluation function to score the state for the minimax algorithm
    def eval(self, state):
        if self.check_winner(state, 1):
            return 10
        elif self.check_winner(state, -1):
            return -10
        else:
            return self.heuristic_eval(state)

class RandomOpponent:
    @staticmethod
    def get_available_actions(state):
        available_actions = []
        for i in range(4):
            for j in range(4):
                if state[i][j] == 0:
                    available_actions.append((i, j))
        return available_actions

    def make_move(self, state):
        actions = self.get_available_actions(state)
        return random.choice(actions)

def simulate_games(num_games, minimax_agent, minimax_depth=4):
    random_opponent = RandomOpponent()

    minimax_wins = 0
    random_wins = 0
    draws = 0

    for _ in range(num_games):
        state = np.zeros((4, 4), dtype=int)
        current_player = 1

        while True:
            if current_player == 1:
                action = minimax_agent.make_move(state)
            else:
                action = random_opponent.make_move(state)

            state = TicTacToe_Minimax_Agent.perform_action(state, action, current_player)

            if TicTacToe_Minimax_Agent.check_winner(state, current_player):
                if current_player == 1:
                    minimax_wins += 1
                else:
                    random_wins += 1
                break

            if not TicTacToe_Minimax_Agent.get_available_actions(state):
                draws += 1
                break

            current_player *= -1

    return {
        "minimax_wins": minimax_wins,
        "random_wins": random_wins,
        "draws": draws,
    }

num_games = 100
results = simulate_games(num_games, TicTacToe_Minimax_Agent(), minimax_depth=4)
minimax_win_rate = results["minimax_wins"] / num_games
print(f"Minimax agent win rate over {num_games} games: {minimax_win_rate:.2%}")

def print_board(board):
    symbols = {0: '.', 1: 'X', -1: 'O'}
    for row in board:
        print(' '.join([symbols[cell] for cell in row]))
    print()

def human_move(state):
    while True:
        try:
            move = input("Enter your move (row, col): ")
            row, col = map(int, move.split(','))
            if state[row][col] == 0:
                return (row, col)
            else:
                print("Invalid move. Cell is already filled. Try again.")
        except ValueError:
            print("Invalid input. Please enter row and col as integers separated by a comma.")
        except IndexError:
            print("Invalid input. Please enter row and col values within the range of 0-3.")


def play_game(ai_agent):
    state = np.zeros((4, 4), dtype=int)
    current_player = 1 # Human player
    human_symbol, ai_symbol = 1, -1

    while True:
        print_board(state)

        if current_player == human_symbol:
            action = human_move(state)
        else:
            action = ai_agent.make_move(state)

        state = TicTacToe_Minimax_Agent.perform_action(state, action, current_player)

        if TicTacToe_Minimax_Agent.check_winner(state, current_player):
            if current_player == human_symbol:
                print("Congratulations! You won!")
            else:
                print("The AI won.")
            print_board(state)
            break

        if not TicTacToe_Minimax_Agent.get_available_actions(state):
            print("It's a draw!")
            print_board(state)
            break

        current_player *= -1


# ai_agent = TicTacToe_Minimax_Agent()
# print("Tic Tac Toe - You are playing as 'X', the AI is playing as 'O'")
# play_game(ai_agent)


class TicTacToeGUI:
    def __init__(self, ai_agent):
        self.ai_agent = ai_agent
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe")
        self.state = np.zeros((4, 4), dtype=int)
        self.current_player = 1
        self.buttons = [[None for _ in range(4)] for _ in range(4)]
        self.create_widgets()
        self.window.mainloop()

    def create_widgets(self):
        custom_font = font.Font(size=16, weight='bold')
        for i in range(4):
            for j in range(4):
                self.buttons[i][j] = tk.Button(self.window, text="", width=10, height=3,
                                               command=lambda row=i, col=j: self.human_move(row, col))
                self.buttons[i][j].config(font=custom_font)
                self.buttons[i][j].grid(row=i, column=j)

    def human_move(self, row, col):
        if self.state[row][col] == 0:
            self.state[row][col] = self.current_player
            self.update_button_text(row, col)
            if TicTacToe_Minimax_Agent.check_winner(self.state, self.current_player):
                self.game_over(f"Player {self.current_player} wins!")
                return
            if not TicTacToe_Minimax_Agent.get_available_actions(self.state):
                self.game_over("It's a draw!")
                return
            self.current_player *= -1
            self.ai_move()
        else:
            messagebox.showerror("Invalid Move", "This cell is already filled. Please select another one.")

    def ai_move(self):
        action = self.ai_agent.make_move(self.state)
        self.state[action[0]][action[1]] = self.current_player
        self.update_button_text(action[0], action[1])
        if TicTacToe_Minimax_Agent.check_winner(self.state, self.current_player):
            self.game_over(f"Player {self.current_player} wins!")
            return
        if not TicTacToe_Minimax_Agent.get_available_actions(self.state):
            self.game_over("It's a draw!")
            return
        self.current_player *= -1

    def update_button_text(self, row, col):
        text = "X" if self.state[row][col] == 1 else "O"
        color = "#4CAF50" if self.state[row][col] == 1 else "#F44336"
        self.buttons[row][col].config(text=text, state=tk.DISABLED, disabledforeground=color)


    def game_over(self, message):
        messagebox.showinfo("Game Over", message)
        self.window.destroy()

if __name__ == "__main__":
    ai_agent = TicTacToe_Minimax_Agent()
    print("Tic Tac Toe - You are playing as 'X', the AI is playing as 'O'")
    app = TicTacToeGUI(ai_agent)
