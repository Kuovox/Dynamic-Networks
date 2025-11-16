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

