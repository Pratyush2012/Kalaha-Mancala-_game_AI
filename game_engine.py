"""
Kalha game engine.

Board layout (indices):
    Player 2 pits:  [12][11][10][ 9][ 8][ 7]   Store: [13]
    Player 1 pits:  [ 0][ 1][ 2][ 3][ 4][ 5]   Store: [ 6]

Placing the stones order (counter-clockwise):
    0 → 1 → 2 → 3 → 4 → 5 → 6(S1) → 7 → 8 → 9 → 10 → 11 → 12 → 13(S2) → repeat from 0

"""

# Constants for the game
Pits_per_player = 6
Seeds_per_pit = 4
Board_size = 14  # 6 pits + 1 store + 6 pits + 1 store

P1_store = 6
P2_store = 13

P1_pits = [0, 1, 2, 3, 4, 5]
P2_pits = [7, 8, 9, 10, 11, 12]

# inital board setup
def initial_board():
    """
    Returns the starting board state.
    All 12 pits contain 4 seeds; both stores start at 0.
    """
    board = [Seeds_per_pit] * Board_size
    board[P1_store] = 0
    board[P2_store] = 0
    return board

# Helper functions for querying the board state
def player_pits(player):
    """Return the pit indices belonging to the given player."""
    return P1_pits if player == 1 else P2_pits

def player_store(player):
    return P1_store if player == 1 else P2_store

def opponent(player):
    return 2 if player == 1 else 1

def opposite_pit(pit):
    """
    Return the pit directly across the board (used for capturing rule)
    e.g. opposite_pit(0) = 12, opposite_pit(5) = 7
    """
    return 12 - pit



# Game rules (contains the logic for making a move, checking for game end, etc.)
def legal_moves(board, player):
    legal_moves_arr = []
    for pit in player_pits(player):
        if board[pit] > 0:
            legal_moves_arr.append(pit)
    return legal_moves_arr

def game_over(board): # check if one player's pits are all empty
    p1_empty = all(board[pit] == 0 for pit in P1_pits)
    p2_empty = all(board[pit] == 0 for pit in P2_pits)
    return p1_empty or p2_empty

def collect_remaining_seeds(board):
    """When the game ends, collect all remaining seeds into the last player's store."""
    board = board[:]  # make a copy to modify
    for pit in P1_pits:
        board[P1_store] += board[pit]
        board[pit] = 0
    for pit in P2_pits:
        board[P2_store] += board[pit]
        board[pit] = 0
    return board

def make_move(board, player, pit):
    """
    Make a move for the given player from the specified pit.
    
    Rules to follow while making a move:
    1. Pick up all seeds from the chosen pit.
    2. Sow the seeds one by one in a counter-clockwise direction, skipping the opponent's store.
    3. If the last seed lands in the player's own store, they get an extra turn.
    4. If the last seed lands in an empty pit on the player's own side, they capture that seed and any seeds in the opposite pit.

    Returns:
        new_board: the board state after the move
        next_player: the player who will move next (could be the same player if they get an extra turn)
        extra_turn: True if the player gets an extra turn, False otherwise
    """

    b = board[:]  # making a copy of the board to modify (so we don't change the original board in place)
    seeds = b[pit]  
    b[pit] = 0  # clear the seeds from the chosen pit

    player_store_index = player_store(player)
    opponent_store_index = player_store(opponent(player))
    player_pits_indices = player_pits(player) # this is of type list[int]

    # Sowing the seeds
    current_index = pit
    while seeds > 0:
        current_index = (current_index + 1) % Board_size 

        if current_index == opponent_store_index:
            continue

        b[current_index] += 1 
        seeds -= 1  
    
    # Check for extra turn
    extra_turn = (current_index == player_store_index)

    # Check for capturing the rest of opponent's seeds
    if (current_index in player_pits_indices) and (b[current_index] == 1):  # last seed lands in an empty pit on player's own side
        opposite_index = opposite_pit(current_index)
        if b[opposite_index] > 0: 
            b[player_store_index] += b[opposite_index] + 1  
            
            b[current_index] = 0 
            b[opposite_index] = 0 
    
    next_player = player if extra_turn else opponent(player)
    return b, next_player, extra_turn


# Score calculation (after the game ends)
def calculate_score(board):
    return board[P1_store], board[P2_store]

def winner(board):
    score_p1, score_p2 = calculate_score(board)
    if score_p1 > score_p2:
        return 1
    elif score_p2 > score_p1:
        return 2
    else:
        return 0  # tie

def utility(board):
    """Terminal utility from Player 1's perspective. 
    Only called after the game ends (use game_over to check)."""
    b = collect_remaining_seeds(board)
    return b[P1_store] - b[P2_store]


# Display
def display_board(board):

    p2_row = [board[i] for i in reversed(P2_pits)]   # display 12 → 7
    p1_row = [board[i] for i in P1_pits]             # display 0 → 5

    print((25 * "-") + " Game Board " + (25 * "-"))
    print()
    print("                        Player 2")
    print(f"P2 store|" + "".join(f"  {i:2d} |" for i in reversed(range(7, 13))))
    print ("-" * 53)
    print(f"|  {board[P2_store]:2d}   |" + "".join(f"  {v:2d} |" for v in p2_row) +  "       |")
    print(f"|" + " " * 7 + "|" + "-" * 5 + "|" + "-" * 5 + "|" + "-" * 5 + "|" + "-" * 5 + "|" + "-" * 5 + "|" + "-" * 5 + "|" + " " * 7 + "|")
    print(f"|       |" + "".join(f"  {v:2d} |" for v in p1_row) + f"  {board[P1_store]:2d}   |")
    print("-" * 53)
    print(f"        |" + "".join(f"  {i:2d} |" for i in (range(0, 6))) + "P1 store")
    print("                         Player 1")
    print()
    print((63 * "-"))


# Just for testing the game engine
if __name__ == "__main__":
    board = initial_board()
    display_board(board)
    # Example sequence of moves
    moves = [(1, 2), (2, 8), (1, 0), (2, 7), (1, 5), (2, 12), (1, 3), (2, 9)]
    for player, pit in moves:
        print(f"Player {player} moves from pit {pit}")
        board, next_player, extra_turn = make_move(board, player, pit)
        if next_player != player:
            print(f"Extra turn for Player {player}!, but next player is Player {next_player}, but we move on because this is just a test")
        if extra_turn:
            print("Player gets an extra turn!")
        display_board(board)
        if game_over(board):
            print("Game over!")
            board = collect_remaining_seeds(board)
            display_board(board)
            break
        
        