
# Game Theory Assignment -- Traffic Equilibrium Analysis Tool

**Course:** CECS 427 (Sec. 02)

**Professor:** Oscar Morales-Ponce

**Date:** 10/21/2025

**Authors:**

- Khoa Vu (030063200)
- Mya Barragan (029948137)

---

## 🧠 Overview

This project implements a **Traffic Equilibrium Analysis Tool** using Python. The program computes and visualizes the **Travel Equilibrium (Nash Equilibrium)** and **Social Optimality** in a directed traffic network.  

Given a directed graph where each edge is defined by a **cost function** of the form:

\[
c(x) = a x + b
\]

the program determines how vehicles distribute themselves along the available paths between an initial and final node to achieve both **individual equilibrium** and **system-wide efficiency**.

The program reads `.gml` files describing the graph structure and edge parameters, performs equilibrium calculations, and optionally generates visualizations of the network and its edge cost functions.

---

## ⚙️ Installation and Setup

### Requirements

Install dependencies before running the script:

```bash
pip install networkx matplotlib scipy

