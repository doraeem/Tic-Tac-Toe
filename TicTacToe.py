import tkinter as tk
import tkinter.messagebox
import random

class TicTacToe:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic Tac Toe")
        self.master.configure(bg="#E6E6FA")

        # Title Label
        self.title_label = tk.Label(master, text="Tic Tac Toe", font=("Arial", 24), pady=10)
        self.title_label.pack()

        self.board_frame = tk.Frame(master)
        self.board_frame.pack(pady=10)

        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self.board_frame, text="", font=('Arial', 20), width=6, height=3,
                                                command=lambda row=i, col=j: self.player_move(row, col))
                self.buttons[i][j].grid(row=i, column=j, padx=5, pady=5)

        self.mode_frame = tk.Frame(master)
        self.mode_frame.pack(pady=5)

        self.ai_vs_human_button = tk.Button(self.mode_frame, text="AI vs Human", font=('Arial', 14), width=10, command=self.start_ai_vs_human)
        self.ai_vs_human_button.grid(row=0, column=0, padx=5)

        self.ai_vs_ai_button = tk.Button(self.mode_frame, text="AI vs AI", font=('Arial', 14), width=10, command=self.start_ai_vs_ai)
        self.ai_vs_ai_button.grid(row=0, column=1, padx=5)

        self.restart_button = tk.Button(self.mode_frame, text="Restart", font=('Arial', 14), width=10, command=self.reset_board)
        self.restart_button.grid(row=0, column=2, padx=5)

        # Create the board
        self.board = [["" for _ in range(3)] for _ in range(3)]

        # Flag to indicate the current player
        self.current_player = "X"

    # handle player's move
    def player_move(self, row, col):
        if self.board[row][col] == "":
            self.board[row][col] = "X"
            self.buttons[row][col].config(text="X", state=tk.DISABLED)
            print("Player's move: ", (row, col))
            self.print_available_moves()
            if self.game_over():
                self.end_game()
            else:
                ai_row, ai_col = self.ai_move("O")
                self.board[ai_row][ai_col] = "O"
                self.buttons[ai_row][ai_col].config(text="O", state=tk.DISABLED)
                print("AI's move: ", (ai_row, ai_col))
                self.print_available_moves()
                if self.game_over():
                    self.end_game()

    #  print available moves
    def print_available_moves(self):
        available_moves = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == ""]
        print("Available Moves:", available_moves)

    #  check if a player has won
    def check_winner(self, player):
        for row in self.board:
            if all(cell == player for cell in row):
                return True
        for col in range(3):
            if all(row[col] == player for row in self.board):
                return True
        if all(self.board[i][i] == player for i in range(3)):
            return True
        if all(self.board[i][2 - i] == player for i in range(3)):
            return True
        return False

    #  check if the board is full
    def check_draw(self):
        for row in self.board:
            for cell in row:
                if cell == "":
                    return False
        return True

    #  check if the game is over
    def game_over(self):
        return self.check_winner("X") or self.check_winner("O") or self.check_draw()

    #  evaluate the board for the AI
    def evaluate(self):
        if self.check_winner("O"):
            return -1
        elif self.check_winner("X"):
            return 1
        elif self.check_draw():
            return 0
        else:
            return None

    #  make AI move
    def ai_move(self, player):
        best_eval = float('-inf') if player == "O" else float('inf')
        best_moves = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "":
                    self.board[i][j] = player
                    eval = self.minimax(5, player == "O")
                    self.board[i][j] = ""
                    if (player == "O" and eval > best_eval) or (player == "X" and eval < best_eval):
                        best_eval = eval
                        best_moves = [(i, j)]
                    elif eval == best_eval:
                        best_moves.append((i, j))
        move = random.choice(best_moves)
        return move

    # Minimax algorithm implementation
    def minimax(self, depth, is_maximizing):
        if self.game_over() or depth == 0:
            return self.evaluate()

        if is_maximizing:
            max_eval = float('-inf')
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == "":
                        self.board[i][j] = "O"
                        eval = self.minimax(depth - 1, False)
                        self.board[i][j] = ""
                        if eval is not None:
                            max_eval = max(max_eval, eval)
            return max_eval if max_eval != float('-inf') else 0
        else:
            min_eval = float('inf')
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == "":
                        self.board[i][j] = "X"
                        eval = self.minimax(depth - 1, True)
                        self.board[i][j] = ""
                        if eval is not None:
                            min_eval = min(min_eval, eval)
            return min_eval if min_eval != float('inf') else 0

    # start AI vs Human game
    def start_ai_vs_human(self):
        self.reset_board()
        while not self.game_over():
            self.print_available_moves()
            if self.current_player == "X":
                ai_row, ai_col = self.ai_move("O")
                self.board[ai_row][ai_col] = "O"
                self.update_buttons()
                print("AI's move: ", (ai_row, ai_col))
                self.print_available_moves()
                if self.game_over():
                    self.end_game()
                    return
                self.switch_player()
            else:
                break

    #  start AI vs AI game
    def start_ai_vs_ai(self):
        self.reset_board()
        while not self.game_over():
            self.print_available_moves()
            ai_row, ai_col = self.ai_move(self.current_player)
            self.board[ai_row][ai_col] = self.current_player
            self.update_buttons()
            print("AI's move: ", (ai_row, ai_col))
            self.print_available_moves()
            if self.game_over():
                self.end_game()
                return
            self.switch_player()

    #  reset the board
    def reset_board(self):
        for i in range(3):
            for j in range(3):
                self.board[i][j] = ""
                self.buttons[i][j].config(text="", state=tk.NORMAL)

    # update button states
    def update_buttons(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] != "":
                    self.buttons[i][j].config(text=self.board[i][j], state=tk.DISABLED)

    #  end the game and show the result
    def end_game(self):
        if self.check_winner("O"):
            tk.messagebox.showinfo("Game Over", "AI Wins!")
        elif self.check_winner("X"):
            tk.messagebox.showinfo("Game Over", "Player Wins!")
        else:
            tk.messagebox.showinfo("Game Over", "It's a Draw!")

    #  switch players
    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"

# Create the main window
root = tk.Tk()
app = TicTacToe(root)
root.mainloop()

