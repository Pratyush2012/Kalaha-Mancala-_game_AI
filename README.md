

## Installation


```bash


pip install -r requirements.txt
or
py -m pip install -r requirements.txt

```

## How to Run


### Human vs AI
can be run with different -d would suggest not to go over 10
```bash
       py .\HvMinimax.py -d 5
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

