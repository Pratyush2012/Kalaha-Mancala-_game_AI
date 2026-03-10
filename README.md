# Kalaha AI — 02180 Introduction to AI, Spring 2026

## Requirements

- Python 3.10 or later (uses `list[int]` type hints)
- No external libraries needed

## Installation

```bash
# No installation needed. Just clone / unzip and run:
python kalaha.py
```

## How to Run

### Human vs AI (default)
```bash
python kalaha.py                    # You = Player 1, AI = Player 2, medium difficulty
python kalaha.py medium 2           # Same as above (explicit)
python kalaha.py easy   2           # AI on easy
python kalaha.py hard   2           # AI on hard
python kalaha.py medium 1           # You = Player 2, AI = Player 1
```

### AI vs AI (benchmarking)
```bash
python kalaha.py aivai medium easy  # Medium AI (P1) vs Easy AI (P2)
python kalaha.py aivai hard  medium # Hard vs Medium
```

## Difficulty Levels

| Level  | Search Depth | Typical nodes | Typical time/move |
|--------|-------------|---------------|-------------------|
| easy   | 3           | ~50           | <1 ms             |
| medium | 7           | ~3 000        | ~15 ms            |
| hard   | 13          | ~50 000+      | ~500 ms           |

## Board Layout

```
         Player 2
  +----+--+--+--+--+--+--+----+
  | S2 | 12 11 10  9  8  7 | S1 |
  +----+--+--+--+--+--+--+----+
  |    |  0  1  2  3  4  5 |    |
  +----+--+--+--+--+--+--+----+
  Pit#:  0   1   2   3   4   5
         Player 1
```

- Pits 0–5 belong to Player 1; pit 6 is Player 1's store (S1).
- Pits 7–12 belong to Player 2; pit 13 is Player 2's store (S2).
- Seeds are sown counter-clockwise (0→1→2→3→4→5→S1→7→8→...→12→S2→0→...).

## Game Rules (Standard Kalaha)

1. **Sowing**: Pick a non-empty pit on your side; distribute seeds one-by-one counter-clockwise, skipping the opponent's store.
2. **Extra turn**: If the last seed lands in your own store, you get another turn.
3. **Capture**: If the last seed lands in an empty pit on your side and the opposite pit is non-empty, you capture both piles into your store.
4. **Game end**: When one player's side is completely empty. All seeds remaining on the other side go to that player's store. The player with more seeds wins.

## File Structure

```
kalaha/
├── kalaha.py   # Game engine + AI (all code)
└── README.md   # This file
```

The AI code is entirely contained in `kalaha.py` with clearly labelled sections:
- **Board logic**: `initial_board`, `apply_move`, `legal_moves`, `is_terminal`, `utility`
- **Heuristic**: `evaluate`
- **Move ordering**: `order_moves`
- **AI search**: `minimax` (alpha-beta), `ai_move`
- **UI / Game loop**: `display_board`, `play_game`, `ai_vs_ai`
