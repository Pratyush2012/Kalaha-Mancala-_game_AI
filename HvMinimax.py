
from game_engine import (
    initial_board,
    legal_moves,
    make_move,
    game_over,
    display_board,
    collect_remaining_seeds,
    winner
) 

from minimax_agent import MinimaxAgent


def main():

    board = initial_board()
    player = 1

    agent = MinimaxAgent()

    print("Kalaha: Human vs Minimax")
    print("Player 1 = AI")
    print("Player 2 = Human")

    while not game_over(board):

        display_board(board)
        moves = legal_moves(board, player)

        if player == 1:
            print("AI thinking...")

            agent.evaluatedNodes = 0

            value, action = agent.minimax(board.copy(), depth=6, player=player)   # Adjust depth as needed

            print(
                "Agent evaluated",
                agent.evaluatedNodes,
                "states and chose move",
                action,
                "value:",
                value
            )

        else:
            print("Available moves:", moves)

            try:
                action = int(input("Choose pit: "))
            except:
                print("Invalid input")
                continue

        if action not in moves:
            print("Invalid move")
            continue

        board, player, extra_turn = make_move(board, player, action)

        if extra_turn:
            print("Extra turn!")

    # Game finished
    board = collect_remaining_seeds(board)

    print("\nGame Over")
    display_board(board)

    w = winner(board)

    if w == 0:
        print("Draw")
    else:
        print("Winner: Player", w)


if __name__ == "__main__":
    main()