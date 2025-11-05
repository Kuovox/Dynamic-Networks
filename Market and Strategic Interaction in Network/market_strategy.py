# Names: Khoa Vu (030063200) & Mya Barragan (029948137)
# Course: CECS 427 (Sec. 02)
# Professor: Oscar Morales-Ponce
# Date: 11/04/2025

"""
Citation(s):
1) NetworkX Developers. (2025). read_gml — NetworkX 3.5 documentation. Retrieved from https://networkx.org/documentation/stable/reference/readwrite/generated/networkx.readwrite.gml.read_gml.html
2) NetworkX Developers. (2025). hopcroft_karp_matching — NetworkX 3.5 documentation. Retrieved from https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.bipartite.matching.hopcroft_karp_matching.html
3) Sundararajan, B. (2024, February 5). Optimizing Networks with Bipartite Graphs: A Practical Guide. Medium. Retrieved from https://medium.com/%40bragadeeshs/optimizing-networks-with-bipartite-graphs-a-practical-guide-7c94e9de0bc6
"""

import argparse
import sys
import math
import networkx as nx
import matplotlib.pyplot as plt

def read_graph(filename):
    """
    Load and read a GML file using NetworkX, validates nodes 'id' (label=None) so 'label' attribute is not required, and exits cleanly if the file is missing or malformed.
    """
    try:
        G = nx.read_gml(filename, label=None)
    except FileNotFoundError:
        print(f"[ERROR] File '{filename}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Error reading {filename}: {e}")
        sys.exit(1)

    if len(G) == 0:
        print(f"[ERROR] Graph '{filename}' is empty.")
        sys.exit(1)

    return G

def plot_graph(G, title="Preference Graph"):
    """
    Plot a (small) bipartite graph G. Seller nodes (0..n-1) are blue, buyers green.
    Edge labels show valuation when present.
    Visualizes graphs using matplotlib:
        Blue = sellers
        Green = buyers 
        Edge labels = valuations 
            Used when user passes --plot.
    """
    pos = nx.spring_layout(G, seed=42)
    n_nodes = len(G.nodes())
    n = n_nodes // 2

    # Determine seller vs buyer lists by numeric id
    sellers = [node for node in G.nodes() if int(node) < n]
    buyers = [node for node in G.nodes() if int(node) >= n]

    nx.draw_networkx_nodes(G, pos, nodelist=sellers, node_color='lightblue', node_size=150, label='Sellers') 
    nx.draw_networkx_nodes(G, pos, nodelist=buyers, node_color='lightgreen', node_size=150, label='Buyers')
    nx.draw_networkx_labels(G, pos, labels={n: str(n) for n in G.nodes()})
    nx.draw_networkx_edges(G, pos, edge_color='gray', width=2)

    # edge valuation labels if available
    edge_labels = {}
    for u, v, data in G.edges(data=True):
        if 'valuation' in data:
            edge_labels[(u, v)] = str(data['valuation'])
        elif 'val' in data:
            edge_labels[(u, v)] = str(data['val'])
    if edge_labels:
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.title(title)
    plt.axis('off')
    plt.legend(scatterpoints=1)
    plt.savefig("Prefrence_Graph.png")

def get_preference_graph(G):
    """
    Build preference graph pref_G containing only edges (buyer, seller) where:
        valuation - price > 0
    Returns an undirected graph pref_G with same node set as G but only chosen edges.
    So buyers only consider sellers who still yield positive utility.
    """
    pref_G = nx.Graph()
    pref_G.add_nodes_from(G.nodes(data=True))

    n_nodes = len(G.nodes())
    if n_nodes % 2 != 0:
        raise ValueError("Graph must have 2n nodes (even).")
    n = n_nodes // 2

    sellers = [node for node in G.nodes() if int(node) < n]
    buyers = [node for node in G.nodes() if int(node) >= n]

    for b in buyers:
        # For each buyer, inspect seller neighbors in original graph and select
        # only those with positive utility (valuation - price > 0).
        for nbr in G.neighbors(b):
            # ensure neighbor is seller
            if int(nbr) >= n:
                continue
            edge_data = G.get_edge_data(b, nbr) or G.get_edge_data(nbr, b)
            if edge_data is None:
                continue
            if 'valuation' not in edge_data:
                raise ValueError(f"Edge ({b},{nbr}) missing 'valuation' attribute.")
            valuation = float(edge_data['valuation'])
            price = float(G.nodes[nbr].get('price', 0))
            utility = valuation - price
            if utility > 0:  # strictly positive utility only
                pref_G.add_edge(b, nbr, valuation=valuation)
    return pref_G

def market_clearing(G, interactive=False, plot=False, max_rounds=10000):
    """
    Run market-clearing:
      - buyers with no positive options are inactive (payoff 0)
      - active buyers must be matched
      - constricted sellers (via alternating reachability) have prices increased
    """
    n_nodes = len(G.nodes())
    if n_nodes % 2 != 0:
        raise ValueError("Graph must have 2n nodes (even).")
    n = n_nodes // 2

    sellers = set(node for node in G.nodes() if int(node) < n)
    buyers = set(node for node in G.nodes() if int(node) >= n)

    # ensure default prices exist
    for s in sellers:
        if 'price' not in G.nodes[s]:
            G.nodes[s]['price'] = 0.0
        else:
            # normalize to float
            G.nodes[s]['price'] = float(G.nodes[s]['price'])

    rounds = 0
    while True:
        rounds += 1
        if rounds > max_rounds:
            print(f"[STOP] Reached max_rounds={max_rounds}. Terminating to avoid runaway.")
            break

        pref_G = get_preference_graph(G)

        # Identify active buyers = buyers with at least one positive-utility seller (i.e., degree>0 in pref_G)
        active_buyers = {b for b in buyers if pref_G.degree(b) > 0}
        inactive_buyers = buyers - active_buyers

        # If there are no active buyers, market cleared by assignment rule
        if len(active_buyers) == 0:
            if interactive:
                print(f"\n--- Round {rounds} ---")
                print("Matching: set()")
                print("[INFO] No active buyers (all have non-positive utilities). Market cleared.")
                print("Inactive buyers:", sorted(list(inactive_buyers), key=lambda x: int(x)))
            break

        # compute maximum bipartite matching using Hopcroft-Karp
        try:
            from networkx.algorithms.bipartite.matching import hopcroft_karp_matching
        except Exception:
            # fallback to max_weight_matching if hopcroft not available (but prefer hopcroft)
            matching_dict = {}
            mwm = nx.algorithms.matching.max_weight_matching(pref_G, maxcardinality=True)
            # convert to dict: for each (u,v) pair
            for u, v in mwm:
                matching_dict[u] = v
                matching_dict[v] = u
        else:
            # hopcroft expects top_nodes set = sellers or buyers. We'll pass sellers side.
            matching_dict = hopcroft_karp_matching(pref_G, top_nodes=sellers)

        # Extract matched pairs (buyer,seller) where buyer in buyers and seller in sellers
        matched_pairs = set()
        matched_buyers = set()
        matched_sellers = set()
        for u, v in matching_dict.items():
            if u in buyers and v in sellers:
                matched_pairs.add((u, v))
                matched_buyers.add(u)
                matched_sellers.add(v)

        # interactive output
        if interactive:
            print(f"\n--- Round {rounds} ---")
            print("Matching:", matched_pairs)
            print("Active buyers:", sorted(list(active_buyers), key=lambda x: int(x)))
            print("Inactive buyers:", sorted(list(inactive_buyers), key=lambda x: int(x)))
            prices_str = ", ".join(f"{s}:{G.nodes[s]['price']}" for s in sorted(sellers, key=lambda x: int(x)))
            print("[Prices] " + prices_str)

        # Check whether all active buyers are matched -> market cleared
        if matched_buyers >= active_buyers and len(active_buyers) == len(matched_buyers):
            if interactive:
                print("[INFO] Market cleared: all active buyers are matched.")
            break

        # Build directed alternating graph for reachability:
        #   add buyer -> seller edges for pref_G edges
        #   add seller -> buyer edges only for matched edges (reverse direction)
        directed = nx.DiGraph()
        directed.add_nodes_from(pref_G.nodes())

        for (u, v) in pref_G.edges():
            # ensure direction from buyer -> seller
            if int(u) >= n and int(v) < n:
                directed.add_edge(u, v)
            elif int(v) >= n and int(u) < n:
                directed.add_edge(v, u)
            else:
                # ignore malformed partition edges
                continue

        # add reverse edges from matched sellers to their matched buyer to allow alternating paths
        for (b, s) in matched_pairs:
            directed.add_edge(s, b)

        # unmatched active buyers (free buyers) are active_buyers \ matched_buyers
        free_active_buyers = active_buyers - matched_buyers

        # BFS/DFS from free active buyers to find reachable set R
        reachable = set()
        stack = list(free_active_buyers)
        while stack:
            node = stack.pop()
            if node in reachable:
                continue
            reachable.add(node)
            for nbr in directed.successors(node):
                if nbr not in reachable:
                    stack.append(nbr)

        # constricted sellers = sellers that are NOT reachable (within sellers set)
        reachable_sellers = {x for x in reachable if x in sellers}
        constricted_sellers = set(sellers) - reachable_sellers

        if interactive:
            print("[Debug] free_active_buyers:", sorted(list(free_active_buyers), key=lambda x: int(x)))
            print("[Debug] reachable:", sorted(list(reachable), key=lambda x: int(x)))
            print("[Debug] constricted_sellers:", sorted(list(constricted_sellers), key=lambda x: int(x)))

        # If no constricted sellers found, fall back to increasing price of unmatched sellers that are connected to active buyers
        if not constricted_sellers:
            # choose sellers that appear in pref_G neighbor set of active buyers but are unmatched
            candidate_sellers = set()
            for b in active_buyers:
                for nbr in pref_G.neighbors(b):
                    if nbr not in matched_sellers:
                        candidate_sellers.add(nbr)
            if candidate_sellers:
                to_increase = candidate_sellers
                if interactive:
                    print("[WARN] No constricted sellers detected. Increasing prices of candidate unmatched sellers:", sorted(list(to_increase), key=lambda x: int(x)))
            else:
                # as a final fallback, increase prices of all unmatched sellers
                to_increase = set(sellers) - matched_sellers
                if not to_increase:
                    # nothing to change; terminate to avoid infinite loop
                    print("[STOP] No sellers to increase and active buyers remain unmatched. Terminating.")
                    break
                if interactive:
                    print("[WARN] No candidate sellers found; increasing prices of all unmatched sellers as final fallback:", sorted(list(to_increase), key=lambda x: int(x)))
        else:
            to_increase = constricted_sellers

        # Increase price for each selected seller by 1.0 (assignment-spec simpler increment)
        for s in to_increase:
            old_price = float(G.nodes[s].get('price', 0.0))
            G.nodes[s]['price'] = old_price + 1.0

        # Optionally plot the current preference graph
        if plot:
            # create a copy of pref_G for plotting so we can show valuations on edges
            tmp = nx.Graph()
            tmp.add_nodes_from(pref_G.nodes(data=True))
            tmp.add_edges_from(pref_G.edges(data=True))
            # also attach valuation values from original G where missing
            for (u, v) in list(tmp.edges()):
                data = tmp.get_edge_data(u, v) or {}
                if 'valuation' not in data:
                    orig = G.get_edge_data(u, v) or G.get_edge_data(v, u)
                    if orig and 'valuation' in orig:
                        tmp[u][v]['valuation'] = orig['valuation']
            plot_graph(tmp, title=f"Preference Graph - Round {rounds}")

    return G

def main():
    parser = argparse.ArgumentParser(description="Market-clearing simulation on bipartite market (GML input).")
    parser.add_argument("gml_file", help="Input GML file describing the market graph.")
    parser.add_argument("--plot", action="store_true", help="Plot the graph and preference graphs each round.")
    parser.add_argument("--interactive", action="store_true", help="Print detailed round-by-round updates.")
    args = parser.parse_args()

    # read graph
    G = read_graph(args.gml_file)

    # basic validation: even number of nodes
    if len(G.nodes()) % 2 != 0:
        print("[ERROR] Graph must contain 2n nodes (even).")
        sys.exit(1)

    # validate valuations exist on edges
    for u, v, data in G.edges(data=True):
        if 'valuation' not in data:
            print(f"[ERROR] Edge ({u},{v}) missing 'valuation' attribute.")
            sys.exit(1)

    # initial plot if requested
    if args.plot:
        plot_graph(G, title="Market Graph")

    # run market-clearing
    final_G = market_clearing(G, interactive=args.interactive, plot=args.plot)

    # final summary
    if args.interactive:
        n = len(final_G.nodes()) // 2
        sellers = [node for node in final_G.nodes() if int(node) < n]
        print("\n[FINAL PRICES]")
        for s in sorted(sellers, key=lambda x: int(x)):
            print(f"Seller {s}: price = {final_G.nodes[s].get('price', 0.0)}")

if __name__ == "__main__":
    main()