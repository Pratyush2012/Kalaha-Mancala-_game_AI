from typing import Tuple, Optional

from game_engine import (
    legal_moves,
    make_move,
    game_over,
    utility
)
# Minmax at top and with AB pruning at bottom

class MinimaxAgent:

    def __init__(self):
        self.evaluatedNodes = 0


    def minimax(self, state, depth, player) -> Tuple[int, Optional[int]]:

        self.evaluatedNodes += 1

        # Terminal node checks if done or depth limit reached
        if depth == 0 or game_over(state):
            return utility(state), None

        actions = legal_moves(state, player) # get legal moves for current player

        best_action = None

        # Maximizing player
        if player == 1:    # player 1 is the maximizing player, trying to maximize the score from their perspective

            max_eval = float("-inf")

            for action in actions:

                new_state, next_player, _ = make_move(state, player, action)

                eval_value, _ = self.minimax(new_state, depth - 1, next_player)

                if eval_value > max_eval:
                    max_eval = eval_value
                    best_action = action

            return max_eval, best_action

        # Minimizing player
        else:

            min_eval = float("inf") #looks for lowest score for player 1, which is the highest score for player 2

            for action in actions:

                new_state, next_player, _ = make_move(state, player, action)

                eval_value, _ = self.minimax(new_state, depth - 1, next_player)

                if eval_value < min_eval:
                    min_eval = eval_value
                    best_action = action

            return min_eval, best_action
        
class ABMinimaxAgent:

    def __init__(self):
        self.evaluatedNodes = 0


    def minimax(self, state, depth, player, alpha=float("-inf"), beta=float("inf")):

        self.evaluatedNodes += 1

        # Terminal node
        if depth == 0 or game_over(state):
            return utility(state), None

        actions = legal_moves(state, player)
        best_action = None

        # Maximizing player
        if player == 1:

            max_eval = float("-inf")

            for action in actions:

                new_state, next_player, _ = make_move(state, player, action)

                eval_value, _ = self.minimax(new_state, depth - 1, next_player, alpha, beta)

                if eval_value > max_eval:
                    max_eval = eval_value
                    best_action = action

                # Update alpha
                alpha = max(alpha, eval_value)

                #Alpha-Beta pruning
                if beta <= alpha:
                    break

            return max_eval, best_action

        # Minimizing player
        else:

            min_eval = float("inf")

            for action in actions:

                new_state, next_player, _ = make_move(state, player, action)

                eval_value, _ = self.minimax(new_state, depth - 1, next_player, alpha, beta)

                if eval_value < min_eval:
                    min_eval = eval_value
                    best_action = action

                # Update beta
                beta = min(beta, eval_value)

                # 🔥 Alpha-Beta pruning
                if beta <= alpha:
                    break

            return min_eval, best_action