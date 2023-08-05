# SatClave
A small library implementing graph functions, and other in future

### Installation
```
pip install satclave
```

## Get started
Here are the implementations of SatClave.

### Graph
```Python
from satclave import Graph
# Create a new graph
graph = Graph()

# Add some vertices
graph.add_vertex(1)
graph.add_vertex(2)
graph.add_vertex(3)
graph.add_vertex(4)

# Add some edges
graph.add_edge(1, 2)
graph.add_edge(2, 3)
graph.add_edge(3, 4)
graph.add_edge(4, 1)

# Print the graph
print("Vertices:", graph.vertices)
print("Edges:", graph.edges)

# Test graph connectivity
print("Is the graph connected?", graph.is_connected())

# Test DFS and BFS
print("DFS:", graph.depth_first_search(1))
print("BFS:", graph.breadth_first_search(1))

# Test shortest path
print("Shortest path from 1 to 3:", graph.get_shortest_path(1, 3))

# Test connected components
print("Connected components:", graph.get_connected_components())

# Test vertex removal
graph.remove_vertex(2)
print("Vertices after removal:", graph.vertices)
print("Edges after removal:", graph.edges)

# Test cycle detection
print("Does the graph contain a cycle?", graph.is_cyclic())
```

### Vector
```python
from vector import Vector

# create two vectors
v1 = Vector([1, 2, 3])
v2 = Vector([4, 5, 6])

# test vector addition and subtraction
v3 = v1 + v2
v4 = v2 - v1
print(f"v1 + v2 = {v3}")  
print(f"v2 - v1 = {v4}") 

# test dot product and cross product
dot_product = v1.dot(v2)
cross_product = v1.cross(v2)
print(f"v1 . v2 = {dot_product}")  
print(f"v1 x v2 = {cross_product}") 

# test vector magnitude and normalization
magnitude_v1 = v1.magnitude()
normalized_v1 = v1.normalize()
print(f"magnitude of v1 = {magnitude_v1}")  
print(f"normalized v1 = {normalized_v1}")  
```
