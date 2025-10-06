# Social and Large-Scale Networks Assignment -- Graph Analysis Tool

**Course:** CECS 427 (Sec. 02)

**Professor:** Oscar Morales-Ponce

**Date:** 10/07/2025

**Authors:**

- Khoa Vu (030063200)
- Mya Barragan (029948137)

------------------------------------------------------------------------

## 📌 Overview

This project provides a Python-based command-line tool for analyzing, visualizing, and simulating social and large-scale networks.

It supports clustering coefficient computation, neighborhood overlap, community detection, homophily verification, robustness checks, temporal simulations, and more.

---

## 📦 Setup Instructions

### Requirements

* Python 3.8+
* Libraries:

  ```bash
  pip install networkx matplotlib scipy
  ```

### Files

* `graph_analysis.py` → main script
* `sample_graph.gml` → example input graph
* `edges.csv` → example temporal edge simulation file

---

## ▶️ Usage

General syntax:

```bash
python graph_analysis.py graph_file.gml [OPTIONS]
```

### Examples

1. **Partition into 3 components, plot clustering, simulate 5 failures, save output**

```bash
python graph_analysis.py sample_graph.gml --components 3 --plot C --simulate_failures 5 --output output.gml
```

2. **Temporal simulation**

```bash
python graph_analysis.py sample_graph.gml --plot T --temporal_simulation edges.csv
```

3. **Verify homophily and structural balance**

```bash
python graph_analysis.py sample_graph.gml --verify_homophily --verify_balanced_graph --output out.gml
```

---

## 🧮 Features & Approach

### 1. Graph Loading / Exporting

* Loads `.gml` graphs with **node/edge attributes** using NetworkX.
* Exports modified graphs with computed attributes.

### 2. Clustering Coefficient

* Computed with `nx.clustering(G)` for each node.
* Saved as node attribute `"clustering"`.

### 3. Neighborhood Overlap

* For each edge `(u,v)`, overlap =
  [
  \frac{|\text{common neighbors}(u,v)|}{\min(\deg(u)-1, \deg(v)-1)}
  ]
* Saved as edge attribute `"overlap"`.

### 4. Community Detection

* Uses **Girvan-Newman** method.
* Assigns `"community"` attribute to each node.

### 5. Visualization (`--plot`)

* `C`: Node size = clustering coefficient, color = degree.
* `N`: Edge thickness = neighborhood overlap, color = degree sum.
* `P`: Attribute-based visualization (e.g., node color, signed edges).
* `T`: Temporal evolution (requires `edges.csv`).

### 6. Homophily Test

* Uses **t-test** comparing edges with same vs. different node attributes (e.g., `"color"`).

### 7. Balanced Graph Verification

* Checks if signed graph (edges with `sign=±1`) is structurally balanced.

### 8. Failure Simulation (`--simulate_failures k`)

* Randomly removes `k` edges.
* Reports:

  * Change in average shortest path.
  * Number of disconnected components.
  * Betweenness centrality distribution.

### 9. Robustness Check (`--robustness_check k`)

* Runs multiple random failure simulations.
* Reports:

  * Avg # of components.
  * Max/min component sizes.
  * Cluster persistence.

### 10. Temporal Simulation (`--temporal_simulation file.csv`)

* Reads time series of edge changes:

  ```csv
  source,target,timestamp,action
  A,B,1,add
  B,C,2,remove
  ```
* Dynamically updates graph.

---

## 📂 Example Input Files

### `sample_graph.gml`

```gml
graph [
  directed 0
  node [
    id "A"
    label "Alice"
    color "red"
  ]
  node [
    id "B"
    label "Bob"
    color "red"
  ]
  node [
    id "C"
    label "Charlie"
    color "blue"
  ]
  node [
    id "D"
    label "Diana"
    color "blue"
  ]
  edge [
    source "A"
    target "B"
    sign 1
  ]
  edge [
    source "A"
    target "C"
    sign -1
  ]
  edge [
    source "B"
    target "D"
    sign 1
  ]
  edge [
    source "C"
    target "D"
    sign -1
  ]
]
```

### `edges.csv`

```csv
source,target,timestamp,action
A,C,1,remove
A,D,2,add
B,C,3,add
```

---

## ✅ Submission Checklist

* [x] `graph_analysis.py`
* [x] README.md (this file)
* [x] Sample `.gml` graph (`sample_graph.gml`)
* [x] (Optional) Temporal `.csv` file (`edges.csv`)

