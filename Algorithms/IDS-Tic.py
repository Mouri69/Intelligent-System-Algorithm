import tkinter as tk
from tkinter import messagebox
import random

class TicTacToeAI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe with AI")
        
        # Initialize game state
        self.board = [""] * 9
        self.current_turn = "X"
        
        # Create grid of buttons
        self.buttons = [
            tk.Button(root, text="", font='Arial 20', width=5, height=2, command=lambda i=i: self.player_turn(i)) 
            for i in range(9)
        ]
        
        for index, button in enumerate(self.buttons):
            button.grid(row=index // 3, column=index % 3)

    def player_turn(self, pos):
        # Player can only make a move if cell is empty and it's their turn
        if self.board[pos] == "" and self.current_turn == "X":
            self.board[pos] = "X"
            self.buttons[pos].config(text="X")
            if self.is_winner("X"):
                messagebox.showinfo("Game Over", "Congratulations! You win!")
                self.restart_game()
            else:
                self.current_turn = "O"
                self.ai_turn()

    def ai_turn(self):
        # Get AI's move using IDS and update board
        position = self.find_best_move()
        if position is not None:
            self.board[position] = "O"
            self.buttons[position].config(text="O")
            if self.is_winner("O"):
                messagebox.showinfo("Game Over", "AI wins!")
                self.restart_game()
            else:
                self.current_turn = "X"

    #IDS Algorithm
    def find_best_move(self):
        empty_cells = [i for i in range(9) if self.board[i] == ""]

        # First, try to win in the next move
        for move in empty_cells:
            temp_board = self.board[:]
            temp_board[move] = "O"
            if self.check_board_winner("O", temp_board):
                return move  # AI wins here

        # Then, check for a blocking move
        for move in empty_cells:
            temp_board = self.board[:]
            temp_board[move] = "X"
            if self.check_board_winner("X", temp_board):
                return move  # Block player from winning

        # If no immediate moves, use Iterative Deepening Search (IDS)
        max_depth = len(empty_cells)

        def ids_strategy(board, depth):
            if depth == 0:
                return None
            
            for move in range(9):
                if board[move] == "":
                    simulated_board = board[:]
                    simulated_board[move] = "O"
                    if self.check_board_winner("O", simulated_board):
                        return move
                    result = ids_strategy(simulated_board, depth - 1) #-1 to recurssivaly recall one less depth
                    if result is not None:
                        return move
            return None

        for depth in range(1, max_depth + 1): #+1 to allow it to explore deeper moves 
            for move in empty_cells:
                simulated_board = self.board[:]
                simulated_board[move] = "O"
                result = ids_strategy(simulated_board, depth - 1) #-1 to see outcomes available at current depth
                if result is not None:
                    return move

        # Fallback: pick a random empty cell
        return random.choice(empty_cells)

    def check_board_winner(self, player, board):
        winning_positions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
                             (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
                             (0, 4, 8), (2, 4, 6)]             # Diagonals
        return any(all(board[i] == player for i in line) for line in winning_positions)

    def is_winner(self, player):
        winning_positions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
                             (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
                             (0, 4, 8), (2, 4, 6)]             # Diagonals
        return any(all(self.board[i] == player for i in line) for line in winning_positions)

    def restart_game(self):
        self.board = [""] * 9
        for button in self.buttons:
            button.config(text="")
        self.current_turn = "X"

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToeAI(root)
    root.mainloop()
