# DIA-Autonomous-Robot
#  Maze-Solving AI Agents (COMP3004 Final Project)

This project implements and evaluates an autonomous agent using classic search algorithms to navigate randomly generated mazes with increasing difficulty. It includes both visual simulation and quantitative performance analysis under normal and noisy conditions.

## Features

- Multiple search algorithms:
  - Random Walk
  - Greedy Best-First Search
  - Breadth-First Search (BFS)
  - Uniform Cost Search (UCS)
  - A* Search
- Dynamic maze generation with obstacles and mud tiles (high cost paths)
- Optional noisy perception simulation (adds false positives and negatives)
- Replanning logic for adaptive agents under uncertainty
- Pygame-based visual interface
- Experiment runner with CSV logging and Matplotlib result visualisation

## Folder Structure

.
├── agent.py # Agent logic for all AI strategies
├── environment.py # Maze generation and rendering
├── experiment_runner.py # Batch experiment execution and CSV logging
├── levels.py # Maze size definitions
├── main.py # Pygame interface for visual demo
├── results.csv # Experiment results (auto-generated)
├── results_summary.csv # Summary of averages per method (auto-generated)
├── plot_results.py # Generates bar charts from experiment results
├── assets/
│ ├── mouse.png
│ └── cheese.png
└── README.md


## How to Run
### Run visual demo:

python main.py
You will be prompted to select:

Maze difficulty 
Algorithm   
Whether to enable noisy perception

Run experiments:
python experiment_runner.py
This will test all algorithms over 30 runs per level, with and without noise.

Plot results:
python plot_results.py
Generates graphs comparing:

Success rate
Steps
Cost
Time
Replans due to noise

## Tools Used
Python 3.11
Pygame
Matplotlib
pandas

Stephanie Chung 20491960 hcysc1
COMP3004: Designing Intelligent Agents

