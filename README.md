# Semantic Freshness-Aware Infrastructure Reconciliation for Digital Twins

This repository contains the preliminary proof-of-concept simulation for a semantic freshness-aware reconciliation policy in Edge-Cloud environments. 

## Project Structure
- `src/` — Python simulation code
- `data/` — EdgeSimPy dataset used for topology scaling
- `results/` — Output metrics from the simulation
- `docs/` — LaTeX report and final PDF (once added)

## How to Run
1. Ensure Python 3.10+ is installed.
2. Install dependencies: `pip install -r requirements.txt` (or `pip install numpy pandas edge_sim_py`)
3. Run the simulation: `python src/simulate_reconciliation.py`
4. Results will print to the console and save to `results/preliminary_results.csv`.

## Preliminary Results
| Policy | Reconciliations | Avg AoI | Total Overhead |
|---|---|---|---|
| Periodic | 20 | 2.0 | 200 |
| Event-Driven | 61 | 2.0 | 610 |
| Semantic (Proposed) | 35 | 2.0 | 550 |