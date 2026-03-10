"""
Kalaha (Kalah) Board Game with AI
02180 Introduction to AI - Spring 2026

Board layout (indices):
  Player 2 pits:  [12][11][10][ 9][ 8][ 7]   Store: [13]
  Player 1 pits:  [ 0][ 1][ 2][ 3][ 4][ 5]   Store: [ 6]

Player 1 owns pits 0-5 and store 6.
Player 2 owns pits 7-12 and store 13.
Sowing goes: 0->1->2->3->4->5->6->7->8->9->10->11->12->13->0->...
"""

import copy
import time
import math

# ─────────────────────────── Constants ───────────────────────────

PITS_PER_PLAYER = 6
SEEDS_PER_PIT   = 4
BOARD_SIZE      = 14   # 6 + 1 + 6 + 1

P1_STORE = 6
P2_STORE = 13

P1_PITS = list(range(0, 6))   # [0..5]
P2_PITS = list(range(7, 13))  # [7..12]

# Difficulty → search depth
DIFFICULTY = {"easy": 3, "medium": 7, "hard": 13}

# ─────────────────────────── Board ───────────────────────────────

def initial_board() -> list[int]:
    """Return the starting board state."""
    board = [SEEDS_PER_PIT] * BOARD_SIZE
    board[P1_STORE] = 0
    board[P2_STORE] = 0
    return board

def player_pits(player: int) -> list[int]:
    return P1_PITS if player == 1 else P2_PITS

def player_store(player: int) -> int:
    return P1_STORE if player == 1 else P2_STORE

def opponent(player: int) -> int:
    return 2 if player == 1 else 1

def opposite_pit(pit: int) -> int:
    """Return the index of the pit directly opposite (across the board)."""
    return 12 - pit   # works for pits 0-5 and 7-12

def legal_moves(board: list[int], player: int) -> list[int]:
    """Return list of non-empty pit indices that the player can sow from."""
    return [p for p in player_pits(player) if board[p] > 0]

def is_terminal(board: list[int]) -> bool:
    """Game is over when either player's side is completely empty."""
    return all(board[p] == 0 for p in P1_PITS) or \
           all(board[p] == 0 for p in P2_PITS)

def collect_remaining(board: list[int]) -> list[int]:
    """When game ends, move all remaining seeds to the respective stores."""
    b = board[:]
    for p in P1_PITS:
        b[P1_STORE] += b[p]
        b[p] = 0
    for p in P2_PITS:
        b[P2_STORE] += b[p]
        b[p] = 0
    return b

def apply_move(board: list[int], player: int, pit: int):
    """
    Apply a move: sow seeds from `pit` counter-clockwise.
    Returns (new_board, next_player, extra_turn).
    """
    b = board[:]
    seeds = b[pit]
    b[pit] = 0
    idx = pit
    opp_store = player_store(opponent(player))

    while seeds > 0:
        idx = (idx + 1) % BOARD_SIZE
        if idx == opp_store:          # skip opponent's store
            continue
        b[idx] += 1
        seeds -= 1

    # Extra-turn rule: last seed lands in own store
    own_store = player_store(player)
    if idx == own_store:
        return b, player, True        # same player goes again

    # Capture rule: last seed lands in empty own pit, opposite pit is non-empty
    own_pits = player_pits(player)
    if idx in own_pits and b[idx] == 1 and b[opposite_pit(idx)] > 0:
        b[own_store] += b[idx] + b[opposite_pit(idx)]
        b[idx] = 0
        b[opposite_pit(idx)] = 0

    return b, opponent(player), False


def utility(board: list[int]) -> int:
    """Terminal utility: positive = P1 advantage."""
    b = collect_remaining(board)
    return b[P1_STORE] - b[P2_STORE]

# ─────────────────────────── Heuristic ───────────────────────────

def evaluate(board: list[int], player: int) -> float:
    """
    Heuristic evaluation h(s) for non-terminal states.

    h(s) = w1*(score_diff) + w2*(extra_turn_moves) + w3*(capture_potential)

    From the perspective of `player` (positive = good for player).
    All components are normalised to be roughly in [−48, 48].
    """
    opp = opponent(player)
    ps  = player_store(player)
    os  = player_store(opp)

    # 1. Score difference (already in stores)
    score_diff = board[ps] - board[os]

    # 2. Count moves that grant an extra turn for `player`
    extra_turn_moves = sum(
        1 for p in player_pits(player)
        if board[p] > 0 and (ps - p) % BOARD_SIZE == board[p]
    )

    # 3. Capture potential: for each own pit where landing is possible and
    #    opposite pit is non-empty, add the seeds that would be captured.
    capture_score = 0
    for p in player_pits(player):
        if board[p] > 0:
            # Where would the last seed land?
            landing = (p + board[p]) % BOARD_SIZE
            if landing in player_pits(player) and board[landing] == 0:
                capture_score += board[opposite_pit(landing)]

    # Weights
    w1, w2, w3 = 1.0, 2.0, 1.5
    h = w1 * score_diff + w2 * extra_turn_moves + w3 * capture_score

    # Return relative to the maximising player (player 1 = max, player 2 = min)
    return h if player == 1 else -h

# ─────────────────────────── Move ordering ───────────────────────

def order_moves(board: list[int], player: int, moves: list[int]) -> list[int]:
    """
    Order moves to improve alpha-beta pruning efficiency.
    Priority (descending):
      1. Moves that grant an extra turn
      2. Moves that result in a capture
      3. All other moves (sorted by pit index descending – tends to spread seeds further)
    """
    ps = player_store(player)

    def priority(pit):
        seeds = board[pit]
        # Extra turn?
        if (ps - pit) % BOARD_SIZE == seeds:
            return 2
        # Capture?
        landing = (pit + seeds) % BOARD_SIZE
        if (landing in player_pits(player) and
                board[landing] == 0 and
                board[opposite_pit(landing)] > 0):
            return 1
        return 0

    return sorted(moves, key=priority, reverse=True)

# ─────────────────────────── Minimax + Alpha-Beta ─────────────────

_nodes_visited = 0   # diagnostic counter

def minimax(board: list[int], player: int, depth: int,
            alpha: float, beta: float, maximising: bool) -> tuple[float, int | None]:
    """
    Minimax with alpha-beta pruning.
    Returns (value, best_move_pit_index).
    Player 1 is the maximising player; Player 2 is the minimising player.
    """
    global _nodes_visited
    _nodes_visited += 1

    if is_terminal(board):
        return utility(board), None

    moves = legal_moves(board, player)
    if not moves:
        # No moves but not terminal: pass turn (shouldn't happen in standard Kalaha)
        return minimax(board, opponent(player), depth, alpha, beta, not maximising)

    if depth == 0:
        return evaluate(board, player), None

    moves = order_moves(board, player, moves)
    best_move = moves[0]

    if maximising:
        value = -math.inf
        for pit in moves:
            new_board, next_player, extra_turn = apply_move(board, player, pit)
            # If extra turn, same player moves again (still maximising)
            next_max = (next_player == 1)
            child_val, _ = minimax(new_board, next_player, depth - 1,
                                   alpha, beta, next_max)
            if child_val > value:
                value, best_move = child_val, pit
            alpha = max(alpha, value)
            if alpha >= beta:
                break   # beta cutoff
        return value, best_move
    else:
        value = math.inf
        for pit in moves:
            new_board, next_player, extra_turn = apply_move(board, player, pit)
            next_max = (next_player == 1)
            child_val, _ = minimax(new_board, next_player, depth - 1,
                                   alpha, beta, next_max)
            if child_val < value:
                value, best_move = child_val, pit
            beta = min(beta, value)
            if alpha >= beta:
                break   # alpha cutoff
        return value, best_move


def ai_move(board: list[int], player: int, difficulty: str = "medium") -> int:
    """Choose the best move for `player` using minimax + alpha-beta."""
    global _nodes_visited
    depth = DIFFICULTY[difficulty]
    _nodes_visited = 0
    t0 = time.time()
    maximising = (player == 1)
    _, best = minimax(board, player, depth, -math.inf, math.inf, maximising)
    elapsed = time.time() - t0
    print(f"  [AI] depth={depth}, nodes={_nodes_visited:,}, time={elapsed:.3f}s")
    return best

# ─────────────────────────── Display ─────────────────────────────

def display_board(board: list[int]) -> None:
    """Pretty-print the board."""
    p2_row = [board[i] for i in reversed(P2_PITS)]   # 12→7
    p1_row = [board[i] for i in P1_PITS]              # 0→5

    print()
    print("         Player 2")
    print("  +----+--+--+--+--+--+--+----+")
    p2_labels = "  | S2 |" + "|".join(f"{v:2d} " for v in p2_row) + "| S1 |"
    print(f"  |{board[P2_STORE]:3d} | " +
          "  ".join(str(v).rjust(2) for v in p2_row) +
          f"  |{board[P1_STORE]:3d} |")
    print("  +----+--+--+--+--+--+--+----+")
    print(f"  |    | " +
          "  ".join(str(v).rjust(2) for v in p1_row) +
          f"  |    |")
    print("  +----+--+--+--+--+--+--+----+")
    print("  Pit#:  0   1   2   3   4   5")
    print("         Player 1")
    print()

# ─────────────────────────── Game loop ───────────────────────────

def get_human_move(board: list[int], player: int) -> int:
    moves = legal_moves(board, player)
    while True:
        try:
            choice = int(input(f"  Player {player}, choose a pit {moves}: "))
            if choice in moves:
                return choice
            print("  Invalid choice. Try again.")
        except ValueError:
            print("  Please enter a number.")


def play_game(ai_player: int = 2, difficulty: str = "medium") -> None:
    """
    Main game loop.
    ai_player: which player the AI controls (1 or 2).
    """
    board = initial_board()
    current_player = 1

    print("\n" + "="*50)
    print("  KALAHA  —  You are Player", 3 - ai_player)
    print(f"  AI difficulty: {difficulty}")
    print("="*50)
    display_board(board)

    while not is_terminal(board):
        print(f"--- Player {current_player}'s turn ---")

        if current_player == ai_player:
            print("  AI is thinking...")
            pit = ai_move(board, current_player, difficulty)
            print(f"  AI chose pit {pit}  (seeds: {board[pit]})")
        else:
            pit = get_human_move(board, current_player)

        board, current_player, extra = apply_move(board, current_player, pit)
        display_board(board)

        if extra and not is_terminal(board):
            print(f"  Player {current_player} gets an extra turn!")

    # Game over
    board = collect_remaining(board)
    print("="*50)
    print("  GAME OVER")
    print(f"  Player 1: {board[P1_STORE]} seeds")
    print(f"  Player 2: {board[P2_STORE]} seeds")
    if board[P1_STORE] > board[P2_STORE]:
        winner = 1
    elif board[P2_STORE] > board[P1_STORE]:
        winner = 2
    else:
        winner = None
    if winner:
        print(f"  Winner: Player {winner}!")
    else:
        print("  It's a draw!")
    print("="*50)


def ai_vs_ai(difficulty1: str = "medium", difficulty2: str = "easy") -> None:
    """Pit two AI players against each other (useful for benchmarking)."""
    board = initial_board()
    current = 1
    move_count = 0

    while not is_terminal(board):
        diff = difficulty1 if current == 1 else difficulty2
        pit = ai_move(board, current, diff)
        board, current, _ = apply_move(board, current, pit)
        move_count += 1

    board = collect_remaining(board)
    print(f"AI vs AI finished in {move_count} moves.")
    print(f"P1 ({difficulty1}): {board[P1_STORE]}  |  P2 ({difficulty2}): {board[P2_STORE]}")
    if board[P1_STORE] > board[P2_STORE]:
        print("Winner: Player 1")
    elif board[P2_STORE] > board[P1_STORE]:
        print("Winner: Player 2")
    else:
        print("Draw")
    return board[P1_STORE], board[P2_STORE]


# ─────────────────────────── Entry point ─────────────────────────

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "aivai":
        d1 = sys.argv[2] if len(sys.argv) > 2 else "hard"
        d2 = sys.argv[3] if len(sys.argv) > 3 else "easy"
        ai_vs_ai(d1, d2)
    else:
        diff = sys.argv[1] if len(sys.argv) > 1 else "medium"
        side = int(sys.argv[2]) if len(sys.argv) > 2 else 2
        play_game(ai_player=side, difficulty=diff)
