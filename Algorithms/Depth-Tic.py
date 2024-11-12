import tkinter as tk
from tkinter import messagebox
import random

class TicTacToeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe - DFS AI")
        self.board_state = [""] * 9
        self.active_player = "X"
        self.button_list = [tk.Button(root, text="", font='Arial 20', width=5, height=2,
                                       command=lambda i=i: self.user_turn(i)) for i in range(9)]
        for idx, btn in enumerate(self.button_list):
            btn.grid(row=idx // 3, column=idx % 3)

    def user_turn(self, position):
        if self.board_state[position] == "" and self.active_player == "X":
            self.board_state[position] = "X"
            self.button_list[position].config(text="X")
            if self.is_winner("X"):
                messagebox.showinfo("Game Over", "Congratulations, you win!")
                self.restart_game()
            else:
                self.active_player = "O"
                self.ai_turn()

    def ai_turn(self):
        position = self.calculate_ai_move()
        if position is not None:
            self.board_state[position] = "O"
            self.button_list[position].config(text="O")
            if self.is_winner("O"):
                messagebox.showinfo("Game Over", "Computer wins!")
                self.restart_game()
            else:
                self.active_player = "X"

   #DFS Algorithm
   
    def calculate_ai_move(self):
        visited_states = set()
        available_moves = [i for i in range(9) if self.board_state[i] == ""]

        # Check if AI can win in the next move
        for move in available_moves:
            temp_board = self.board_state[:]
            temp_board[move] = "O"
            if self.is_winning_state("O", temp_board):
                return move

        # Check if player can win in the next move and block it
        for move in available_moves:
            temp_board = self.board_state[:]
            temp_board[move] = "X"
            if self.is_winning_state("X", temp_board):
                return move
        
        def depth_first_search(current_board):
            if tuple(current_board) not in visited_states:
                visited_states.add(tuple(current_board))
            
            for next_move in range(9):
                if current_board[next_move] == "":
                    new_board = current_board[:]
                    new_board[next_move] = "X"  # Simulate user's move
                    result = depth_first_search(new_board)
                    if result is not None:
                        return result
            return None
        
        for move in available_moves:
            temp_board = self.board_state[:]
            temp_board[move] = "O"
            result = depth_first_search(temp_board)
            if result is not None:
                return result
            
        return available_moves[0]

    def is_winning_state(self, player, board):
        win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                          (0, 3, 6), (1, 4, 7), (2, 5, 8),
                          (0, 4, 8), (2, 4, 6)]
        return any(all(board[i] == player for i in combo) for combo in win_conditions)

    def is_winner(self, player):
        return self.is_winning_state(player, self.board_state)

    def restart_game(self):
        self.board_state = [""] * 9
        for btn in self.button_list:
            btn.config(text="")
        self.active_player = "X"

if __name__ == "__main__":
    window = tk.Tk()
    game_instance = TicTacToeGame(window)
    window.mainloop()
