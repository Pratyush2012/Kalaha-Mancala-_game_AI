from game_engine import (
    initial_board,
    legal_moves,
    make_move,
    game_over,
    collect_remaining_seeds,
    winner,
    P1_store,
    P2_store,
    display_board
)

class KalahaCLI:
    """Simple command-line interface for running the Kalaha game."""

    def __init__(self):
        """Initialize the game state."""
        self.board = initial_board()
        self.current_player = 1
        self.turn_number = 1

    # Main game flow
    def run(self):
        """Start the game loop and keep running until the game ends."""
        self.print_welcome()

        while not game_over(self.board):
            self.play_turn()

        self.finish_game()

    def print_welcome(self):
        print("=" * 58)
        print(" " * 22 + "KALAHA")
        print("=" * 58)
        print("Mode: Player vs Player")
        print("Choose a pit number from your own side when it is your turn.")
        print("Player 1 uses pits 0-5")
        print("Player 2 uses pits 7-12")
        print("=" * 58)
        print()

    # Input handling
    def get_player_move(self):
        """Ask the current player for a move until a valid one is entered."""
        allowed_moves = legal_moves(self.board, self.current_player)

        while True:
            print("Available pits:", " ".join(str(m) for m in allowed_moves))
            user_input = input(f"Player {self.current_player}, choose a pit: ").strip()

            if user_input.lower() in {"q", "quit", "exit"}:
                print("Game exited.")
                raise SystemExit

            if not user_input.isdigit():
                print("Please enter a valid pit number.")
                print()
                continue

            chosen_pit = int(user_input)

            if chosen_pit not in allowed_moves:
                print("Invalid move. Choose one of the available pits.")
                print()
                continue

            return chosen_pit

    # Turn handling
    def play_turn(self):
        """Run one full turn for the current player."""
        display_board(self.board)
        print(f"Player {self.current_player}'s turn")
        print("-" * 58)


        chosen_pit = self.get_player_move()
        seeds_in_pit = self.board[chosen_pit]

        print(f"Player {self.current_player} chose pit {chosen_pit} with {seeds_in_pit} seeds.")
        print()

        # Store values before the move, used for simple capture detection
        prev_store_p1 = self.board[P1_store]
        prev_store_p2 = self.board[P2_store]

        new_board, next_player, extra_turn = make_move(
            self.board,
            self.current_player,
            chosen_pit
        )

        self.board = new_board

        # Show a message if a capture happened
        if self.current_player == 1:
            if self.board[P1_store] - prev_store_p1 > 1:
                print("Capture! Player 1 captured seeds.")
        else:
            if self.board[P2_store] - prev_store_p2 > 1:
                print("Capture! Player 2 captured seeds.")

        # Handle extra turn rule
        if extra_turn and not game_over(self.board):
            print(f"Extra turn for Player {self.current_player}.")
        else:
            self.current_player = next_player

        self.turn_number += 1
        print()

    # End-of-game handling
    def finish_game(self):
        """Collect remaining seeds, print final board, and show the result."""
        self.board = collect_remaining_seeds(self.board)

        print()
        print("=" * 58)
        print(f"{'GAME OVER':^58}")
        print("=" * 58)

        display_board(self.board)

        p1_score = self.board[P1_store]
        p2_score = self.board[P2_store]

        print("Final score")
        print(f"Player 1 store: {p1_score}")
        print(f"Player 2 store: {p2_score}")

        game_winner = winner(self.board)

        if game_winner == 0:
            print("Result: Draw")
        else:
            print(f"Result: Player {game_winner} wins")

        print("=" * 58)

# Start the game
if __name__ == "__main__":
    game = KalahaCLI()
    game.run()