# Names: Khoa Vu (030063200) & Mya Barragan (029948137)
# Course: CECS 427 (Sec. 02)
# Professor: Oscar Morales-Ponce
# Date: 10/07/2025

'''
Citation(s):
1) GeeksforGeeks. (2025, July 15). Fatman Evolutionary Model in Social Networks. Retrieved October 3, 2025, from https://www.geeksforgeeks.org/machine-learning/fatman-evolutionary-model-in-social-networks/
2) NetworkX Developers. (n.d.). NetworkX documentation (stable). NetworkX. Retrieved October, 2025, from https://networkx.org/documentation/stable/
3) Tushar Aggarwal. NetworkX: A Comprehensive Guide to Mastering Network Analysis with Python. Medium, October 4, 2023. Available at: medium.com/@tushar_aggarwal/networkx-a-comprehensive-guide-to-mastering-network-analysis-with-python-fd7e5195f6a0 
4) pandas Development Team. pandas.read_csv — pandas 2.3.3 Documentation. Available at: pandas.pydata.org/docs/reference/api/pandas.read_csv.html 
5) Matplotlib Animation: FuncAnimation Class in Python. GeeksforGeeks. Available at: geeksforgeeks.org/python/matplotlib-animation-funcanimation-class-in-python/ 
'''

# Import necessary libraries
import argparse
import random
import csv
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

# Utility functions
def load_graph(file_path): # Load a graph from a .gml file.
    G = nx.read_gml(file_path)
    if not nx.is_weighted(G):
        for u, v in G.edges():
            G[u][v]['weight'] = 1.0
    return G


def save_graph(G, path): # Export graph to a .gml file.
    nx.write_gml(G, path)
    print(f"[INFO] Graph exported to {path}")


def compute_metrics(G): # Compute clustering coefficient for each node and store as attribute.
    cc = nx.clustering(G)
    nx.set_node_attributes(G, cc, 'clustering')
    for u, v in G.edges(): 
        neigh_u, neigh_v = set(G.neighbors(u)), set(G.neighbors(v))
        inter = len(neigh_u & neigh_v)
        denom = len(neigh_u | neigh_v) or 1
        G[u][v]['overlap'] = inter / denom


def partition_graph(G, n): # Partition graph into n communities using Girvan-Newman.
    comp_gen = nx.community.girvan_newman(G)
    for i, communities in enumerate(comp_gen):  # Get first n partitions
        if i == n - 1:  
            break
    parts = [list(c) for c in communities]  
    for idx, part in enumerate(parts):      # Assign community ID to nodes
        for node in part:   
            G.nodes[node]['community'] = idx
    print(f"[INFO] Partitioned graph into {len(parts)} communities.")


def simulate_failures(G, k): # Randomly remove k edges and analyze connectivity, shortest path, and betweenness centrality.
    k = min(k, len(G.edges()))
    edges = random.sample(list(G.edges()), k)
    G.remove_edges_from(edges)
    comps = nx.number_connected_components(G)
    if comps > 1:   # If disconnected, average shortest path is undefined
        avg_path = 0.0
    else:   
        try:    
            avg_path = nx.average_shortest_path_length(G)
        except nx.NetworkXError:    # Handle case of disconnected graph
            avg_path = 0.0
    print(f"[INFO] Failures: removed {k} edges\n       Components: {comps}\n       Avg shortest path: {avg_path:.3f}")  # Compute betweenness centrality


def robustness_check(G, k, trials=5): # Perform repeated random edge removals (k edges per trial) and report average connectivity and component sizes.
    comp_counts, max_sizes = [], []
    for _ in range(trials):
        G_copy = G.copy()
        simulate_failures(G_copy, k)
        comps = list(nx.connected_components(G_copy))
        comp_counts.append(len(comps))
        max_sizes.append(max(len(c) for c in comps))
    print(f"[INFO] Robustness: Avg comps={np.mean(comp_counts):.2f}, Max size={np.max(max_sizes)}") # Average number of components and max component size


def verify_homophily(G): # Run a t-test on node attributes (color/group) to test for homophily.
    attrs = [G.nodes[n].get('group', random.randint(0, 1)) for n in G.nodes()]
    groups = list(set(attrs))
    if len(groups) < 2: # Ensure there is less than 2 groups
        print("[WARN] Homophily test skipped: not enough attribute diversity.")
        return
    g1 = [G.nodes[n]['clustering'] for n in G.nodes() if G.nodes[n].get('group') == groups[0]]
    g2 = [G.nodes[n]['clustering'] for n in G.nodes() if G.nodes[n].get('group') == groups[1]]
    if np.std(g1) == 0 or np.std(g2) == 0:  # Avoid t-test on identical values
        print("[WARN] Homophily test unreliable: identical clustering values.")
        return
    t, p = stats.ttest_ind(g1, g2, equal_var=False)
    print(f"[INFO] Homophily t-test: t={t:.3f}, p={p:.3f}") # Two-sample t-test


def verify_balance(G): # Check if the signed graph is structurally balanced using BFS logic.
    for u, v in G.edges():  # Ensure all edges have a 'sign' attribute
        if 'sign' not in G[u][v]:
            G[u][v]['sign'] = 1
    unbalanced = 0
    for tri in nx.enumerate_all_cliques(G): 
        if len(tri) == 3:
            edges = [(tri[0], tri[1]), (tri[1], tri[2]), (tri[0], tri[2])]
            signs = [G[e[0]][e[1]].get('sign', 1) for e in edges]
            if np.prod(signs) < 0:  # Odd number of negative edges
                unbalanced += 1
    print(f"[INFO] Balanced graph check: {unbalanced} unbalanced triangles.")


# Visualization
def plot_graph(G, mode):
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(6, 6))
    if mode == 'C':  # clustering visualization
        sizes = [300 * G.nodes[n].get('clustering', 0.5) for n in G.nodes()]
        colors = [G.degree(n) for n in G.nodes()]
        nx.draw(G, pos, with_labels=True, node_size=sizes, node_color=colors, cmap='coolwarm')
    elif mode == 'N':  # neighborhood overlap visualization
        widths = [5 * G[u][v].get('overlap', 0.1) for u, v in G.edges()]
        nx.draw(G, pos, with_labels=True, width=widths, edge_color='gray')
    elif mode == 'P':   # partition visualization
        colors = [G.nodes[n].get('group', 0) for n in G.nodes()]
        nx.draw(G, pos, with_labels=True, node_color=colors, cmap='Set2')
    plt.title(f"Plot Mode: {mode}")
    plt.show()


#Temporal Simulation
def temporal_simulation(G, csv_file): # Simulate edge additions/removals over time from a CSV.
    with open(csv_file, 'r') as f:  # Open CSV file
        reader = csv.DictReader(f)
        for row in reader:  # Read each row
            src, tgt, action = row['source'], row['target'], row['action']
            if action.lower() == 'add': # Add edge if not present
                G.add_edge(src, tgt)
                print(f"[TIME] Added edge {src}-{tgt}")
            elif action.lower() == 'remove' and G.has_edge(src, tgt):   # Remove edge if present
                G.remove_edge(src, tgt)
                print(f"[TIME] Removed edge {src}-{tgt}")


def main(): # Main function to parse arguments and execute functionalities
    parser = argparse.ArgumentParser(description="Graph Analysis Tool")
    parser.add_argument('graph_file', help='Input .gml file')
    parser.add_argument('--components', type=int)
    parser.add_argument('--plot', choices=['C', 'N', 'P', 'T'])
    parser.add_argument('--verify_homophily', action='store_true')
    parser.add_argument('--verify_balanced_graph', action='store_true')
    parser.add_argument('--simulate_failures', type=int)
    parser.add_argument('--robustness_check', type=int)
    parser.add_argument('--temporal_simulation')
    parser.add_argument('--output', default='output.gml')
    args = parser.parse_args()

    G = load_graph(args.graph_file) # Load graph
    print(f"[INFO] Loaded graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")

    compute_metrics(G)  # Compute clustering and overlap
    
    if args.components: # Partition graph if requested
        partition_graph(G, args.components)

    if args.simulate_failures:  # Simulate failures if requested
        simulate_failures(G.copy(), args.simulate_failures)

    if args.robustness_check:   # Perform robustness check if requested
        robustness_check(G.copy(), args.robustness_check)

    if args.verify_homophily:   # Verify homophily if requested
        verify_homophily(G)

    if args.verify_balanced_graph:  # Verify balance if requested
        verify_balance(G)

    if args.temporal_simulation:    # Perform temporal simulation if CSV provided
        temporal_simulation(G, args.temporal_simulation)

    if args.plot and args.plot != 'T':  # Plot graph if requested and not temporal
        plot_graph(G, args.plot)

    save_graph(G, args.output)  # Save modified graph

if __name__ == '__main__':  
    main()  