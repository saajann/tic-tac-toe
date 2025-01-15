import tkinter as tk
import json
import random


class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe")
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.game_mode = None
        self.create_menu()
        self.window.bind("r", lambda event: self.reset_game())

    def create_menu(self):
        """Creates the menu to choose the game mode."""
        self.reset_game_state()
        for widget in self.window.winfo_children():
            widget.destroy()
        tk.Label(self.window, text="Choose Game Mode", font=("Helvetica", 16)).pack()
        tk.Button(self.window, text="Player vs Player", font=("Helvetica", 14), command=self.start_pvp).pack()
        tk.Button(self.window, text="Player vs AI", font=("Helvetica", 14), command=self.start_pvai).pack()
        tk.Button(self.window, text="View Previous Games", font=("Helvetica", 14), command=self.view_previous_games).pack()

    def start_pvp(self):
        """Starts a Player vs Player game."""
        self.game_mode = "PVP"
        self.create_board()

    def start_pvai(self):
        """Starts a Player vs AI game."""
        self.game_mode = "PVAI"
        self.create_board()

    def create_board(self):
        """Creates the game board with buttons."""
        for widget in self.window.winfo_children():
            widget.destroy()
        for row in range(3):
            for col in range(3):
                button = tk.Button(
                    self.window,
                    text=" ",
                    font=("Helvetica", 24),
                    width=5,
                    height=2,
                    command=lambda r=row, c=col: self.make_move(r, c),
                )
                button.grid(row=row, column=col)
                self.buttons[row][col] = button

    def make_move(self, row, col):
        """Handles a player's move."""
        if self.board[row][col] == " ":
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player)

            if self.check_winner(self.current_player):
                self.end_game(f"Player {self.current_player} wins!")
            elif self.is_draw():
                self.end_game("It's a draw!")
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                if self.game_mode == "PVAI" and self.current_player == "O":
                    self.ai_move()

    def ai_move(self):
        """Handles the AI's move."""
        empty_cells = [(r, c) for r in range(3) for c in range(3) if self.board[r][c] == " "]
        row, col = random.choice(empty_cells)
        self.make_move(row, col)

    def check_winner(self, player):
        """Checks if the player has won."""
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)):  # Rows
                return True
            if all(self.board[j][i] == player for j in range(3)):  # Columns
                return True
        if all(self.board[i][i] == player for i in range(3)):  # Main diagonal
            return True
        if all(self.board[i][2 - i] == player for i in range(3)):  # Anti-diagonal
            return True
        return False

    def is_draw(self):
        """Checks if the game is a draw."""
        return all(cell != " " for row in self.board for cell in row)

    def end_game(self, result):
        """Ends the game and displays the result."""
        for row in self.buttons:
            for button in row:
                button.config(state="disabled")

        tk.Label(self.window, text=result, font=("Helvetica", 16)).grid(
            row=3, column=0, columnspan=3
        )
        tk.Label(self.window, text="Press 'r' to play again", font=("Helvetica", 12)).grid(
            row=4, column=0, columnspan=3
        )
        self.save_game(result)

    def save_game(self, result):
        """Saves the finished game to a JSON file."""
        game_data = {
            "board": self.board,
            "result": result,
        }

        try:
            with open("tic_tac_toe_games.json", "r") as file:
                games = json.load(file)
        except FileNotFoundError:
            games = []

        games.append(game_data)

        with open("tic_tac_toe_games.json", "w") as file:
            json.dump(games, file, indent=4)

    def view_previous_games(self):
        """Displays the previous games."""
        for widget in self.window.winfo_children():
            widget.destroy()

        try:
            with open("tic_tac_toe_games.json", "r") as file:
                games = json.load(file)
        except FileNotFoundError:
            games = []

        if not games:
            tk.Label(self.window, text="No previous games found.", font=("Helvetica", 16)).pack()
        else:
            for idx, game in enumerate(games):
                tk.Label(self.window, text=f"Game {idx + 1}: {game['result']}", font=("Helvetica", 14)).pack()
                for row in game["board"]:
                    tk.Label(self.window, text=" | ".join(row), font=("Helvetica", 12)).pack()

        tk.Button(self.window, text="Back to Menu", font=("Helvetica", 14), command=self.create_menu).pack()

    def reset_game_state(self):
        """Resets the game state."""
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.buttons = [[None for _ in range(3)] for _ in range(3)]

    def reset_game(self):
        """Resets the game to start a new game."""
        self.reset_game_state()
        self.create_board()

    def run(self):
        """Runs the main event loop."""
        self.window.mainloop()


if __name__ == "__main__":
    game = TicTacToe()
    game.run()

