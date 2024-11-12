import tkinter as tk
from tkinter import messagebox
import random
from collections import deque

class TicTacToeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic Tac Toe")
        self.board_state = [""] * 9
        self.current_turn = "X"
        self.buttons = [tk.Button(master, text="", font='Arial 20', width=5, height=2,
                                   command=lambda i=i: self.player_turn(i)) for i in range(9)]
        for i, button in enumerate(self.buttons):
            button.grid(row=i // 3, column=i % 3)

    def player_turn(self, index):
        if self.board_state[index] == "" and self.current_turn == "X":
            self.board_state[index] = "X"
            self.buttons[index].config(text="X")
            if self.check_winner("X"):
                messagebox.showinfo("Game Over", "You win!")
                self.restart_game()
            else:
                self.current_turn = "O"
                self.ai_turn()

    def ai_turn(self):
        move_index = self.determine_ai_move()
        if move_index is not None:
            self.board_state[move_index] = "O"
            self.buttons[move_index].config(text="O")
            if self.check_winner("O"):
                messagebox.showinfo("Game Over", "Computer wins!")
                self.restart_game()
            else:
                self.current_turn = "X"

    #Breadth Algorithm
    def determine_ai_move(self):
        queue = deque()
        visited_states = set()
        available_moves = [i for i in range(9) if self.board_state[i] == ""]

        # Check if the AI can win in the next move
        for move in available_moves:
            temp_board = self.board_state[:]
            temp_board[move] = "O"
            if self.is_winner("O", temp_board):
                return move  # Winning move for AI

        # Check if the player can win in the next move and block it
        for move in available_moves:
            temp_board = self.board_state[:]
            temp_board[move] = "X"
            if self.is_winner("X", temp_board):
                return move  # Block player's winning move

        # If no immediate win or block is necessary, continue with BFS
        for move in available_moves:
            temp_board = self.board_state[:]
            temp_board[move] = "O"
            queue.append((temp_board, move))

        while queue: #Continue if there is any board state in queue
            current_state, move = queue.popleft()

            # Explore further moves
            for next_move in range(9):
                if current_state[next_move] == "":
                    new_board_state = current_state[:]
                    new_board_state[next_move] = "X"  # Simulate placing "X"
                    if tuple(new_board_state) not in visited_states:
                        visited_states.add(tuple(new_board_state))
                        queue.append((new_board_state, next_move))

        # If no strategic move found, return a random available move
        return available_moves[0]

    # Check for a winner on a given board state
    def is_winner(self, player, board):
        winning_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                                (0, 3, 6), (1, 4, 7), (2, 5, 8),
                                (0, 4, 8), (2, 4, 6)]
        return any(all(board[i] == player for i in combo) for combo in winning_combinations)

    def check_winner(self, player):
        return self.is_winner(player, self.board_state)

    def restart_game(self):
        self.board_state = [""] * 9
        for button in self.buttons:
            button.config(text="")
        self.current_turn = "X"

if __name__ == "__main__":
    root = tk.Tk()
    game_instance = TicTacToeGame(root)
    root.mainloop()
