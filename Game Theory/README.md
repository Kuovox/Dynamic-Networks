
# Game Theory Assignment -- Traffic Equilibrium Analysis Tool

**Course:** CECS 427 (Sec. 02)

**Professor:** Oscar Morales-Ponce

**Date:** 10/21/2025

**Authors:**

- Khoa Vu (030063200)
- Mya Barragan (029948137)

---

## Overview

This project implements a **Traffic Equilibrium Analysis Tool** using Python. The program computes and visualizes the **Travel Equilibrium (Nash Equilibrium)** and **Social Optimality** in a directed traffic network.  

Given a directed graph where each edge is defined by a **cost function** of the form:

`c(x) = a x + b`

The program determines how vehicles distribute themselves along the available paths between an initial and final node to achieve both **individual equilibrium** and **system-wide efficiency**.

The program reads `.gml` files describing the graph structure and edge parameters, performs equilibrium calculations, and optionally generates visualizations of the network and its edge cost functions.

---

## Installation and Setup

### Requirements

Install dependencies before running the script:

```bash
pip install networkx matplotlib scipy
```

---

## Running the Program
Execute from the command line:
```bash
python ./traffic_analysis.py digraph_file.gml n source target [--plot]
```

Example:
```bash
python ./traffic_analysis.py traffic.gml 4 0 3 --plot
```
This reads the directed graph `traffic.gml` and computes the Travel Equilibrium and Social Optimum for 4 vehicles traveling from node 0 to node 3.

---

## Features & Command-Line Options
| Option / Argument  | Description                                                              |
| ------------------ | ------------------------------------------------------------------------ |
| `digraph_file.gml` | Input file describing the directed graph and edge parameters (`a`, `b`). |
| `n`                | Total number of vehicles in the network.                                 |
| `source`           | Starting node ID.                                                        |
| `target`           | Destination node ID.                                                     |
| `--plot`           | Plot the directed graph and visualize edge cost functions.               |

---

## Example Input File
`traffic.gml`
```gml
graph [
  directed 1
  node [ id 0 label "Start" ]
  node [ id 1 label "A" ]
  node [ id 2 label "B" ]
  node [ id 3 label "End" ]

  edge [ source 0 target 1 a 1 b 0 ]
  edge [ source 1 target 3 a 0 b 1 ]
  edge [ source 0 target 2 a 0 b 2 ]
  edge [ source 2 target 3 a 1 b 0 ]
]
```
Each edge has a polynomial cost function `c(x) = a*x + b`.

---

## Example Usage & Output
