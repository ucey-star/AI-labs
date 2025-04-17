# 🧩 8-Puzzle Solver using A\* Search

This project implements an **A\*-based solver** for the classic 8-puzzle problem. The core logic is encapsulated in the `PuzzleNode` class, which represents individual puzzle states and generates successor nodes during the search.

---

## 🚀 Features

- Models puzzle states as nodes with depth and parent tracking  
- Generates valid successor states by sliding the empty tile  
- Supports integration with A\* search using custom heuristics  
- Includes helper methods for copying nodes, comparing states, and locating the blank tile

---

## 📦 Class: `PuzzleNode`

This class defines the structure and behavior of a puzzle node used in search algorithms like A\*.

### ✅ Attributes:
- `puzzle`: NumPy array version of the board  
- `state`: List of lists (2D board)  
- `parent`: Pointer to the parent node  
- `depth`: Node depth from the root  
- `f_value`: Evaluation function (g + h)  
- `pruned`: Marks if node was pruned  
- `length`: Board size (3 for 8-puzzle)

### ✅ Key Methods:
- `__lt__(self, other)`: For priority queue comparisons  
- `__str__()`: String representation of the puzzle  
- `empty_tile()`: Returns coordinates of the blank (0) tile  
- `copy()`: Returns a deep copy of the current node  
- `successor_states()`: Generates all valid next moves

---

## 📐 How It Works

The puzzle is modeled as a 3x3 grid. The blank tile (0) can move up, down, left, or right if the move is within bounds. Each move generates a new `PuzzleNode`, which is used in search algorithms to find the shortest path to the goal state.

### Example State:
```
[[1, 2, 3],
 [4, 0, 5],
 [6, 7, 8]]
```

### Sample Successor Moves:
- Swap 0 with up (1)
- Swap 0 with down (7)
- Swap 0 with left (4)
- Swap 0 with right (5)

---

## 📁 File Structure

```
.
├── puzzle_node.py          # Contains PuzzleNode class and logic
├── (optional) solver.py    # A* search implementation (not included here)
```

---

## ✅ Requirements

Only standard libraries are needed:

```bash
pip install numpy
```

---

## 🧠 Usage

You can import `PuzzleNode` into your solver module to run A\* search like this:

```python
from puzzle_node import PuzzleNode

start_state = [[1, 2, 3], [4, 0, 5], [6, 7, 8]]
start_node = PuzzleNode(start_state, 0, None)
successors = start_node.successor_states()
```

---

## 🔄 Next Steps

- Integrate with A\* search using heuristics like Manhattan Distance or Misplaced Tiles  
- Add goal state checking and solution path reconstruction  
- Visualize search path and performance metrics

---

## 📄 License

This project is open-source and intended for learning and academic use.

---
