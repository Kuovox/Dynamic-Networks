# Market and Strategic Interaction in Network Assignment

**Course:** CECS 427 (Sec. 02)

**Professor:** Oscar Morales-Ponce

**Date:** 10/21/2025

**Authors:**

- Khoa Vu (030063200)
- Mya Barragan (029948137)

---

## Overview

This project implements a **Market-Clearing Simulation Tool** using Python. The program analyzes a **bipartite market network** consisting of sellers and buyers, where buyers have valuation edges toward sellers and sellers have adjustable prices.  

The tool simulates an iterative **market-clearing algorithm** in which:
1. Buyers select their most preferred seller based on valuation minus price.
2. A matching is computed between buyers and sellers.
3. Prices of unmatched sellers are increased.
4. The process repeats until a perfect matching is achieved (market equilibrium).

The program reads `.gml` files describing the bipartite market, performs the iterative price-adjustment algorithm, and optionally visualizes the graph at each round.

---

## Installation and Setup

### Requirements

Install the required dependencies:

```bash
pip install networkx matplotlib
```

---

## Running the Program
Execute from the command line:

```bash
python ./market_strategy.py market.gml [--plot] [--interactive]
```
Example:
```bash
python ./market_strategy.py market.gml --plot --interactive
```
This reads the bipartite graph in `market.gml`, runs the market-clearing algorithm, optionally visualizes the graph, and displays the status of each iteration.

---

##

| Option / Argument | Description                                                                                       |
| ----------------- | ------------------------------------------------------------------------------------------------- |
| `market.gml`      | Input file describing the bipartite graph. Sellers have price attributes; edges store valuations. |
| `--plot`          | Plots the graph (initial graph and/or each round’s preference graph).                             |
| `--interactive`   | Displays matching results and price updates at every iteration.                                   |

---

## Example Input File
`market.gml`
```gml
graph [
  directed 0

  node [ id 0 price 10 ]
  node [ id 1 price 20 ]
  node [ id 2 ]
  node [ id 3 ]

  edge [ source 2 target 0 valuation 15 ]
  edge [ source 2 target 1 valuation 10 ]
  edge [ source 3 target 0 valuation 18 ]
  edge [ source 3 target 1 valuation 22 ]
]
```

- Nodes `0` and `1` are sellers (set A).
- Nodes `2` and `3` are buyers (set B).
- Edge attribute `valuation` represents how much a buyer values purchasing from a seller.
  
---

## Example Usage & Output
``` bash
python market_strategy.py market.gml --interactive
```
Output:
```csharp
[INFO] Loaded bipartite market with 4 nodes and 4 edges.

--- Round 1 ---
Matching: {(2, 0)}
[UPDATE] Seller 1 price increased to 21

--- Round 2 ---
Matching: {(2, 0), (3, 1)}
[INFO] Market cleared successfully.
```

If `--plot` is used, the tool will display:
- The initial bipartite graph
- Preference graph on each round (buyers linked only to their current top seller)

---

## Approach Summary

1. Graph Parsing
  `networkx.read_gml()` loads nodes and edge attributes. Sellers are indexed `0..n-1`, buyers `n..2n-1`.
2. Preference Computation
  Each buyer selects the seller that maximizes `(valuation - price)`.
3. Maximum Matching
  A bipartite matching is computed to determine which sellers are currently demanded.
4. Price Adjustment Rule
  Unmatched sellers increase their price by +1 each round.
5. Termination Condition
  Algorithm ends when all buyers are matched (market equilibrium).

---

## Output Files
| File / Output     | Description                                            |
| ----------------- | ------------------------------------------------------ |
| Console Output    | Displays iterative matching results and price updates. |
| `plot.png` (auto) | Graph visualization when using `--plot` (optional).    |

---

## Submission Checklist
- `market_strategy.py`
- `README.md`
- `market.gml` (sample input)

---

## Citations

1. https://networkx.org/documentation/stable/reference/readwrite/generated/networkx.readwrite.gml.read_gml.html

2. https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.bipartite.matching.hopcroft_karp_matching.html

3. https://medium.com/%40bragadeeshs optimizing-networks-with-bipartite-graphs-a-practical-guide-7c94e9de0bc6 
