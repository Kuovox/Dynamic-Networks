# Information Network and the WWW Assignment

**Course:** CECS 427 (Sec. 02)

**Professor:** Oscar Morales-Ponce

**Date:** 11/18/2025

**Authors:**

- Khoa Vu (030063200)
- Mya Barragan (029948137)

---

## Overview

This project implements a web crawler, directed graph generator, and PageRank analyzer using Python.
The program:
1. Crawls the web starting from seed URLs and restricted to a specified domain.
2. Builds a directed graph where nodes represent web pages and edges represent hyperlinks.
3. Computes the PageRank of each page in the graph.
4. Optionally loads an existing `.gml` graph instead of crawling.
5. Generates a log-log degree distribution plot to analyze the network structure.

The tool reads input parameters from the command line and supports multiple tasks such as crawling, PageRank computation, graph export, and visualization.

---

## Installation and Setup

### Requirements

Install the required dependencies:

```bash
pip install networkx matplotlib requests beautifulsoup4
```

---

## Running the Program

Execute the script from the terminal:

```bash
python ./page_rank.py [OPTIONS]
```

### Examples
1. Crawl the web, compute PageRank, save graph, and generate log-log plot:

```bash
python page_rank.py --crawler crawler.txt \
    --loglogplot \
    --crawler_graph out_graph.gml \
    --pagerank_values node_rank.txt \
    --plot crawler_graph.png --plot_pick degree
```

2. Use an existing graph instead of crawling:

```bash
python ./page_rank.py \
  --input graph.gml \
  --loglogplot \
  --pagerank_values node_rank.txt
```

---

## Command-Line Options

| Option / Argument        | Description                                                                                      |
| ------------------------ | ------------------------------------------------------------------------------------------------ |
| `--crawler FILE`         | Reads crawling configuration from `crawler.txt` and generates a directed graph via web scraping. |
| `--input graph.gml`      | Loads an existing directed graph in GML format instead of crawling.                              |
| `--loglogplot`           | Produces a log-log degree distribution plot (`loglog_plot.png`).                                 |
| `--crawler_graph FILE`   | Saves the generated crawler graph to a GML file.                                                 |
| `--pagerank_values FILE` | Outputs PageRank values of all nodes to a text file.                                             |

---

## Crawler Input File Format (`crawler.txt`)

The crawler configuration file contains:

```php-template
<max_nodes>
<domain>
<seed_url_1>
<seed_url_2>
...
```

Example:

```ruby
200
https://dblp.org
https://dblp.org/search
https://dblp.org/search?q=graph
https://dblp.org/search?q=computer+science
```

- max_nodes: Maximum nodes/pages to crawl
- domain: Only pages beginning with this prefix are visited
- seed URLs: BFS starting points

To avoid generating a star graph, seed pages were chosen from DBLP sections that contain many interlinked HTML pages (e.g., `/search`, `/faq`, `/about/`). These pages tend to link to multiple other pages within the domain, producing a more realistic, interconnected web graph as required by the assignment.

All crawled pages must belong to the specified domain (e.g., `https://dblp.org/pid`).

---

## Features and Workflow
### 1. Web Crawling
- Visits HTML pages only
- Restricts all outgoing links to the same domain
- Performs BFS traversal
- Stops when the number of fetched nodes reaches `max_nodes`
- Builds a directed graph where:
  - Node = web page URL
  - Edge: A → B if A contains a hyperlink to B
- **Note on robots.txt:**  
  - DBLP restricts crawling of many `/pid/` and `/rec/` pages via robots.txt.
  - For educational purposes, robots.txt checks were disabled so the crawler could access pages necessary for generating the graph dataset.
 
### 2. Graph Handling
The program supports two graph modes:
- Crawled Graph
  - Generated from scratch using `--crawler crawler.txt`.
- Imported Graph
  - Loaded directly from `.gml` via `networkx.read_gml()`.

Both forms produce a `networkx.DiGraph`.

### 3. PageRank Algorithm
The program computes:
```python
nx.pagerank(G, alpha=0.85)
```

Outputs sorted scores to the file specified with:
```css
--pagerank_values node_rank.txt
```

Example output:
```ruby
https://dblp.org/pid/e/PErdos.html 0.002931
https://dblp.org/pid/s/PaulGSpirakis.html 0.001842
...
```

### 4. Log-Log Plot

A log-log plot is generated to analyze scale-free properties of the web graph:
- x-axis: degree
- y-axis: number of nodes with that degree
- Saved as `loglog_plot.png`

This plot helps reveal power-law degree behavior commonly found in web graphs.

---

## Example Output Files
| File / Output     | Description                                |
| ----------------- | ------------------------------------------ |
| `out_graph.gml`   | Directed graph produced by the crawler.    |
| `node_rank.txt`   | PageRank values of all pages in the graph. |
| `loglog_plot.png` | Log-log degree distribution of the graph.  |
| `crawler_graph.png` | Visualization of an induced subgraph (11 nodes). This graph highlights cross-links in the crawled graph and demonstrates a non-star, web-like structure. |

---

## Approach Summary

1. Parsing Input
    - Reads crawler parameters or loads `.gml` file.
    
2. Crawling Strategy
    - BFS traversal
    - Only HTML pages
    - Only the given domain
    - Crawling configuration was chosen to avoid trivial star graphs (as required by the assignment). Seeds were selected from DBLP pages with rich internal link structures (e.g., `/search`, `/about/`, `/faq/`) to ensure the resulting graph reflects web-like connectivity rather than a single dominating hub.

3. Directed Graph Construction
    - Uses NetworkX DiGraph
    - Adds edges for every discovered hyperlink
    
4. PageRank Computation
    - Uses damping factor α = 0.85
    - Normalizes probabilities across nodes
    
5. Degree Distribution Plotting
    - Computes histogram of node degrees
    - Plotted in log-log scale using matplotlib

--- 

## Submission Checklist
- `page_rank.py`
- `README.md`
- `crawler.txt`
- `graph.gml` (if using provided dataset)
- Sample outputs:
  - `out_graph.gml`
  - `node_rank.txt`
  - `loglog_plot.png`
 
---

## Citations
1) Machine Learning Mastery (web crawling)
  Brownlee, J. (n.d.). How to Use Web Crawling in Python. Machine Learning Mastery. Retrieved from https://machinelearningmastery.com/web-crawling-in-python

2) ZenRows (Python web crawler tutorial)
  ZenRows. (n.d.). How to Build a Web Crawler in Python (Step-by-Step Tutorial). ZenRows Blog. Retrieved from https://www.zenrows.com/blog/web-crawler-python

3) GeeksforGeeks (PageRank implementation)
  GeeksforGeeks. (n.d.). PageRank Algorithm Implementation in Python. GeeksforGeeks. Retrieved from https://www.geeksforgeeks.org/python/page-rank-algorithm-implementation
