# 🎮 4x4 Tic Tac Toe AI with Minimax & GUI

This project features a smart **Tic Tac Toe AI agent** that plays optimally on a **4x4 grid** using the **Minimax algorithm** with **alpha-beta pruning** and **heuristic evaluation**. It includes:

- A simulation engine to test against random players  
- A playable **Tkinter GUI** for human-vs-AI gameplay  
- Performance benchmarking across multiple games

---

## 🧠 Features

- **Minimax Algorithm** with depth control  
- **Alpha-Beta Pruning** for faster decision-making  
- **Heuristic Evaluation** for non-terminal states  
- **Human vs AI gameplay** in terminal or GUI  
- **Game simulation** vs random opponent for performance testing  
- **Clean and interactive GUI** built with Tkinter

---

## 🛠️ Tech Stack

- Python 3  
- NumPy  
- Tkinter (built-in for GUI)

---

## 📦 Installation

Just clone the repo and run the script with Python. All dependencies are built-in or installable via pip:

```bash
pip install numpy
```

---

## 🚀 How to Run

### 🧪 Run Simulations

To simulate 100 games of AI vs Random agent:

```bash
python your_script.py
```

You’ll see the win rate printed like:

```
Minimax agent win rate over 100 games: 92.00%
```

### 🎮 Launch GUI for Human Play

To play against the AI with a graphical interface:

```bash
python your_script.py
```

> You are 'X'. The AI plays as 'O'. First move is yours!

---

## 📐 AI Logic

### 🧮 Minimax + Alpha-Beta Pruning

The AI explores all possible game states to a certain depth, choosing moves that maximize its chance of winning while minimizing the opponent’s.

### 🧠 Heuristic Evaluation

Evaluates non-terminal states with this logic:
- +1 for each line (row/col/diag) where AI has 3 marks and 1 empty
- -1 for each line where the opponent does

---

## 🖼️ GUI Overview

- 4x4 grid using Tkinter
- Disabled buttons after move
- Color-coded symbols:  
  - X (Human): 🟩  
  - O (AI): 🟥
- Game ends with alert message: win, lose, or draw

---

## 📁 File Structure

```
.
├── tictactoe_minimax.py        # Core logic, simulation, and GUI
```

---

## 🧪 Sample Game Logic

```python
ai_agent = TicTacToe_Minimax_Agent()
print("You are playing as 'X', the AI is playing as 'O'")
play_game(ai_agent)  # or launch TicTacToeGUI(ai_agent)
```

---

## 🧠 Example Heuristic

For this board:
```
X X X .
. . . .
. . . .
. . . .
```

AI evaluates a +1 potential win by filling the last cell in the first row.

---

## 📄 License

This project is open-source and intended for academic or personal use.

---
