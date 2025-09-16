# Names: Khoa Vu (030063200) & Mya Barragan (029948137)
# Course: CECS 427 (Sec. 02)
# Professor: Oscar Morales-Ponce
# Date: 09/11/2025

'''
Citation(s):
1) GeeksforGeeks. (n.d.). Erdős–Renyi model – Generating random graphs. GeeksforGeeks. Retrieved September 2025, from https://www.geeksforgeeks.org/dsa/erdos-renyl-model-generating-random-graphs/
2) GeeksforGeeks. (n.d.). Breadth First Search or BFS for a Graph. GeeksforGeeks. Retrieved September 2025, from https://www.geeksforgeeks.org/dsa/breadth-first-search-or-bfs-for-a-graph/
3) NetworkX Developers. (n.d.). NetworkX documentation (stable). NetworkX. Retrieved September, 2025, from https://networkx.org/documentation/stable/
'''

import argparse
import math # needed for ln(n) in probability
import networkx as nx # main graph library
import matplotlib.pyplot as plt # for visualization

def create_random_graph(n, c): # graph generation
    '''
    Generates a new Erdős–Rényi random graph with n nodes and edge probability p = c * ln(n) / n.
    Arguments:
        n (int): number of nodes
        c (float): parameter for the edge probability
    Returns:
        G (networkx.Graph): generated graph

    '''
    p = (c * math.log(n)) / n # formula for probability 
    G = nx.erdos_renyi_graph(n, p) # generates random G(n,p)

    # Label nodes as strings ("0", "1", ..., "n-1")
    mapping = {i: str(i) for i in range(n)} # relabels nodes to strings
    return nx.relabel_nodes(G, mapping) # returns graph

def multi_source_bfs(G, sources): # BFS
    '''
    Perform BFS from multiple source nodes and store the shortest paths.
    Arguments:
        G (networkx.Graph): input graph
        source (list of str): source node IDs
    Returns
        dict: {source: {target: path}}
    '''
    paths = {}
    for s in sources:
        if s not in G: # check node exists
            print(f"Warning: source node {s} not in the graph")
            continue
        
        # Use shortest_path built-in from NetworkX (BFS on unweighted graph)
        paths[s] = dict(nx.single_source_shortest_path(G, s)) # BFS paths
    return paths

def analyze_graph(G): # graph analysis
    '''
    Perform structural analyses on the graph.
    Returns: 
        dict with results
    '''
    results = {}

    # Connected components
    components = list(nx.connected_components(G)) # find connected components & G = input graph
    results["num_components"] = len(components)

    # Cycle detection (any simple cycle)
    try: 
        cycle = nx.find_cycle(G) # raises error if no cycle
        results["has_cycle"] = True
        results["cycle_example"] = cycle
    except nx.NetworkXNoCycle:
        results["has_cycle"] = False

    # Isolated nodes
    results["isolated_nodes"] = list(nx.isolates(G)) # identifies nodes that are not connected to any other node.

    # Graph density
    results["density"] = nx.density(G)

    # Average shortest path length (only if connected)
    if nx.is_connected(G):
        results["avg_shortest_path_len"] = nx.average_shortest_path_length(G)
    else:
        results["avg_shortest_path_len"] = None
    return results

def plot_graph(G, bfs_paths=None, analysis=None):
    '''
    Visualize the graph, highlight BFS paths and isolated nodes.

    Arguments:
        G(networkx.Graph): input graph
        bfs_Paths (dict): paths from BFS
        analysis (dict): results from analyze 
    '''

    pos = nx.spring_layout(G, seed=42)

    plt.figure(figsize=(8,8))

    # Draw base graph w/ light blue
    nx.draw_networkx(G, pos, node_color="lightblue", with_labels=True, node_size=500)

    # Highlight isolated nodes w/ red
    if analysis and analysis["isolated_nodes"]:
        nx.draw_networkx_nodes(
            G, pos,
            nodelist=analysis["isolated_nodes"],
            node_color="red",
            node_size=600
        )

    # Highlight BFS paths w/ colored edges per source
    if bfs_paths:
        colors = ["green", "orange", "purple", "cyan"]
        for i, (src, paths) in enumerate(bfs_paths.items()):
            color = colors[i % len(colors)]
            for path in paths.values():
                edges = list(zip(path[:-1], path[1:]))
                nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color=color, width=2)
    
    plt.title("Graph Visualization with BFS & Analysis")
    plt.show()

# --output out_graph_file.gml
def save_graph(G, filename):
    '''Save graph to .gml file.'''
    nx.write_gml(G, filename)

def load_graph(filename):
    '''Load graph from .gml files'''
    return nx.read_gml(filename)


def main():
    parser = argparse.ArgumentParser(description="Graphs Tool") # Creates an argument parser that reads command-line options; python graph.py -h

    parser.add_argument("--input", type=str, help="Input .gml file") # Defines an optional argument --input that expects a string (a filename); --input my_graph.gml.
    parser.add_argument("--create_random_graph", nargs=2, metavar=("n", "c"), # Defines --create_random_graph which takes 2 arguments: n = number of nodes & c = parameter for probability formula; nargs=2 means it needs exactly 2 values; --create_random_graph 100 1.5
                        help="Generate Erdős–Rényi graph with n nodes and parameter c")
    parser.add_argument("--multi_BFS", nargs="+", help="Perform BFS from given source nodes") # Defines --multi_BFS which accepts 1 or more values and nargs="+" means "one or more arguments"; Example: --multi_BFS 0 2 7
    parser.add_argument("--analyze", action="store_true", help="Analyze graph structure") # A flag argument (boolean switch) and if present, it sets args.analyze = True; --analyze
    parser.add_argument("--plot", action="store_true", help="Plot graph") # Another flag. If used, program plots the graph; --plot.
    parser.add_argument("--output", type=str, help="Output .gml file") # Defines an optional argument --output that expects a string (a filename); --output final_graph.gml 

    args = parser.parse_args() # Actually reads the arguments typed on the command line and stores them inside args.
    # Example: python graph.py --create_random_graph 50 1.2 --plot then args.create_random_graph = ["50", "1.2"], args.plot = True

    # Load or create graph
    if args.create_random_graph:
        n = int(args.create_random_graph[0]) # the number of nodes (converted from string to int).
        c = float(args.create_random_graph[1]) # the probability parameter (converted to float).
        G = create_random_graph(n, c)
    elif args.input: # If no random graph was requested, but --input was given:
        G = load_graph(args.input) # Loads an existing .gml graph file from disk using load_graph().
    else:
        print("Error: must specify --input or --create_random_graph")
        return
    
    # BFS
    bfs_paths = None # Initializes as empty(None)
    if args.multi_BFS: # If user passed --multi_BFS with node IDs:
        bfs_paths = multi_source_bfs(G, args.multi_BFS) # Calls multi_source_bfs(G, args.multi_BFS) which computes all shortest paths and stores results in bfs_paths (a dictionary of paths).

    # Analysis
    results = None
    if args.analyze: # If --analyze flag is set:
        results = analyze_graph(G) # Calls analyze_graph(G) which runs connected components, cycle detection, density, etc.
        print("\n--- Graph Analysis ---")
        for k, v in results.items():
            print(f"{k}: {v}")

    # Plotting
    if args.plot: # If --plot is present:
        plot_graph(G, bfs_paths=bfs_paths, analysis=results)
        # The graph G
        # The BFS paths (if any were computed)
        # The analysis results (if computed)

    # Save output
    if args.output: # If the user passed --output filename.gml
        save_graph(G, args.output) # Saves the graph to that file and this exported graph will include all metadata.

if __name__ == "__main__":
    main()
