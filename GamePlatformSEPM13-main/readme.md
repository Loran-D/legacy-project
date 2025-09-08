# UU Game by Group 13

## Overview
This is a digital implementation of the abstract strategy board game Tak, played on a 6x6 grid. Players compete against an AI opponent to create a road connecting opposite sides of the board using flat pieces, or to have the most flat pieces on top when the board fills up.

## Game Rules
- Player (Black) and AI (White) alternate turns, with AI moving first
- Each player starts with 21 pieces
- The game is played on a 6x6 board
- Pieces can be placed either flat or standing
- The game ends when:
  - A player creates a continuous path of flat pieces between opposite sides
  - The board is completely filled
  - 200 moves are reached without a winner
  - If there's a tie in flat pieces during a flat win condition

### Valid Moves
- Place a piece from your hand (flat or standing)
- Move a piece or stack of pieces you control (top piece must be yours)
- Stack pieces on top of flat pieces (max 5 pieces per stack)
- Cannot stack on top of standing pieces

## Installation

### Option 1: Direct Installation
1. Execute the UUgame.exe file.

# OR

### Option 2: Setup from Source
### Prerequisites
- Python 3.x
- Pygame library

### Setup
1. Clone the repository:
```bash
git clone https://github.com/Erikbraa/GamePlatformSEPM13.git
cd GamePlatformSEPM13
```

2. Install required dependencies:
```bash
pip install pygame
```

3. Run the game:
```bash
python UI.py
```

### Winning the Game
You can win by:
1. Creating a continuous path of your flat pieces connecting opposite sides of the board
2. Having the most flat pieces on top when the board is filled
3. The game can end in a draw if:
   - 200 turns are reached without a winner
   - Players have equal flat pieces during a flat win condition

## Game Components
This game is implemented using Python and Pygame. The main components include:
- Board: Manages the game board state and layout
- Piece: Handles individual game pieces and their properties
- Player: Manages player actions and state
- Stack: Controls piece stacking mechanics
- UI: Handles game visualization and user interaction
- AI: Implements the computer opponent's decision-making logic

## How to Play
1. Start the game - Select AI difficulty (EASY, MEDIUM, HARD)
2. On your turn (Black):
    - Click on a cell to select piece(s) (press 1-5) or place a new one
    - Click on another cell to move the selected piece(s)
    - Hold Shift to place a standing piece
    - Hold Ctrl to stack a new piece on a stack