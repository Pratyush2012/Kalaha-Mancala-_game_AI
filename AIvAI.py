import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
import time

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
from minimax_agent import ABMinimaxAgent

# ---------------------------
# Setup
# ---------------------------

runs = 5
depths = [3,4, 5,6, 7,8]

minimax_agent = MinimaxAgent()
ab_agent = ABMinimaxAgent()


# ---------------------------
# Simulation: Minimax
# ---------------------------

def simulate_minimax(depth):
    totalStates = 0
    state = initial_board()
    player = 1

    while not game_over(state):
        valid_actions = legal_moves(state, player)

        if player == 1:
            minimax_agent.evaluatedNodes = 0

            _, action = minimax_agent.minimax(state.copy(), depth, player)

            totalStates += minimax_agent.evaluatedNodes
        else:
            action = np.random.choice(valid_actions)

        state, player, _ = make_move(state, player, action)

    return totalStates


# ---------------------------
# Simulation: Alpha-Beta
# ---------------------------

def simulate_ab(depth):
    totalStates = 0
    state = initial_board()
    player = 1

    while not game_over(state):
        valid_actions = legal_moves(state, player)

        if player == 1:
            ab_agent.evaluatedNodes = 0

            _, action = ab_agent.minimax(state.copy(), depth, player)

            totalStates += ab_agent.evaluatedNodes
        else:
            action = np.random.choice(valid_actions)

        state, player, _ = make_move(state, player, action)

    return totalStates


# ---------------------------
# Benchmark runner
# ---------------------------

def benchmark(func, depth):
    results = []
    start_time = time.time()

    for _ in range(runs):
        results.append(func(depth))

    total_time = time.time() - start_time

    return np.mean(results), total_time


# ---------------------------
# Run experiments
# ---------------------------

minimax_nodes = []
ab_nodes = []

minimax_times = []
ab_times = []

for depth in tqdm(depths, desc="Benchmarking depths"):

    m_nodes, m_time = benchmark(simulate_minimax, depth)
    ab_nodes_val, ab_time = benchmark(simulate_ab, depth)

    minimax_nodes.append(m_nodes)
    ab_nodes.append(ab_nodes_val)

    minimax_times.append(m_time)
    ab_times.append(ab_time)


# ---------------------------
# Print summary
# ---------------------------

print("\n--- SUMMARY ---")
for i, d in enumerate(depths):
    print(f"\nDepth {d}:")
    print(f"Minimax    -> Nodes: {minimax_nodes[i]:.0f}, Time: {minimax_times[i]:.2f}s")
    print(f"Alpha-Beta -> Nodes: {ab_nodes[i]:.0f}, Time: {ab_times[i]:.2f}s")


# ---------------------------
# Plot 1: Nodes vs Depth
# ---------------------------

plt.figure()
plt.plot(depths, minimax_nodes, marker='o', label="Minimax")
plt.plot(depths, ab_nodes, marker='o', label="Alpha-Beta")

plt.title("Nodes Evaluated vs Depth")
plt.xlabel("Depth")
plt.ylabel("Nodes Evaluated")
plt.legend()
plt.grid()

plt.show()


# ---------------------------
# Plot 2: Time vs Depth
# ---------------------------

plt.figure()
plt.plot(depths, minimax_times, marker='o', label="Minimax")
plt.plot(depths, ab_times, marker='o', label="Alpha-Beta")

plt.title("Execution Time vs Depth")
plt.xlabel("Depth")
plt.ylabel("Time (seconds)")
plt.legend()
plt.grid()

plt.show()


# ---------------------------
# Efficiency gain
# ---------------------------

reduction = 100 * (1 - np.mean(ab_nodes) / np.mean(minimax_nodes))
print(f"\nAlpha-Beta reduces nodes by {reduction:.2f}%")