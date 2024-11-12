import tkinter as tk
from tkinter import messagebox
import random
from collections import deque

class UltimateTicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Uniform Cost Search Tic Tac Toe")
        self.game_board = [""] * 9
        self.current_turn = "X"
        self.squares = [tk.Button(root, text="", font='Arial 20', width=5, height=2,
                                  command=lambda i=i: self.player_turn(i)) for i in range(9)]
        for i, square in enumerate(self.squares):
            square.grid(row=i // 3, column=i % 3)

    def player_turn(self, index):
        if self.game_board[index] == "" and self.current_turn == "X":
            self.game_board[index] = "X"
            self.squares[index].config(text="X")
            if self.verify_winner("X"):
                messagebox.showinfo("Game Over", "You win!")
                self.restart_game()
            else:
                self.current_turn = "O"
                self.ai_turn()

    def ai_turn(self):
        index = self.decide_ai_move()
        if index is not None:
            self.game_board[index] = "O"
            self.squares[index].config(text="O")
            if self.verify_winner("O"):
                messagebox.showinfo("Game Over", "Computer wins!")
                self.restart_game()
            else:
                self.current_turn = "X"

    #UCS Algorithm
    def decide_ai_move(self):
        move_queue = deque() #Double linked list
        visited_states = set() #Unordered
        possible_moves = [i for i in range(9) if self.game_board[i] == ""]

        # AI checks for a winning move
        for move in possible_moves:
            simulated_board = self.game_board[:]
            simulated_board[move] = "O"
            if self.verify_winner_on_board("O", simulated_board):
                return move  # Winning move for O

        # Block player's winning move
        for move in possible_moves:
            simulated_board = self.game_board[:]
            simulated_board[move] = "X"
            if self.verify_winner_on_board("X", simulated_board):
                return move  # Block X from winning

        # Apply UCS if no immediate win or block
        for move in possible_moves:
            simulated_board = self.game_board[:]
            simulated_board[move] = "O"
            move_queue.append((simulated_board, move, 0))  # (state, first_move, cost)

        while move_queue:
            current_state, first_move, cost = move_queue.popleft()
            state_tuple = tuple(current_state)

            if state_tuple in visited_states:
                continue

            visited_states.add(state_tuple)

            # Winning path check for O
            if self.verify_winner_on_board("O", current_state):
                return first_move

            # Generate possible next moves
            next_moves = [i for i in range(9) if current_state[i] == ""]
            for next_move in next_moves:
                updated_state = current_state[:]
                updated_state[next_move] = "X"  # Simulate opponent's move
                new_cost = cost + 1

                # Adjust costs based on outcomes
                if self.verify_winner_on_board("X", updated_state):
                    new_cost += 10  # Add cost if X is likely to win
                elif self.verify_winner_on_board("O", updated_state):
                    new_cost -= 10  # Favorable state for O

                move_queue.append((updated_state, first_move, new_cost))

            # Sort move queue by cost for UCS
            move_queue = deque(sorted(move_queue, key=lambda x: x[2]))

        # Default random choice if no optimal move
        return random.choice(possible_moves)

    # Verify winner for a specific board layout
    def verify_winner_on_board(self, player, board):
        win_patterns = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                        (0, 3, 6), (1, 4, 7), (2, 5, 8),
                        (0, 4, 8), (2, 4, 6)]
        return any(all(board[i] == player for i in pattern) for pattern in win_patterns)

    def verify_winner(self, player):
        win_patterns = [(0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
                        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
                        (0, 4, 8), (2, 4, 6)]  # Diagonals
        return any(all(self.game_board[i] == player for i in pattern) for pattern in win_patterns)

    def restart_game(self):
        self.game_board = [""] * 9
        for square in self.squares:
            square.config(text="")
        self.current_turn = "X"

if __name__ == "__main__":
    root = tk.Tk()
    game = UltimateTicTacToe(root)
    root.mainloop()
