🎮 A* Chase Game — Grid-Based Pursuit Game with Pygame

A small grid-based game built with Python and Pygame, featuring a player-controlled spaceship and an A* pathfinding agent (Alien) that dynamically chases the player. The project explores pathfinding algorithms, dynamic enemy pursuit, real-time game logic, JSON-based modular level configuration, UI design, and asset integration, including custom visuals and background music.

⸻

🚀 How to Run the Game
```bash
# Clone the repo
git clone https://github.com/danielle060821/astar-chase-game.git
cd astar-chase-game

# Create virtual environment
python3 -m venv .venv

# Activate venv (Mac/Linux)
source .venv/bin/activate

# Install dependencies
pip install pygame

# Run the game
python game.py
```
⸻

🎮 How to Play

Move the player (spaceship) using:
• W = up
• A = left
• S = down
• D = right

Objective
• Reach the goal flag before the A* alien agent catches you.

Game Rules
• The alien agent uses A* pathfinding to recalculate the shortest route toward the player in real time
• Movement cooldowns ensure fair pacing between player and agent
• A step counter tracks the agent’s movement cost
• The game displays a countdown intro, win/lose states, and an end-game delay before exit

⸻

🧠 Technical Highlights

• A* pathfinding implemented from scratch with:
 • Open set (priority queue)
 • Closed set
 • g_score, f_score, and path reconstruction

• Real-time agent pursuit with dynamic path recomputation

• Grid-based collision and movement constraints

• JSON-driven level system
 • Grid layout, player spawn, agent spawn, goal, and music loaded from external JSON
 • Enables scalable multi-level expansion without modifying core game logic

• Modular game structure (separate logic for grid, agent, and game state)

• Custom UI and assets:
 • Player spaceship sprite
 • Alien enemy sprite
 • Goal flag icon
 • Integrated background music (composed and edited by the developer)

• Relative asset paths for portability across environments
• Virtual environment workflow for clean dependency management

⸻

📁 Project Structure (Simplified)
```
My_Game/
├── README.md
├── game.py
├── a_Star.py
├── Maps/
│   └──level1.json
├── legacy/
│   └── grid_level1.py
├── assets/
│   ├── images/
│   └── audio/
└── .venv/
```
⸻

📌 Notes

• Designed as a playable demo rather than a full commercial game
• The project focuses on algorithmic correctness, system structure, and interactive behavior rather than visual polish
• Future extensions could include multi-level maps, teleport mechanics, or learning-based agents

