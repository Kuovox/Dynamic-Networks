# Names: Khoa Vu (030063200) & Mya Barragan (029948137)
# Course: CECS 427 (Sec. 02)
# Professor: Oscar Morales-Ponce
# Date: 11/18/2025

"""
Citation(s):
1) Machine Learning Mastery (web crawling) Brownlee, J. (n.d.). How to Use Web Crawling in Python. Machine Learning Mastery. Retrieved from https://machinelearningmastery.com/web-crawling-in-python
2) ZenRows (Python web crawler tutorial) ZenRows. (n.d.). How to Build a Web Crawler in Python (Step-by-Step Tutorial). ZenRows Blog. Retrieved from https://www.zenrows.com/blog/web-crawler-python
3) GeeksforGeeks (PageRank implementation) GeeksforGeeks. (n.d.). PageRank Algorithm Implementation in Python. GeeksforGeeks. Retrieved from https://www.geeksforgeeks.org/python/page-rank-algorithm-implementation
"""

import argparse
import collections
import os
import sys
import time
import requests
import networkx as nx
import matplotlib.pyplot as plt

from typing import List, Set, Optional
from urllib.parse import urljoin, urlparse, urldefrag
from urllib import robotparser
from bs4 import BeautifulSoup


def load_gml(path: str): # Load a graph from a GML file
    if not os.path.exists(path):    # Check if the file exists before attempting to load it
        fail(f"File not found: {path}") 
    try: 
        G = nx.read_gml(path)   # Attempt to read the GML file using NetworkX's read_gml function
    except Exception as e:  # Catch any exceptions that occur during the loading process and print an error message
        fail(f"Could not load GML: {e}")    
    if isinstance(G, nx.MultiDiGraph):  # If the loaded graph is a MultiDiGraph, convert it to a DiGraph by collapsing multiple edges into single edges
        return nx.DiGraph(G)
    if isinstance(G, nx.Graph): # If the loaded graph is an undirected Graph, convert it to a DiGraph by treating each undirected edge as two directed edges
        return nx.DiGraph(G)
    return G

# Save a graph to a GML file
def save_gml(G: nx.DiGraph, path: str): 
    try:
        nx.write_gml(G, path)   # Attempt to write the graph to a GML file using NetworkX's write_gml function
    except Exception as e:  # Catch any exceptions that occur during the saving process and print an error message
        fail(f"Failed to write GML: {e}")

# Crawler function to build a directed graph from a given domain and seed URLs, with limits on the number of nodes and edges
def run_crawler(limit: int, domain: str, seeds: List[str], timeout: float = 8.0, pause: float = 0.25):
    ua = "Crawler-Agent/1.1 (+student-project)" # User-Agent string to identify the crawler when making HTTP requests
    # robots_url = urljoin(domain, "/robots.txt") # URL for the robots.txt file of the domain, which specifies the crawling rules for web crawlers
    # rp = load_robots(robots_url)
    graph = nx.DiGraph()
    queue = collections.deque()
    start_nodes = []
    
    for s in seeds:
        fixed = canonicalize(domain, s) # Canonicalize the seed URL to ensure it is in a standard format
        if fixed and same_host(fixed, domain):  # Check if the canonicalized URL is valid and belongs to the same host as the domain
            start_nodes.append(fixed)

    if not start_nodes: # If no valid in-domain seed URLs are found, print an error message and exit the program
        fail("No valid in-domain seeds found in crawler.txt")

    for url in start_nodes: # Add the valid seed URLs to the crawling queue
        queue.append(url)
    
    # Set to keep track of visited URLs to avoid processing the same URL multiple times
    visited = set()
    session = requests.Session()
    session.headers.update({"User-Agent": ua})

    while queue and len(graph) < limit: # Continue crawling until the queue is empty or the graph reaches the specified node limit
        url = queue.popleft()
        if url in visited:  # Skip URLs that have already been visited to avoid processing the same URL multiple times
            continue
        visited.add(url)

        # ignore robots.txt rules to ensure we can crawl the sample domain
        # if not rp.can_fetch(ua, url):  # Check if the crawler is allowed to access the URL according to the rules specified in the robots.txt file. If not, skip the URL.
            # continue

        # Make an HTTP GET request to the URL with a specified timeout and allow redirects. If the request fails, skip the URL.
        try:
            resp = session.get(url, timeout=timeout, allow_redirects=True)
        except requests.RequestException:
            continue

        if not is_html(resp): # Check if the response is an HTML page by looking at the Content-Type header. If it is not HTML, skip the URL.
            continue

        graph.add_node(url) # Add the URL as a node in the graph

        try:
            links = pull_links(resp.url, resp.text) # Extract links from the HTML content of the page using the pull_links function, which returns a set of canonicalized URLs found in the page
        except Exception:   # If there is an error while parsing the HTML or extracting links, skip the URL
            links = set()

        MAX_OUT_PER_PAGE = 20
        out = set()
        for link in links:  # Filter the extracted links to include only those that belong to the same host as the domain and do not have certain file extensions (e.g., images, videos, archives). This helps to focus the crawler on relevant pages and avoid unnecessary crawling of non-HTML resources.
            if not same_host(link, domain):
                continue
            ext = link.lower()
            if ext.endswith((".png", ".jpg", ".jpeg", ".gif", ".pdf",
                             ".mp4", ".mp3", ".zip", ".gz", ".svg",
                             ".tar")):
                continue
            out.add(link)

        for link in list(out)[:MAX_OUT_PER_PAGE]: # For each valid link extracted from the page, add an edge from the current URL to the linked URL in the graph. If the linked URL is not already in the graph and the graph has reached the specified node limit, skip adding the edge and do not enqueue the linked URL for crawling.
            if link not in graph and len(graph) >= limit:
                continue

            graph.add_edge(url, link)   # Add a directed edge from the current URL to the linked URL in the graph

            if link not in visited and link not in queue and len(graph) < limit:    # If the linked URL has not been visited and is not already in the crawling queue, and the graph has not reached the node limit, add the linked URL to the crawling queue for further processing.
                queue.append(link)

        time.sleep(pause)   # Pause between requests to avoid overwhelming the server and to be respectful of the site's resources

    return graph    # Return the constructed directed graph representing the crawled web pages and their links

def load_crawler_options(path: str):    # Load crawler options from a specified file path, which should contain the maximum number of nodes, the domain to crawl, and the seed URLs. The function checks for the existence of the file, reads its contents, and validates the format of the data. It returns the maximum number of nodes, the domain, and a list of seed URLs.
    if not os.path.exists(path):    # Check if the specified file exists. If it does not, print an error message and exit the program.
        fail(f"Crawler file missing: {path}")

    with open(path, "r", encoding="utf-8") as f:    # Read the contents of the file and strip whitespace from each line. Only non-empty lines are kept in the list.
        lines = [ln.strip() for ln in f if ln.strip()]

    if len(lines) < 2:  # Check if the file contains at least two lines (the maximum number of nodes and the domain). If not, print an error message and exit the program.
        fail("crawler.txt must contain: N, domain, and seed URLs")

    try:    # Attempt to convert the first line of the file to an integer, which represents the maximum number of nodes to crawl. If this conversion fails, print an error message and exit the program.
        n = int(lines[0])
    except ValueError:  # If the first line cannot be converted to an integer, print an error message indicating that the first line must be an integer and exit the program.
        fail("The first line of crawler.txt must be an integer (max nodes)")

    # The second line of the file is expected to contain the domain to crawl. The function removes any trailing slashes from the domain and checks if it includes a valid URL scheme (e.g., http:// or https://). If the domain does not include a valid scheme, an error message is printed and the program exits.
    domain = lines[1].rstrip("/")
    seeds = [s.rstrip("/") for s in lines[2:]] or [domain]

    if not urlparse(domain).scheme: # Check if the domain includes a valid URL scheme. If not, print an error message and exit the program.
        fail("Domain must include a scheme, e.g., https://example.com")

    return n, domain, seeds # Return the maximum number of nodes, the domain, and the list of seed URLs extracted from the file. The maximum number of nodes is returned as an integer, while the domain and seed URLs are returned as strings.

def save_loglog(G: nx.DiGraph, out_path="loglog_plot.png"):   # Generate a log-log plot of the degree distribution of the graph G and save it to the specified output path. The function checks if the graph is empty or if all degrees are zero before attempting to generate the plot. If the graph is empty or all degrees are zero, it prints an appropriate message and does not generate the plot.
    if len(G) == 0: # Check if the graph is empty. If it is, print a message indicating that the graph is empty and no log-log plot will be generated, then return from the function.
        print("Graph is empty. No log-log plot generated.")
        return

    degrees = [d for _, d in G.degree() if d > 0]   # Create a list of degrees for all nodes in the graph, filtering out nodes with a degree of zero. This is done to avoid issues with logarithmic scaling when generating the log-log plot.
    if not degrees: # Check if the list of degrees is empty (i.e., all nodes have a degree of zero). If it is empty, print a message indicating that all degrees are zero and no log-log plot will be generated, then return from the function.
        print("All degrees = 0. Skipping log-log plot.")
        return

    # Use the Counter class from the collections module to count the frequency of each degree in the list of degrees. The resulting frequency distribution is stored in the variable freq, which is a dictionary where the keys are the unique degrees and the values are the counts of nodes with those degrees.
    freq = collections.Counter(degrees)
    xs = sorted(freq)
    ys = [freq[k] for k in xs]

    # Generate a log-log plot of the degree distribution using Matplotlib. The x-axis represents the degree (on a logarithmic scale), and the y-axis represents the node count (also on a logarithmic scale). The plot is saved to the specified output path with a resolution of 180 DPI.
    plt.figure(figsize=(7, 5))
    plt.loglog(xs, ys)
    plt.xlabel("Degree (log)")
    plt.ylabel("Node Count (log)")
    plt.title("Degree Distribution (loglog)")
    plt.tight_layout()
    plt.savefig(out_path, dpi=180)

# Compute the PageRank scores for the nodes in the graph G and save the results to a specified output file. The function checks if the graph is empty before attempting to compute PageRank. If the graph is empty, it prints an appropriate message and does not attempt to compute PageRank.
def compute_pagerank(G: nx.DiGraph, out_file: str, damping=0.85):
    if len(G) == 0: # Check if the graph is empty. If it is, print a message indicating that the graph is empty and PageRank cannot be computed, then return from the function.
        fail("Cannot compute PageRank on an empty graph.")
    try:
        pr = nx.pagerank(G, alpha=damping, max_iter=100)    # Attempt to compute the PageRank scores for the nodes in the graph using NetworkX's pagerank function. The damping factor is set to 0.85, and the maximum number of iterations is set to 100. If the PageRank computation fails to converge within the specified number of iterations, an exception is raised.
    except nx.PowerIterationFailedConvergence:  # If the PageRank computation fails to converge, print an error message indicating that PageRank failed to converge and exit the program.
        fail("PageRank failed to converge.")
    # Sort the PageRank scores in descending order, and in case of ties, sort by URL in ascending order. The sorted results are stored in the variable ranking, which is a list of tuples where each tuple contains a URL and its corresponding PageRank score.
    ranking = sorted(pr.items(), key=lambda x: (-x[1], x[0]))
    with open(out_file, "w", encoding="utf-8") as f:    # Open the specified output file for writing. The file is opened in write mode with UTF-8 encoding. If the file cannot be opened for writing, an exception will be raised.
        for url, val in ranking:    # Iterate through the sorted PageRank scores and write each URL and its corresponding PageRank score to the output file. The PageRank score is formatted to 12 decimal places, and the URL is written on a new line. If there is an error while writing to the file, an exception will be raised.
            f.write(f"{val:.12f}\t{url}\n")

# Generate a visualization of a subgraph of the graph G, containing a specified number of nodes selected based on a given strategy (either "first" or "degree"). The visualization is saved to the specified output file. If the graph is empty, a message is printed indicating that no visualization will be created.
def plot_subgraph(G: nx.DiGraph, out_file="graph_plot.png",
                  n=11, strategy="first"):
    if G.number_of_nodes() == 0:    # Check if the graph is empty. If it is, print a message indicating that the graph is empty and no visualization will be created, then return from the function.
        print("Empty graph. No visualization created.")
        return

    if strategy == "degree":    # If the strategy for selecting nodes is "degree", sort the nodes in the graph by their degree in descending order and select the top n nodes. The degree of each node is obtained using the degree() method of the graph, which returns a dictionary where the keys are the node identifiers and the values are their corresponding degrees.
        degs = dict(G.degree())
        chosen = [node for node, _ in sorted(degs.items(),
                                             key=lambda x: -x[1])[:n]]
    else:   # If the strategy for selecting nodes is "first", simply select the first n nodes from the graph's node list. The nodes are returned in the order they were added to the graph.
        chosen = list(G.nodes())[:n]

    # Create a subgraph of G containing only the selected nodes and their edges. The subgraph is created using the subgraph() method of the graph, which returns a new graph containing only the specified nodes and the edges between them.
    H = G.subgraph(chosen).copy()
    plt.figure(figsize=(11, 8))
    pos = nx.spring_layout(H, seed=12, k=0.45, iterations=200)
    nx.draw_networkx_nodes(H, pos, node_size=150, alpha=0.9)
    nx.draw_networkx_edges(H, pos, arrows=True, arrowsize=10)
    nx.draw_networkx_labels(H, pos, font_size=7)
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(out_file, dpi=200)
    plt.close()
    print(f"Graph visualization saved to {out_file}")

# Helper function to print an error message and exit the program with a specified exit code. The error message is printed to standard error (stderr) to indicate that it is an error message, and the program exits with the provided exit code (default is 2).
def fail(msg: str, exit_code: int = 2):
    print(f"[Error] {msg}", file=sys.stderr)
    sys.exit(exit_code)

# Helper function to check if the response from an HTTP request is an HTML page. It checks the status code of the response and the Content-Type header to determine if the response is an HTML page. If the status code is 200 and the Content-Type header contains "text/html", it returns True; otherwise, it returns False.
def is_html(resp: requests.Response) -> bool:
    ctype = resp.headers.get("Content-Type", "").lower()
    return (resp.status_code == 200) and ("text/html" in ctype)

# Helper function to canonicalize a URL by resolving it against a base URL, removing any fragment identifiers, and ensuring that it has a valid scheme (e.g., http or https). If the URL is invalid or cannot be canonicalized, the function returns None.
def canonicalize(base_url: str, link: str) -> Optional[str]:
    if not link:
        return None
    try:    # Use urljoin to resolve the link against the base URL, and urldefrag to remove any fragment identifiers from the resulting URL. The urlparse function is used to parse the URL and check if it has a valid scheme (http or https). If the URL is valid, it is returned in a canonicalized form; otherwise, None is returned.
        absolute = urljoin(base_url, link)
        absolute, _ = urldefrag(absolute)
        parsed = urlparse(absolute)
        if not parsed.scheme.startswith("http"):
            return None

        host = parsed.hostname or ""
        if parsed.port: # If the URL includes a port number, check if it is the default port for the scheme (80 for http and 443 for https). If it is not the default port, include the port number in the host string; otherwise, just use the hostname.
            default = (
                (parsed.scheme == "http" and parsed.port == 80) or
                (parsed.scheme == "https" and parsed.port == 443)
            )
            if not default: # If the port number is not the default for the scheme, include it in the host string. Otherwise, just use the hostname.
                host = f"{host}:{parsed.port}"
        path = parsed.path or "/"
        q = f"?{parsed.query}" if parsed.query else ""
        return f"{parsed.scheme}://{host}{path}{q}"
    except Exception:
        return None

# Helper function to check if a given URL belongs to the same host as a specified domain root. It compares the hostname and scheme of the URL with those of the domain root. If both the hostname and scheme match, it returns True; otherwise, it returns False.
def same_host(url: str, domain_root: str) -> bool:
    u = urlparse(url)
    r = urlparse(domain_root)
    return (u.hostname == r.hostname) and (u.scheme == r.scheme)

# Helper function to extract and canonicalize links from the HTML content of a page. It uses BeautifulSoup to parse the HTML and find all anchor tags with href attributes. Each link is canonicalized using the canonicalize function, and valid links are collected in a set and returned.
def pull_links(page_url: str, html: str) -> Set[str]:
    soup = BeautifulSoup(html, "html.parser")
    found = set()

    for tag in soup.find_all("a", href=True):   # Iterate through all anchor tags in the HTML that have an href attribute. For each tag, the href value is canonicalized using the canonicalize function, and if the resulting URL is valid (not None), it is added to the set of found links.
        cleaned = canonicalize(page_url, tag["href"])
        if cleaned:
            found.add(cleaned)
    return found

def load_robots(robots_url: str) -> robotparser.RobotFileParser:
    rp = robotparser.RobotFileParser()
    rp.set_url(robots_url)
    try:
        rp.read()
    except Exception:
        # If robots.txt cannot be read, allow all by default
        pass
    return rp

# Main function to parse command-line arguments, crawl or load a web graph, compute PageRank, and generate plots and visualizations based on the provided options.
def parser():
    ap = argparse.ArgumentParser(
        description="Crawl or load a web graph, compute PageRank, and plot degree statistics."
    )
    # Add command-line arguments for crawling, loading input graph, generating log-log plot, saving crawled graph, outputting PageRank values, and plotting the graph visualization.
    ap.add_argument("--crawler", type=str,
                    help="Path to crawler.txt to perform crawling")
    ap.add_argument("--input", type=str,
                    help="Load graph from an existing GML file instead of crawling")
    ap.add_argument("--loglogplot", action="store_true",
                    help="Generate a log-log plot of degree distribution")
    ap.add_argument("--crawler_graph", type=str,
                    help="Save the crawled graph to this GML file")
    ap.add_argument("--pagerank_values", type=str,
                    help="Output file for PageRank scores")
    ap.add_argument("--plot", nargs="?", const="graph_plot.png",
                    help="Generate induced subgraph visualization")
    ap.add_argument("--plot_pick", choices=["first", "degree"], default="first",
                    help="Method for selecting nodes for visualization")
    return ap

# Main function to execute the program based on the provided command-line arguments. It handles crawling or loading the graph, generating plots, computing PageRank, and visualizing the graph as specified by the user.
def main():
    args = parser().parse_args()
    # Crawl or load input graph
    if args.crawler:
        max_nodes, domain, seeds = load_crawler_options(args.crawler)
        # Use the limit specified in crawler.txt
        node_cap = max_nodes
        print(f"Crawling domain {domain} with limit {node_cap} nodes ...")
        G = run_crawler(node_cap, domain, seeds)
        print(f"Final graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
        print("Done.")

        if args.crawler_graph:  # If the user has specified a path to save the crawled graph, save the graph to a GML file using the save_gml function. The graph is saved to the specified path, and a message is printed confirming that the graph has been saved.
            save_gml(G, args.crawler_graph)
    else:
        if not args.input:  # If the user has not specified either a crawler file or an input graph file, print an error message and exit the program.
            fail("Must specify either --crawler or --input")
        print(f"Loading graph from {args.input} ...")
        G = load_gml(args.input)
        print(f"Loaded graph: number of nodes = {G.number_of_nodes()}  number of edges = {G.number_of_edges()}")

    # Generate log-log plot of degree distribution if requested by the user. If the graph is empty or all degrees are zero, a message is printed indicating that the log-log plot will not be generated.
    if args.loglogplot:
        save_loglog(G)
    # Compute PageRank scores and save to file if requested by the user. If the graph is empty, a message is printed indicating that PageRank cannot be computed.
    if args.pagerank_values:
        compute_pagerank(G, args.pagerank_values)
    else:
        print("Note: PageRank output not requested")
    # Generate a visualization of the graph if requested by the user. If the graph is empty, a message is printed indicating that no visualization will be created.
    if args.plot:
        plot_subgraph(G, out_file=args.plot,
                      n=11, strategy=args.plot_pick)

if __name__ == "__main__":
    main()