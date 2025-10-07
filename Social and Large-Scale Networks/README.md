# Social and Large-Scale Networks Assignment -- Graph Analysis Tool

**Course:** CECS 427 (Sec. 02)

**Professor:** Oscar Morales-Ponce

**Date:** 10/07/2025

**Authors:**

- Khoa Vu (030063200)
- Mya Barragan (029948137)

---

## 🧠 Overview

This project implements a **Graph Analysis Tool** designed to explore and visualize social and large-scale networks using Python. The program loads graphs from `.gml` files, computes key metrics such as clustering coefficients and neighborhood overlap, partitions the network into communities, tests for homophily and balance, and simulates temporal and structural changes.

This project demonstrates the analysis of dynamic network behaviors through clustering, robustness testing, and temporal simulation.

---

## ⚙️ Installation and Setup

### Requirements

Install the required libraries using:

```bash
pip install networkx matplotlib scipy pandas
```

### Running the Program

The program executes from the command line:

```bash
python ./graph_analysis.py graph_file.gml [OPTIONS]
```

---

## 🧩 Features & Command-Line Options

| Option                           | Description                                                                                                      |     |                                                                                                                                                                                                |
| -------------------------------- | ---------------------------------------------------------------------------------------------------------------- | --- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--components n`                 | Partition the graph into *n* communities using the **Girvan–Newman** algorithm.                                  |     |                                                                                                                                                                                                |
| `--robustness_check k`           | Perform repeated random edge removals (*k* edges per trial) and report average connectivity and component sizes. |     |                                                                                                                                                                                                |
| `--simulate_failures k`          | Randomly remove *k* edges and analyze connectivity, shortest path, and betweenness centrality.                   |     |                                                                                                                                                                                                |
| `--verify_homophily`             | Run a **t-test** on node attributes (color/group) to test for homophily.                                         |     |                                                                                                                                                                                                |
| `--verify_balanced_graph`        | Check if the **signed graph** is structurally balanced using BFS logic.                                          |     |                                                                                                                                                                                                |
| `--plot [C                       | N                                                                                                                | P]` | Visualize the network: <br>• `C`: clustering coefficient (node size = CC, color = degree) <br>• `N`: neighborhood overlap (edge thickness = overlap) <br>• `P`: node color = attribute values. |
| `--temporal_simulation file.csv` | Simulate edge additions/removals over time from a CSV.                                                           |     |                                                                                                                                                                                                |
| `--output out.gml`               | Export processed or annotated graph to a `.gml` file.                                                            |     |                                                                                                                                                                                                |
| `--split_output_dir path/`       | Save each community as a separate `.gml` file.                                                                   |     |                                                                                                                                                                                                |

---

## 📘 Example Files

### `sample_graph.gml`

```gml
graph [
  node [ id "A" label "Alice" color "red" ]
  node [ id "B" label "Bob" color "blue" ]
  node [ id "C" label "Carol" color "red" ]
  node [ id "D" label "Dan" color "blue" ]
  edge [ source "A" target "B" weight 1.0 sign 1 ]
  edge [ source "A" target "C" weight 1.0 sign 1 ]
  edge [ source "B" target "D" weight 1.0 sign -1 ]
  edge [ source "C" target "D" weight 1.0 sign 1 ]
]
```

### `edges.csv`

```csv
source,target,timestamp,action
A,D,1,add
B,C,2,add
A,B,3,remove
```

---

## 🧮 Example Usages

### 1️⃣ Partition and Plot Clustering

```bash
python graph_analysis.py sample_graph.gml --components 3 --plot C --output out.gml
```

**Output:**

```
[INFO] Loaded graph with 4 nodes and 4 edges.
[INFO] Partitioned graph into 3 communities.
[INFO] Graph exported to out.gml
```

---

### 2️⃣ Simulate Failures

```bash
python graph_analysis.py sample_graph.gml --simulate_failures 3
```

**Output:**

```
[INFO] Failures: removed 3 edges
       Components: 2
       Avg shortest path: 0.000
```

---

### 3️⃣ Verify Homophily and Balance

```bash
python graph_analysis.py sample_graph.gml --verify_homophily --verify_balanced_graph
```

**Output:**

```
[INFO] Homophily t-test: t=1.234, p=0.217
[INFO] Balanced graph check: 0 unbalanced triangles.
```

---

### 4️⃣ Temporal Simulation

```bash
python graph_analysis.py sample_graph.gml --temporal_simulation edges.csv
```

**Output:**

```
[INFO] Loaded graph with 4 nodes and 4 edges.
[TIME] Added edge A-D
[TIME] Added edge B-C
[TIME] Removed edge A-B
```

---

### 5️⃣ Robustness Check

```bash
python graph_analysis.py sample_graph.gml --robustness_check 3
```

**Output:**

```
[INFO] Robustness: Avg comps=2.40, Max size=3
```

---

## 📊 Approach Summary

### Clustering Coefficient

Computed with `nx.clustering(G)`, measuring how interconnected each node’s neighbors are.

### Neighborhood Overlap

Calculated per edge using shared neighbor ratio. Stored as `overlap` edge attribute.

### Community Detection

Girvan–Newman algorithm used to partition graph into modular communities.

### Homophily Verification

A **t-test** compares clustering coefficients between attribute-based node groups.

### Structural Balance

BFS traversal checks for signed triads where sign product < 0 (unbalanced triads).

### Failure Simulation & Robustness

Randomly remove *k* edges and measure the resulting structure. `--robustness_check` averages across multiple trials.

### Temporal Simulation

Processes edge events over timestamps, logging additions/removals step-by-step.

---

## 📦 Output Files

| File              | Description                                          |
| ----------------- | ---------------------------------------------------- |
| `out.gml`         | Exported graph with updated metrics and annotations. |
| `component_*.gml` | Separate files when using `--split_output_dir`.      |
| `plot.png`        | Visualization saved automatically from `--plot`.     |

---

## ✅ Submission Checklist

* [x] `graph_analysis.py`
* [x] `README.md`
* [x] `sample_graph.gml`
* [x] `edges.csv`
