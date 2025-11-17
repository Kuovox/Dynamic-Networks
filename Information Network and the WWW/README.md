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
python ./page_rank.py \
  --crawler crawler.txt \
  --loglogplot \
  --crawler_graph out_graph.gml \
  --pagerank_values node_rank.txt
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
100
https://dblp.org/pid
https://dblp.org/pid/e/PErdos.html
https://dblp.org/pid/s/PaulGSpirakis.html
https://dblp.org/pid/89/8192.html
```

- max_nodes: Maximum nodes/pages to crawl
- domain: Only pages beginning with this prefix are visited
- seed URLs: BFS starting points

All crawled pages must belong to the specified domain (e.g., `https://dblp.org/pid`).

---

## Features and Workflow
