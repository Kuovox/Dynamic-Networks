# Names: Khoa Vu (030063200) & Mya Barragan (029948137)
# Course: CECS 427 (Sec. 02)
# Professor: Oscar Morales-Ponce
# Date: 10/21/2025

'''
Citation(s):
1) NetworkX Developers. (n.d.). NetworkX documentation (stable). NetworkX. Retrieved October, 2025, from https://networkx.org/documentation/stable/
2) NetworkX’s network_simplex algorithm documentation “network_simplex — NetworkX 3.5 documentation” 
3) A Medium article showing how to build a simple traffic model with NetworkX in Python “How to Build a Simple Traffic Model with NetworkX in Python”
4) The Matplotlib Pyplot tutorial “Pyplot tutorial — Matplotlib 3.10.6 documentation”
'''

import argparse # Handles command-line arguments
import networkx as nx # Used to load, store, and manipulate graphs (nodes, edges, attributes).
import matplotlib.pyplot as plt # Used for plotting and visualizing the graph.
from scipy.optimize import minimize # Performs numerical optimization — finds the flow that minimizes cost or equalizes path costs.

def parse_args(): # Defines how the program reads arguments from the terminal.
    parser = argparse.ArgumentParser(description="Traffic equilibrium and social optimum analyzer")
    parser.add_argument("gml_file", help="Input GML file")
    parser.add_argument("n", type=float, help="Number of vehicles")
    parser.add_argument("source", type=int, help="Source node ID")
    parser.add_argument("target", type=int, help="Target node ID")
    parser.add_argument("--plot", action="store_true", help="Plot graph and cost functions")
    return parser.parse_args()

def read_graph(gml_file):
    try:
        G = nx.read_gml(gml_file) # Uses NetworkX to read the .gml file (a structured graph file format).
        # Returns a DiGraph (directed graph) object where nodes and edges have attributes.

        # Convert string node labels like "0", "1" to integers
        mapping = {}
        for node in G.nodes():
            # Only convert if node looks like an integer string (like '1') into integers.
            if isinstance(node, str) and node.isdigit():
                mapping[node] = int(node)
            else:
                mapping[node] = node

        # Apply the new mapping (relabels nodes)
        G = nx.relabel_nodes(G, mapping) # Relabels the graph’s nodes to use integers.
        print("[DEBUG] Nodes after relabeling:", list(G.nodes())) # Prints all node names (for debugging) and returns the cleaned graph object.
        return G

    except Exception as e: # Catches any errors (e.g., missing file or invalid format) and safely exits the program.
        print(f"Error reading GML: {e}")
        exit(1)

def compute_paths(G, source, target): # Finds all simple paths (no repeated nodes) from source to target.
    return list(nx.all_simple_paths(G, source, target)) # Uses NetworkX’s built-in path search function.
    '''
    Example output:
    [[0, 1, 3], [0, 2, 3]]
    '''    

def path_cost(G, path, flow): # Returns the total cost of that path for that flow.
    cost = 0
    for u, v in zip(path[:-1], path[1:]):
        a = G[u][v]['a']
        b = G[u][v]['b']
        cost += a * flow + b 
        # a and b are stored as edge attributes in the .gml file.
        # For each edge along the path, it adds the cost given the current flow x.
    return cost

def equilibrium(G, paths, n): # Defines an internal function eq_condition(f1) that returns the difference between path costs.
    '''
    At equilibrium:
        Both used paths have equal travel times (costs).
        If costs differ, drivers would switch until they equalize.
    '''
    def eq_condition(f1):
        f2 = n - f1
        c1 = path_cost(G, paths[0], f1)
        c2 = path_cost(G, paths[1], f2)
        return abs(c1 - c2)
    res = minimize(eq_condition, x0=[n/2], bounds=[(0, n)]) # Uses SciPy’s minimize to find f1 (flow on path 1) where cost difference is minimized (i.e., equilibrium).
    f1 = res.x[0]
    f2 = n - f1
    return f1, f2 # the flow on each path.

def social_optimum(G, paths, n): # Calculates total system cost for given f1, f2.
    def total_cost(flows):
        f1, f2 = flows
        f2 = n - f1
        return f1 * path_cost(G, paths[0], f1) + f2 * path_cost(G, paths[1], f2)
    res = minimize(total_cost, x0=[n/2], bounds=[(0, n)]) 
    f1 = res.x[0]
    f2 = n - f1
    return f1, f2 

def plot_graph(G):
    '''
    Visualizes the graph using NetworkX + Matplotlib.
    Each edge is labeled with its cost function (e.g., 1x+0).
    spring_layout gives nodes an appealing, force-based layout.
    '''
    pos = nx.spring_layout(G)
    labels = { (u,v): f"{G[u][v]['a']}x+{G[u][v]['b']}" for u,v in G.edges() }
    nx.draw(G, pos, with_labels=True, node_color='lightblue')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.show()
    
def main():
    args = parse_args()
    G = read_graph(args.gml_file) # Reads arguments and loads the graph.

    # Ensures compatibility if graph uses string labels (like "Start", "End") instead of integers.
    if args.source not in G.nodes:
        args.source = str(args.source)
    if args.target not in G.nodes:
        args.target = str(args.target)

    # Prints debug info to confirm everything loaded correctly.
    print("[DEBUG] Nodes after relabeling:", list(G.nodes()))
    print("[DEBUG] Using source:", args.source)
    print("[DEBUG] Using target:", args.target)

    # Compute all simple paths between source and target
    paths = compute_paths(G, args.source, args.target)
    print("[DEBUG] Paths found:", paths)

    if not paths:
        print("[ERROR] No valid paths found between source and target!")
        exit(1) # Exits if no path exists.

    # Compute travel equilibrium
    try:
        f_eq = equilibrium(G, paths, args.n)
        print("\n=== Travel Equilibrium (Nash Equilibrium) ===")
        for i, f in enumerate(f_eq):
            print(f"Path {i+1}: Flow = {f:.2f}")
    except Exception as e: # Catches any errors (e.g., numerical issues).
        print(f"[ERROR] Failed to compute equilibrium: {e}")

    # Compute social optimum
    try:
        f_opt = social_optimum(G, paths, args.n)
        print("\n=== Social Optimum ===")
        for i, f in enumerate(f_opt):
            print(f"Path {i+1}: Flow = {f:.2f}")
    except Exception as e:
        print(f"[ERROR] Failed to compute social optimum: {e}")

    # Plot graph if requested
    if args.plot:
        try:
            plot_graph(G)
        except Exception as e:
            print(f"[ERROR] Plotting failed: {e}")

if __name__ == "__main__":
    main()