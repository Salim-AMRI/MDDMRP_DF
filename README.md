# MDDMRP-DF: Multi-Depot Drone Marine Routing with Flexible Depots

This repository contains the code, instances, and results for the paper:

> **Multi-Depot Drone Marine Routing with Flexible Depots and Discrete Speeds: An Exact Mixed-Integer Linear Programming Approach for Underwater Mine Counter-Measures**

Submitted to *Journal of Heuristics*.

## 📋 Table of contents

- [Overview](#overview)
- [Repository structure](#repository-structure)
- [Installation](#installation)
- [Quick start](#quick-start)
- [Reproducing the paper](#reproducing-the-paper)
- [Instance format](#instance-format)

## Overview

The Multi-Depot Drone Marine Routing Problem with Flexible Depots (MDDMRP-DF) is a routing problem motivated by mine counter-measure missions in strategic waterways. It integrates:

- **3D depth-dependent ocean currents** (Zermelo navigation)
- **Variable water density** (speed- and depth-dependent)
- **Discrete speed choices** (1.2, 1.6, 2.0 m/s)
- **Flexible depot return** (drones may end at any depot)
- **Heterogeneous fleet** (per-drone energy and depth limits)

Two solution methods are provided:

1. **Exact MILP formulation** solved with Gurobi (moderate instances ≤ 60 targets)
2. **Adaptive Large Neighborhood Search (ALNS)** for larger instances (up to 200 targets)

## Repository structure
.
├── code/ # Python source code
│ └── alns_v2.py # ALNS solver (main file)
├── instances/ # Benchmark instances (JSON)
├── results/ # Raw experimental results
│ ├── summary_ALNS.csv # Aggregated results
│ └── solutions/ # Optimal routes (JSON)
├── figures/ # Figures from the paper
├── docs/ # Additional documentation
├── README.md
├── LICENSE
└── requirements.txt


## Installation

### Requirements

- Python 3.8 or higher
- NumPy
- (Optional) Gurobi 13.0 for the exact MILP solver

### Install dependencies

```bash
pip install -r requirements.txt

requirements.txt contents

numpy>=1.24
matplotlib>=3.7
pandas>=2.0
scipy>=1.10

Quick start
Run the ALNS on a single instance
bash
cd code
python alns_v2.py ../instances/instance_advanced_0.json \
    --runs 30 \
    --max-iter 5000 \
    --time-limit 300 \
    --out ../results/test_run
Run the ALNS on all instances
bash
cd code
python alns_v2.py ../instances \
    --runs 30 \
    --max-iter 5000 \
    --time-limit 300 \
    --resume \
    --out ../results/full_run
Command-line options
Option	Default	Description
--runs	30	Number of independent runs per instance
--max-iter	5000	Maximum iterations per run
--time-limit	300	Time limit per run (seconds)
--q-min	0.05	Minimum destruction ratio
--q-max	0.30	Maximum destruction ratio
--destroy	random,worst,cluster,current	Active destroy operators
--repair	greedy	Active repair operator
--accept	sa	Acceptance criterion (sa or descent)
--ls-freq	1	Local search frequency (0 = disabled)
--no-adaptive	False	Disable adaptive weights
--out	results_alns	Output directory
--resume	False	Skip already completed runs
--save-solutions	None	Directory for route JSON files
Reproducing the paper
1. Table 7 — ALNS validation on small instances
bash
cd code
python alns_v2.py ../instances \
    --runs 30 --max-iter 5000 --time-limit 300 \
    --out ../results/small_validation
2. Table 8 — Comparison on medium instances
bash
python alns_v2.py ../instances \
    --runs 30 --max-iter 5000 --time-limit 300 \
    --out ../results/medium
3. Table 9 — Scalability on 100-target instances
bash
python alns_v2.py ../instances/instance_100_*.json \
    --runs 30 --max-iter 5000 --time-limit 300 \
    --out ../results/large_100
4. Table 10 — Scalability on 150-target instances
bash
python alns_v2.py ../instances/instance_150_*.json \
    --runs 30 --max-iter 5000 --time-limit 300 \
    --out ../results/large_150
5. Table 11 — Scalability on 200-target instances
bash
python alns_v2.py ../instances/instance_200_*.json \
    --runs 30 --max-iter 5000 --time-limit 300 \
    --out ../results/large_200
6. Table 12 — Algorithmic ablation
bash
# Full ALNS
python alns_v2.py ../instances/instance_150_5.json \
    --runs 30 --max-iter 5000 --time-limit 300 \
    --out ../results/ablation_150_5_full

# Without local search
python alns_v2.py ../instances/instance_150_5.json \
    --runs 30 --max-iter 5000 --time-limit 300 \
    --ls-freq 0 \
    --out ../results/ablation_150_5_no_ls

# Random removal only
python alns_v2.py ../instances/instance_150_5.json \
    --runs 30 --max-iter 5000 --time-limit 300 \
    --destroy random \
    --out ../results/ablation_150_5_random_only

# Without adaptive weights
python alns_v2.py ../instances/instance_150_5.json \
    --runs 30 --max-iter 5000 --time-limit 300 \
    --no-adaptive \
    --out ../results/ablation_150_5_no_adaptive

# Greedy acceptance
python alns_v2.py ../instances/instance_150_5.json \
    --runs 30 --max-iter 5000 --time-limit 300 \
    --accept descent \
    --out ../results/ablation_150_5_greedy
Repeat the same commands for instance_200_9.json.

Instance format
Each instance is a JSON file with the following structure:

json
{
  "depots": [
    {"x": 0.0, "y": 0.0, "z": 0.0},
    {"x": 100.0, "y": 50.0, "z": 0.0}
  ],
  "targets": [
    {
      "x": 50.0, "y": 30.0, "z": -45.0,
      "weight": 0.75,
      "duration": 120.0,
      "is_mine": true
    }
  ],
  "drones": [
    {
      "E_max": 72000.0,
      "H_max": 150.0,
      "start_depot": 0
    }
  ],
  "drone_speeds": [1.2, 1.6, 2.0],
  "time_matrices": [[[...]]],
  "energy_matrices": [[[...]]],
  "sensor_power": 100.0,
  "depth_penalty": 10.0
}
