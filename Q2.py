import networkx as nx
import matplotlib.pyplot as plt
G = nx.Graph()
with open("global-cities.dat", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        parts = line.split('|')
        if len(parts) >= 3:
            node_id = parts[1].strip()
            city_name = parts[2].strip()
            G.add_node(node_id, name=city_name)
with open("global-net.dat", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) == 2:
            node1, node2 = parts[0].strip(), parts[1].strip()
            G.add_edge(node1, node2)

# Q1
print("Total number:", G.number_of_nodes())
print("Total edge number:", G.number_of_edges())

# Q2
components = list(nx.connected_components(G))
print("number of onnected components:", len(components))

largest_component_nodes = max(components, key=len)
G_largest = G.subgraph(largest_component_nodes).copy()
print("The number of nodes in the largest connected component:", G_largest.number_of_nodes())
print("The number of edges in the largest connected component:", G_largest.number_of_edges())

#Q3
# Get the degree of all nodes in the G_largest
degree_list = list(G_largest.degree())
# Sort by degree from large to small
degree_list_sorted = sorted(degree_list, key=lambda x: x[1], reverse=True)
top_10 = degree_list_sorted[:10]
print("Top 10 nodes (in degree from high to low):")
for i, (node_id, deg) in enumerate(top_10, start=1):
    city_name = G_largest.nodes[node_id].get('name', 'Unknown')
    print(f"{i}. {city_name} - degree: {deg}")

#Q4
degrees = [deg for node, deg in G.degree()]
total_nodes = len(degrees)
degree_counts = {}
for d in degrees:
    if d > 0:
        degree_counts[d] = degree_counts.get(d, 0) + 1
x_values = sorted(degree_counts.keys())
y_values = [degree_counts[x] / total_nodes for x in x_values]
plt.figure(figsize=(8, 6))
plt.plot(x_values, y_values, 'ro-', markersize=5)
plt.xlabel('Degree')
plt.ylabel('Fraction of Nodes')
plt.title('Degree Distribution')
plt.xlim(min(x_values), max(x_values))
plt.grid(True)
plt.show()

plt.figure(figsize=(8, 6))
plt.plot(x_values, y_values, 'ro-', markersize=5)
plt.xscale('log', base=10)
plt.yscale('log', base=10)
plt.xlabel('Degree')
plt.ylabel('Fraction of Nodes')
plt.title('Degree Distribution (Log-Log Scale)')
plt.xlim(min(x_values), max(x_values))
plt.grid(True, which="both", ls="--")
plt.show()

# Q5:

diameter = nx.diameter(G_largest)
print("The (unweighted) diameter of the giant component is：", diameter)
peripheral_nodes = nx.periphery(G_largest)
print("peripheral node candidate:", peripheral_nodes)
source = peripheral_nodes[0]
lengths = nx.single_source_shortest_path_length(G_largest, source)
target = None
for node, d in lengths.items():
    if d == diameter:
        target = node
        break
if target is None:
    print("No node with a distance equal to the diameter from the starting point was found")
else:
    longest_path_nodes = nx.shortest_path(G_largest, source=source, target=target)
    longest_path_names = [G_largest.nodes[node]['name'] for node in longest_path_nodes]
    print("The longest (unweighted) shortest path is:")
    print(" -> ".join(longest_path_names))


# Q6:
name_to_node = {data['name']: node for node, data in G.nodes(data=True)}
source_node = name_to_node["Canberra"]
target_node = name_to_node["Cape Town"]
shortest_path_nodes = nx.shortest_path(G, source=source_node, target=target_node)
shortest_path_names = [G.nodes[node]['name'] for node in shortest_path_nodes]
num_flights = len(shortest_path_nodes) - 1
print("Minimum number of flights required:", num_flights)
print("City/Airport Name:")
print(" -> ".join(shortest_path_names))

#Q7
betweenness = nx.betweenness_centrality(G)
top10 = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)[:10]
print("Top 10 cities/airports by betweenness centrality:")
for node, centrality in top10:
    city_name = G.nodes[node].get('name', 'Unknown')
    print(f"{city_name}: {centrality:.4f}")
