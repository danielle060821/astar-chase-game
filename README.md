
🎮 A* Chase Game — Grid-Based Pursuit Game with Pygame<br>

A grid-based pursuit game built with Python and Pygame, featuring a player-controlled spaceship and an autonomous alien agent powered by A* pathfinding.
The project explores pathfinding algorithms, real-time agent behavior, modular game architecture, JSON-based level configuration, and game state management, with custom visuals and background music.

This project evolved from a single-file prototype into a multi-module, extensible game framework, designed to support future mechanics such as additional agents, new rules, and multiple levels.

⸻

🚀 How to Run the Game<br>
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

🎮 How to Play<br>

Move the player (spaceship) using:<br>
• W = up<br>
• A = left<br>
• S = down<br>
• D = right<br>

Objective<br>
• Reach the goal flag before the A* alien agent catches you.<br>

Game Rules<br>
• The alien agent uses A* pathfinding to dynamically recompute the shortest route toward the player<br>
• Independent movement cooldowns ensure fair pacing between player and agent<br>
• A step counter tracks the agent’s movement cost<br>
• The game features a countdown intro, clear win/lose conditions, and a timed end-game state<br>

⸻

🧠 Technical Highlights<br>

Pathfinding & Agents<br>

• A* pathfinding implemented from scratch with:<br>
 • Open set (priority queue)<br>
 • Closed set<br>
 • g_score, f_score, and path reconstruction<br>

• Real-time pursuit with dynamic target updates (agent re-plans toward the player each step)<br>
• Agent behavior encapsulated in a dedicated AStarAgent class to support future multi-agent extensions<br>

Game Architecture<br>

• JSON-driven level system<br>
 • Grid layout, player spawn, agent spawn, goal position, and background music loaded from external JSON<br>
 • Enables scalable multi-level expansion without modifying core game logic<br>

• Explicit game state machine (GameState, Phase)<br>
 • Countdown → Playing → Finished<br>
 • Clean separation between game flow and rendering logic<br>

• Rule evaluation system (Rules module)<br>
 • Centralized win/lose logic decoupled from the main game loop<br>
 • Supports future rule extensions (e.g., multiple enemies, hazards, special tiles)<br>

• Modular system design with clear separation of concerns:<br>
 • agents — autonomous entities and AI logic<br>
 • rules — win/lose conditions and game outcome evaluation<br>
 • renderer — drawing, UI, and visual presentation<br>
 • audio — background music management<br>
 • asserts — level validation and safety checks<br>

UI & Assets<br>

• Custom sprites:<br>
 • Player spaceship<br>
 • Alien enemy<br>
 • Goal flag<br>

• Integrated background music (composed and edited by the developer)<br>
• Relative asset paths for portability across environments<br>
• Virtual environment workflow for clean dependency management<br>

⸻

📁 Project Structure (Simplified)<br>
```
My_Game/
├── README.md
├── game.py                 # Main game loop & orchestration
├── game_state.py           # Game phase & state machine
├── a_star.py               # Core A* algorithm
├── agents.py               # Agent abstractions (A* agent)
├── rules.py                # Win / lose rule evaluation
├── renderer.py             # Rendering & UI
├── audio.py                # Background music handling
├── asserts.py              # Level validation checks
├── Maps/
│   └── level1.json         # JSON-based level configuration
├── legacy/
│   └── grid_level1.py      # Deprecated Python-based level (archived)
├── assets/
│   ├── images/
│   └── audio/
└── .venv/
```
⸻

📌 Notes<br>

• Designed as a playable demo and engineering exploration, not a full commercial game<br>
• Emphasis is placed on algorithmic correctness, system structure, and extensibility rather than visual polish<br>
• The codebase was intentionally refactored into multiple modules to support long-term scalability<br>
• Future extensions may include additional levels, teleport mechanics, multiple enemy types, or learning-based agents<br>
