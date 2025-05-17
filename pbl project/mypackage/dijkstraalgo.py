import heapq
import networkx as nx

def custom_dijkstra(G, start_node, end_node):
    # Initialize distances and previous node tracking
    dist = {node: float('inf') for node in G.nodes}
    prev = {node: None for node in G.nodes}
    dist[start_node] = 0
    
    # Priority queue for node exploration
    queue = [(0, start_node)]
    
    while queue:
        current_dist, current_node = heapq.heappop(queue)
        
        # Early exit if we reached the destination
        if current_node == end_node:
            break
        
        for neighbor in G.neighbors(current_node):
            edge_data = G.get_edge_data(current_node, neighbor)
            if edge_data:
                weight = edge_data.get('length', 1)  # Default weight if unspecified
                
                # Relaxation step
                if dist[current_node] + weight < dist[neighbor]:
                    dist[neighbor] = dist[current_node] + weight
                    prev[neighbor] = current_node
                    heapq.heappush(queue, (dist[neighbor], neighbor))
                    
    # Build shortest path from end_node to start_node
    path = []
    node = end_node
    while node:
        path.append(node)
        node = prev[node]
    
    if path[-1] != start_node:  # If end_node wasn't reachable, return an empty list
        return []
    
    path.reverse()
    return path