

## Installation


```bash


pip install -r requirements.txt
or
py -m pip install -r requirements.txt

```

## How to Run


### Human vs AI
Use `-d/--depth` to control search depth and `--agent` to choose the algorithm. Would suggest not to go over depth of 10 based on time runs without AB pruning

Examples:
```bash
python HvAI.py -d 5 --agent minimax
python HvAI.py -d 7 --agent ab
```

### AI vs AI (benchmarking)
```bash
       py .\AIvAI.py
```
### Human vs Human (testing game_engine worked)
```bash
       py main.py
```
## Board Layout

```
         Player 2
  +----+--+--+--+--+--+--+--+----+
  | S2 | 12 11 10  9  8  7  |    |
  |    +--+--+--+--+--+--+--+    |
  |    |  0  1  2  3  4  5  | S1 |
  +----+--+--+--+--+--+--+--+----+
  Pit#:  0   1   2   3   4   5
         Player 1
```

- Pits 0–5 belong to Player 1; pit 6 is Player 1's store (S1).
- Pits 7–12 belong to Player 2; pit 13 is Player 2's store (S2).
- Seeds are sown counter-clockwise (0→1→2→3→4→5→S1→7→8→...→12→S2→0→...).

