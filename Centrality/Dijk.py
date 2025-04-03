from mpi4py import MPI
import numpy as np
import networkx as nx
from heapq import heappop, heappush
from collections import defaultdict

def dijkstra(graph, source):
    """Compute shortest paths from a source node using Dijkstra's algorithm."""
    dist = {node: float('inf') for node in graph.nodes}
    dist[source] = 0
    priority_queue = [(0, source)]

    while priority_queue:
        current_dist, current_node = heappop(priority_queue)
        if current_dist > dist[current_node]:
            continue
        for neighbor in graph.neighbors(current_node):
            distance = current_dist + 1  # All edges have weight 1
            if distance < dist[neighbor]:
                dist[neighbor] = distance
                heappush(priority_queue, (distance, neighbor))
    return dist

def compute_closeness_centrality(graph, nodes):
        centrality = {}
    num_nodes = len(graph.nodes)
    for node in nodes:
        shortest_paths = dijkstra(graph, node)
        total_distance = sum(shortest_paths.values())
        if total_distance > 0:
            centrality[node] = (num_nodes - 1) / total_distance
        else:
            centrality[node] = 0.0
    return centrality

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Processor 0: Load graph and distribute nodes
    if rank == 0:
        print("Loading graph...")
        graph = nx.read_edgelist("facebook_combined.txt", nodetype=int)
        nodes = list(graph.nodes)
        node_chunks = np.array_split(nodes, size)
    else:
        graph = None
        node_chunks = None

    # Broadcast the graph to all processors
    graph = comm.bcast(graph, root=0)
    local_nodes = comm.scatter(node_chunks, root=0)

    # Compute closeness centrality for local nodes
    local_centrality = compute_closeness_centrality(graph, local_nodes)

    # Gather results at processor 0
    all_centralities = comm.gather(local_centrality, root=0)

    if rank == 0:
        # Combine centralities from all processors
        final_centrality = {}
        for centrality in all_centralities:
            final_centrality.update(centrality)


        with open("output.txt", "w") as f:
            for node, centrality in final_centrality.items():
                f.write(f"Node {node}: Closeness Centrality = {centrality}\n")

        # Print top 5 nodes and average centrality
        top_nodes = sorted(final_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
        print("Top 5 nodes with highest closeness centrality:")
        for node, centrality in top_nodes:
            print(f"Node {node}: {centrality}")

        average_centrality = np.mean(list(final_centrality.values()))
        print(f"Average Closeness Centrality: {average_centrality}")

if __name__ == "__main__":
    main()
