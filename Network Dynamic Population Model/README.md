# Network Dynamic Population Model Assignment

**Course:** CECS 427 (Sec. 02)

**Professor:** Oscar Morales-Ponce

**Date:** 12/04/2025

**Authors:**

- Khoa Vu (030063200)
- Mya Barragan (029948137)

---

## Overview

This project implements a network-based simulation system capable of modeling:
1. Cascade Processes
(e.g., information spread via threshold activation)

2. COVID-like SIRS Dynamics
   Including:
   - Susceptible → Infectious → Recovered → Susceptible cycling
   - Vaccination
   - Sheltering-in-place
   - Death events
   - Time-series infection tracking

The program loads a directed graph from a `.gml` file and simulates either process based on command-line flags.
It supports optional visualization, including:

Graph state updates per round (`--interactive`)

Time-series plots (`--plot`)

---

## Installation and Setup
### Requirements

Install dependencies:

``` bash
pip install networkx matplotlib
```

---

## Running the Program
Execute the Python script:

``` bash
python ./dynamic_population.py graph.gml [OPTIONS]
```

---

## Command-Line Options

| Option / Argument              | Description                                                             |                                 |
| ------------------------------ | ----------------------------------------------------------------------- | ------------------------------- |
| `--action [cascade             | covid]`                                                                 | Select which simulation to run. |
| `--initiator m`                | Comma-separated list of starting active/infected nodes (e.g., `1,2,5`). |                                 |
| `--threshold q`                | Cascade activation threshold (0–1).                                     |                                 |
| `--probability_of_infection p` | COVID model per-edge infection probability (0–1).                       |                                 |
| `--probability_of_death q`     | COVID model per-day death probability (0–1).                            |                                 |
| `--lifespan l`                 | Number of rounds/days to simulate.                                      |                                 |
| `--shelter s`                  | Fraction of nodes sheltered from infection (0–1).                       |                                 |
| `--vaccination r`              | Fraction of nodes vaccinated at start (0–1).                            |                                 |
| `--plot`                       | Plots time-series curve of activations or infections.                   |                                 |
| `--interactive`                | Displays graph state every round/day.                                   |                                 |

---

## Examples
### 1. Cascade Simulation
```bash
python ./dynamic_population.py graph.gml \
    --action cascade \
    --initiator 1,2 \
    --threshold 0.33 \
    --plot
```

### 2. COVID SIRS Simulation
```bash
python ./dynamic_population.py graph.gml \
    --action covid \
    --initiator 3 \
    --probability_of_infection 0.05 \
    --probability_of_death 0.01 \
    --lifespan 60 \
    --shelter 0.25 \
    --vaccination 0.35 \
    --plot
```

### 3. Fully Interactive Visualization
```bash
python ./dynamic_population.py graph.gml \
    --action covid \
    --initiator 1,2 \
    --probability_of_infection 0.2 \
    --lifespan 40 \
    --shelter 0.1 \
    --vaccination 0.1 \
    --interactive \
    --plot
```

---

## Input Graph Format (`graph.gml`)

The program expects a graph in GML format.

Example minimal file:
```gml
graph [
  directed 1

  node [ id 1 label "1" ]
  node [ id 2 label "2" ]
  node [ id 3 label "3" ]

  edge [ source 1 target 2 ]
  edge [ source 2 target 3 ]
  edge [ source 1 target 3 ]
]
```

---

## Features & Workflow
### 1. Cascade Simulation
- All nodes start inactive except initiators.
- A node activates if:
  fraction of active in-neighbors ≥ threshold
- Synchronous updates per round.
- Ends when:
    - No more activations, or
    - Safety cap on rounds reached.
- Outputs:
  - Whether complete cascade occurred
  - Rounds total
  - Plot of activations per round (optional)

### 2. COVID SIRS Simulation
States:
- S — Susceptible
- I — Infectious
- R — Recovered (temporary immunity)
- V — Vaccinated (immune)
- X — Sheltered (no transmission)
- D — Dead

Dynamics:
- Infection spread via outgoing edges with probability p_infect
- Death chance while infected: `p_death`
- Infection duration → Recovery
- Recovery duration → Susceptible again
- Shelter and vaccination applied before Day 1
- Time-series stored for final plotting

---

## Example Output Files
| File / Output             | Description                          |
| ------------------------- | ------------------------------------ |
| `infection_plot.png`      | New infections per day (COVID).      |
| `cascade_plot.png`        | New activations per round (cascade). |
| Interactive graph windows | Shows evolving system per timestep.  |

---

## Approach Summary
1) Input Parsing
   - Validates graph existence, parameter ranges, and initiators.
2) Graph Loading
   - Uses networkx.read_gml() to build DiGraph.
3) Simulation Core
   - Cascade → threshold-based adoption
   - COVID → SIRS + death + shelter + vaccination
4) State Tracking
   - Dictionaries for node state and timers (infection/recovery).
5) Visualization
   - Time-series plots via matplotlib
   - Node-colored graph via NetworkX (optional).
6) Error Handling
   - Invalid files, thresholds, probabilities
   - Missing initiators (warn only)

--- 

## Synthetic Test Graph
Included to help with immediate testing:
```gml
graph [
  directed 1
  
  # Nodes 1 through 6
  node [
    id 1
    label "1"
  ]
  node [
    id 2
    label "2"
  ]
  node [
    id 3
    label "3"
  ]
  node [
    id 4
    label "4"
  ]
  node [
    id 5
    label "5"
  ]
  node [
    id 6
    label "6"
  ]

  # Edges
  edge [ source 1 target 2 ]
  edge [ source 2 target 3 ]
  edge [ source 3 target 4 ]
  edge [ source 4 target 5 ]
  edge [ source 5 target 6 ]
  
  edge [ source 1 target 3 ]
  edge [ source 2 target 4 ]
  edge [ source 3 target 5 ]
  edge [ source 4 target 6 ]
  
  edge [ source 2 target 1 ]
  edge [ source 3 target 1 ]
]
```

---

## Citations
1) Afolabi, O. (2023). Simulating Infectious Disease Spread with Python: SIR and SEIR Models. HackerNoon. https://hackernoon.com/simulating-infectious-disease-spread-with-python-sir-and-seir-models
2) “What is disease modeling? Intro to the SIR model.” (n.d.). YouTube. https://www.youtube.com/watch?v=cbXCyO_F2v8
3) Yadav, S. Ramjeet. (2020, May 15). Mathematical Modeling and Simulation of SIR Model for COVID-2019 Epidemic Outbreak: A Case Study of India. medRxiv. https://www.medrxiv.org/content/10.1101/2020.05.15.20103077v1.full

--- 

## Submission Checklist
- dynamic_population.py
- README.md
- graph.gml (test dataset)
- Any example plots generated using --plot
