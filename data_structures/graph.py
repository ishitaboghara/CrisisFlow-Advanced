# data_structures/graph.py - Graph for route management

import heapq
from collections import defaultdict, deque

class Graph:
    """
    Weighted undirected graph for location routing.
    Supports Dijkstra, BFS, DFS, MST
    """
    
    def __init__(self):
        self.adj = defaultdict(dict)  # adj[u][v] = weight
        self.nodes = set()
        self.edges = []
    
    def add_node(self, node):
        """Add a node (location)"""
        self.nodes.add(node)
        if node not in self.adj:
            self.adj[node] = {}
    
    def add_edge(self, u, v, weight=1):
        """Add undirected weighted edge"""
        try:
            weight = float(weight)
        except:
            weight = 1.0
        
        self.nodes.add(u)
        self.nodes.add(v)
        self.adj[u][v] = weight
        self.adj[v][u] = weight
        self.edges.append((u, v, weight))
    
    def remove_edge(self, u, v):
        """Remove edge between u and v"""
        if u in self.adj and v in self.adj[u]:
            del self.adj[u][v]
            del self.adj[v][u]
            self.edges = [(a, b, w) for a, b, w in self.edges if not ((a == u and b == v) or (a == v and b == u))]
    
    def get_neighbors(self, node):
        """Get all neighbors of a node"""
        return list(self.adj.get(node, {}).keys())
    
    def get_weight(self, u, v):
        """Get weight of edge between u and v"""
        return self.adj.get(u, {}).get(v, float('inf'))
    
    def dijkstra(self, start, end):
        """
        Find shortest path using Dijkstra's algorithm
        Returns: (distance, path)
        """
        if start not in self.nodes or end not in self.nodes:
            return None, None
        
        # Initialize distances
        dist = {node: float('inf') for node in self.nodes}
        dist[start] = 0
        parent = {node: None for node in self.nodes}
        visited = set()
        
        # Min heap: (distance, node)
        pq = [(0, start)]
        
        while pq:
            d, u = heapq.heappop(pq)
            
            if u in visited:
                continue
            
            visited.add(u)
            
            if u == end:
                break
            
            for v, weight in self.adj[u].items():
                new_dist = d + weight
                if new_dist < dist[v]:
                    dist[v] = new_dist
                    parent[v] = u
                    heapq.heappush(pq, (new_dist, v))
        
        # Reconstruct path
        if dist[end] == float('inf'):
            return None, None
        
        path = []
        current = end
        while current:
            path.append(current)
            current = parent[current]
        path.reverse()
        
        return dist[end], path
    
    def bfs(self, start):
        """
        Breadth-First Search traversal
        Returns: list of nodes in BFS order
        """
        if start not in self.nodes:
            return []
        
        visited = {start}
        queue = deque([start])
        result = []
        
        while queue:
            node = queue.popleft()
            result.append(node)
            
            for neighbor in self.adj.get(node, {}):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return result
    
    def dfs(self, start):
        """
        Depth-First Search traversal
        Returns: list of nodes in DFS order
        """
        if start not in self.nodes:
            return []
        
        visited = set()
        result = []
        
        def dfs_helper(node):
            visited.add(node)
            result.append(node)
            
            for neighbor in self.adj.get(node, {}):
                if neighbor not in visited:
                    dfs_helper(neighbor)
        
        dfs_helper(start)
        return result
    
    def find_all_paths(self, start, end, max_length=10):
        """Find all paths between start and end (up to max_length)"""
        if start not in self.nodes or end not in self.nodes:
            return []
        
        paths = []
        
        def dfs_paths(current, target, path, visited):
            if len(path) > max_length:
                return
            
            if current == target:
                paths.append(path[:])
                return
            
            for neighbor in self.adj.get(current, {}):
                if neighbor not in visited:
                    visited.add(neighbor)
                    path.append(neighbor)
                    dfs_paths(neighbor, target, path, visited)
                    path.pop()
                    visited.remove(neighbor)
        
        dfs_paths(start, end, [start], {start})
        return paths
    
    def get_connected_components(self):
        """Find all connected components"""
        visited = set()
        components = []
        
        for node in self.nodes:
            if node not in visited:
                component = self.bfs(node)
                components.append(component)
                visited.update(component)
        
        return components
    
    def is_connected(self):
        """Check if graph is connected"""
        if not self.nodes:
            return True
        
        start = next(iter(self.nodes))
        visited = set(self.bfs(start))
        return len(visited) == len(self.nodes)
    
    def get_stats(self):
        """Get graph statistics"""
        return {
            "nodes": len(self.nodes),
            "edges": len(self.edges),
            "connected": self.is_connected(),
            "components": len(self.get_connected_components())
        }