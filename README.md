# Preprocessing (AMBER dataset generation)

This repo starts by generating AMBER simulation folders, running a sequential stretching protocol, and then collecting outputs for downstream analysis.

## `utils/` scripts

### 1) Generate folders + restraint/input files (`stretch.py`)
Creates `S1 ... S401` and writes per-folder `stretch{i}.RST` (DISANG restraints) and `md.in`.

Run:
    python utils/stretch.py

### 2) Run AMBER sequentially (`amber.run`)
Runs simulations folder-by-folder (`S1`, `S2`, ...), where each step continues from the previous `stretch*.rst7`.

Run (example):
    sbatch amber.run

Note: `TOTAL` in `amber.run` controls how many folders you run.

### 3) Postprocessing options

A) Collect all restart files (`rst_collector.py`)  
Copies all `.rst7` files from `S*` into `rst7/`.
    python utils/rst_collector.py

B) Export energies (`energy.py`)  
Parses `md*.out` files and writes `energies.csv`.
    python utils/energy.py

C) Merge + trim trajectories (`sampler.py`)  
Reads `.nc` trajectories from `S*`, trims to DNA atoms, and saves `all_traj_DNAonly.npz`.
    python utils/sampler.py
