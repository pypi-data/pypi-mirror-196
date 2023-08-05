class Graph:
    """
    A class for representing graphs and performing graph theory operations.

    Attributes:
        vertices (set): A set of all vertices in the graph.
        edges (dict): A dictionary mapping vertices to their neighbors.

    Methods:
        add_vertex(self, vertex: int) -> None:
            Adds a vertex to the graph.
        add_edge(self, vertex1: int, vertex2: int) -> None:
            Adds an undirected edge between two vertices in the graph.
        remove_edge(self, vertex1: int, vertex2: int) -> None:
            Removes an undirected edge between two vertices in the graph.
        remove_vertex(self, vertex: int) -> None:
            Removes a vertex and all its associated edges from the graph.
        is_connected(self) -> bool:
            Checks if the graph is connected.
        depth_first_search(self, start_vertex: int) -> list:
            Performs a depth-first search on the graph starting from the given vertex.
        breadth_first_search(self, start_vertex: int) -> list:
            Performs a breadth-first search on the graph starting from the given vertex.
        get_shortest_path(self, start_vertex: int, end_vertex: int) -> list:
            Finds the shortest path between two vertices using Dijkstra's algorithm.
        get_connected_components(self) -> list:
            Finds all the connected components of the graph.
        is_cyclic(self) -> bool:
            Checks if the graph contains a cycle.
    """
    
    def __init__(self):
        self.vertices = set()
        self.edges = {}
        
    def add_vertex(self, vertex: int) -> None:
        """
        Adds a vertex to the graph.
        
        Args:
            vertex (int): The vertex to add.
            
        Returns:
            None.
        """
        self.vertices.add(vertex)
        self.edges[vertex] = set()
        
    def add_edge(self, vertex1: int, vertex2: int) -> None:
        """
        Adds an undirected edge between two vertices in the graph.
        
        Args:
            vertex1 (int): The first vertex.
            vertex2 (int): The second vertex.
            
        Returns:
            None.
        """
        self.edges[vertex1].add(vertex2)
        self.edges[vertex2].add(vertex1)
        
    def remove_edge(self, vertex1: int, vertex2: int) -> None:
        """
        Removes an undirected edge between two vertices in the graph.
        
        Args:
            vertex1 (int): The first vertex.
            vertex2 (int): The second vertex.
            
        Returns:
            None.
        """
        self.edges[vertex1].remove(vertex2)
        self.edges[vertex2].remove(vertex1)
        
    def remove_vertex(self, vertex: int) -> None:
        """
        Removes a vertex and all its associated edges from the graph.
        
        Args:
            vertex (int): The vertex to remove.
            
        Returns:
            None.
        """
        for neighbor in self.edges[vertex]:
            self.edges[neighbor].remove(vertex)
        del self.edges[vertex]
        self.vertices.remove(vertex)
        
    def is_connected(self) -> bool:
        """
        Checks if the graph is connected.
        
        Returns:
            bool: True if the graph is connected, False otherwise.
        """
        visited = set()
        stack = [next(iter(self.vertices))]
        while stack:
            vertex = stack.pop()
            visited.add(vertex)
            for neighbor in self.edges[vertex]:
                if neighbor not in visited:
                    stack.append(neighbor)
        return visited == self.vertices
        
    def depth_first_search(self, start_vertex: int) -> list:
        """
        Performs a depth-first search on the graph starting from the given vertex.
        Args:
            start_vertex (int): The vertex to start the search from.
        
        Returns:
            list: A list of vertices visited in the order they were visited.
        """
        visited = set()
        stack = [start_vertex]
        while stack:
            vertex = stack.pop()
            if vertex not in visited:
                visited.add(vertex)
                stack.extend(self.edges[vertex] - visited)
        return list(visited)

    def breadth_first_search(self, start_vertex: int) -> list:
        """
        Performs a breadth-first search on the graph starting from the given vertex.
    
        Args:
            start_vertex (int): The vertex to start the search from.
        
        Returns:
            list: A list of vertices visited in the order they were visited.
        """
        visited = set()
        queue = [start_vertex]
        while queue:
            vertex = queue.pop(0)
            if vertex not in visited:
                visited.add(vertex)
                queue.extend(self.edges[vertex] - visited)
        return list(visited)

    def get_shortest_path(self, start_vertex: int, end_vertex: int) -> list:
        """
        Finds the shortest path between two vertices using Dijkstra's algorithm.
    
        Args:
            start_vertex (int): The starting vertex.
            end_vertex (int): The ending vertex.
        
        Returns:
            list: A list of vertices in the shortest path.
        """
        distances = {vertex: float('inf') for vertex in self.vertices}
        distances[start_vertex] = 0
        queue = list(self.vertices)
        while queue:
            current_vertex = min(queue, key=lambda vertex: distances[vertex])
            queue.remove(current_vertex)
            if distances[current_vertex] == float('inf'):
                break
            for neighbor in self.edges[current_vertex]:
                alt_route = distances[current_vertex] + 1
                if alt_route < distances[neighbor]:
                    distances[neighbor] = alt_route
        path = []
        current_vertex = end_vertex
        while current_vertex != start_vertex:
            path.append(current_vertex)
            for neighbor in self.edges[current_vertex]:
                if distances[neighbor] == distances[current_vertex] - 1:
                    current_vertex = neighbor
                    break
        path.append(start_vertex)
        path.reverse()
        return path

    def get_connected_components(self) -> list:
        """
        Finds all the connected components of the graph.
    
        Returns:
            list: A list of sets, where each set contains the vertices of a connected component.
        """
        visited = set()
        connected_components = []
        for vertex in self.vertices:
            if vertex not in visited:
                component = set(self.depth_first_search(vertex))
                visited |= component
                connected_components.append(component)
        return connected_components

    def is_cyclic(self) -> bool:
        """
        Checks if the graph contains a cycle.
    
        Returns:
            bool: True if the graph contains a cycle, False otherwise.
        """
        visited = set()
        stack = [(next(iter(self.vertices)), None)]
        while stack:
            vertex, parent = stack.pop()
            visited.add(vertex)
            for neighbor in self.edges[vertex]:
                if neighbor not in visited:
                    stack.append((neighbor, vertex))
                elif neighbor != parent:
                    return True  
        return False
