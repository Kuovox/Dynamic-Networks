# Graph Assignment -- Erdős--Rényi Random Graphs

**Course:** CECS 427 (Sec. 02)

**Professor:** Oscar Morales-Ponce

**Date:** 09/16/2025

**Authors:**

- Khoa Vu (030063200)
- Mya Barragan (029948137)

------------------------------------------------------------------------

## 📌 Overview

This project implements a modular Python application for generating, analyzing, and visualizing graphs, with a focus on Erdős--Rényi random graphs.

The program supports graph creation, BFS traversal, structural analysis, visualization, and exporting results.

Key Features: - Generate Erdős--Rényi random graphs with probability p = (c * ln(n))/n

- Import existing graphs from `.gml` files
  
- Perform **multi-source BFS** with shortest path tracking
  
- Identify **connected components**, **cycles**, and **isolated nodes**

- Compute **graph density** and **average shortest path length**
  
- Visualize graphs with annotations and highlighted paths

- Save enriched graphs back to `.gml`

------------------------------------------------------------------------

## ⚙️ Installation

1.  Make sure you have **Python 3.8+** installed.

2.  Install required dependencies:

    ``` bash
    pip install networkx matplotlib
    ```

------------------------------------------------------------------------

## Usage

Run the script from the command line:

``` bash
python graph.py [options]
```

### Options

-   `--input graph_file.gml`

    Load a graph from an existing `.gml` file.

-   `--create_random_graph n c`
  
    Create an Erdős--Rényi graph with **n nodes** and probability
    parameter **c**.
    
    Uses p = (c * ln(n))/n.

-   `--multi_BFS a1 a2 ...`
  
    Run BFS from one or more source nodes, storing shortest paths.

-   `--analyze`
  
    Perform structural analysis: connected components, cycle detection,
    isolated nodes, density, and average shortest path length.

-   `--plot`
  
    Display a visualization of the graph, with isolated nodes in **red**
    and BFS paths highlighted.

-   `--output out_graph_file.gml`
  
    Save the final graph with computed attributes to a `.gml` file.

------------------------------------------------------------------------

## Examples

### Example 1 -- Generate, Analyze, Plot, Save

``` bash
python graph.py --create_random_graph 200 1.5 --multi_BFS 0 5 20 --analyze --plot --output final_graph.gml
```

-   Creates a 200-node Erdős--Rényi graph
  
-   Runs BFS from nodes 0, 5, and 20
  
-   Performs full structural analysis
  
-   Plots graph with paths and isolated nodes
  
-   Saves results to `final_graph.gml`

### Example 2 -- Load Graph and Analyze

``` bash
python graph.py --input data.gml --analyze --plot
```

-   Reads `data.gml`
  
-   Analyzes structure
  
-   Displays annotated plot

------------------------------------------------------------------------

## Expected Output

-   **Terminal Output:** summary of connected components, cycles, isolated nodes, density, etc.
    
-   **Plots:** graphs with highlighted BFS paths and isolated nodes.
  
-   **.gml File:** saved graph with metadata.

Example terminal output:

    --- Graph Analysis ---
    num_components: 3
    has_cycle: True
    cycle_example: [('0', '2'), ('2', '5'), ('5', '0')]
    isolated_nodes: ['12', '47']
    density: 0.034
    avg_shortest_path_len: 3.42

------------------------------------------------------------------------

## 📂 Submission Contents

-   `graph.py` -- main source code

-   `README.md` -- this file
  
-   `sample_input.gml` -- example input graph
  
-   `sample_output.gml` -- example output after analysis
  
-   *(Optional)* screenshots of plotted graphs

------------------------------------------------------------------------

## 📚 Citations

1. GeeksforGeeks. (n.d.). Erdős–Renyi model – Generating random graphs. GeeksforGeeks. Retrieved September 2025, from https://www.geeksforgeeks.org/dsa/erdos-renyl-model-generating-random-graphs/
   
2. GeeksforGeeks. (n.d.). Breadth First Search or BFS for a Graph. GeeksforGeeks. Retrieved September 2025, from https://www.geeksforgeeks.org/dsa/breadth-first-search-or-bfs-for-a-graph/
   
3. NetworkX Developers. (n.d.). NetworkX documentation (stable). NetworkX. Retrieved September, 2025, from https://networkx.org/documentation/stable/
