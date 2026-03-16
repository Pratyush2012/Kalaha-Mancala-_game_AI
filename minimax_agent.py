from typing import Tuple, Optional

from game_engine import (
    legal_moves,
    make_move,
    game_over,
    utility
)


class MinimaxAgent:

    def __init__(self):
        self.evaluatedNodes = 0


    def minimax(self, state, depth, player) -> Tuple[int, Optional[int]]:

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

                eval_value, _ = self.minimax(new_state, depth - 1, next_player)

                if eval_value > max_eval:
                    max_eval = eval_value
                    best_action = action

            return max_eval, best_action

        # Minimizing player
        else:

            min_eval = float("inf")

            for action in actions:

                new_state, next_player, _ = make_move(state, player, action)

                eval_value, _ = self.minimax(new_state, depth - 1, next_player)

                if eval_value < min_eval:
                    min_eval = eval_value
                    best_action = action

            return min_eval, best_action