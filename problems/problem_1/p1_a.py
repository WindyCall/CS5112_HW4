# Problem 1a,b,c
# NOTE: Problem B and C are to be implemented in this file as well

import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout

def plan_city_a(num_data_hubs, num_service_providers, connections, provider_capacities, preliminary_assignment) -> bool:
    """
    Implement Problems 1a, 1b, and 1c:
    - 1a: Create graph with source -> data hubs -> service providers
    - 1b: Extend with service providers -> sink
    - 1c: Create residual graph based on preliminary_assignment

    Args:
        num_data_hubs: Number of data hubs (n)
        num_service_providers: Number of service providers (k)
        connections: Dictionary mapping data hub -> list of service providers
        provider_capacities: List where index i has capacity (0 for hubs, actual capacity for providers)
        preliminary_assignment: Dictionary mapping data hub -> assigned service provider (excludes last hub)

    Returns:
        bool: True if last data hub can be connected, False otherwise
    """

    # Define special node names
    SOURCE = 'source'
    SINK = 'sink'

    # ========== PROBLEM 1a: Source -> Data Hubs -> Service Providers ==========
    print("Problem 1a: Creating graph with source -> data hubs -> service providers")

    # Create directed graph
    G_1a = nx.DiGraph()

    # Add source node
    G_1a.add_node(SOURCE)

    # Add data hub nodes (0 to n-1)
    for hub in range(num_data_hubs):
        G_1a.add_node(hub)
        # Add edge from source to each data hub with capacity 1
        G_1a.add_edge(SOURCE, hub, capacity=1)

    # Add service provider nodes (n to n+k-1)
    for provider in range(num_data_hubs, num_data_hubs + num_service_providers):
        G_1a.add_node(provider)

    # Add edges from data hubs to service providers based on connections
    for hub, providers in connections.items():
        for provider in providers:
            G_1a.add_edge(hub, provider, capacity=1)

    # Visualize Problem 1a
    visualize_graph(G_1a, "Problem 1a: Source -> Data Hubs -> Service Providers",
                    "figures/source_c_r_graph.png", num_data_hubs)

    # ========== PROBLEM 1b: Add Service Providers -> Sink ==========
    print("\nProblem 1b: Extending graph with service providers -> sink")

    # Create a copy of 1a graph
    G_1b = G_1a.copy()

    # Add sink node
    G_1b.add_node(SINK)

    # Add edges from service providers to sink with their capacities
    for provider in range(num_data_hubs, num_data_hubs + num_service_providers):
        capacity = provider_capacities[provider]
        if capacity > 0:  # Only add edge if capacity > 0
            G_1b.add_edge(provider, SINK, capacity=capacity)

    # Visualize Problem 1b
    visualize_graph(G_1b, "Problem 1b: Full Network with Sink",
                    "figures/sink_c_r_graph.png", num_data_hubs)

    # ========== PROBLEM 1c: Create Residual Graph ==========
    print("\nProblem 1c: Creating residual graph based on preliminary assignment")

    # Start with the full network graph
    G_residual = G_1b.copy()

    # Apply the preliminary assignments to create residual graph
    for hub, assigned_provider in preliminary_assignment.items():
        # This hub is already assigned to a provider
        # In the residual graph:
        # 1. Forward edge from source to hub: capacity becomes 0 (flow = 1)
        # 2. Backward edge from hub to source: capacity becomes 1
        if G_residual.has_edge(SOURCE, hub):
            G_residual[SOURCE][hub]['capacity'] = 0
        G_residual.add_edge(hub, SOURCE, capacity=1)

        # 3. Forward edge from hub to assigned provider: capacity becomes 0 (flow = 1)
        # 4. Backward edge from assigned provider to hub: capacity becomes 1
        if G_residual.has_edge(hub, assigned_provider):
            G_residual[hub][assigned_provider]['capacity'] = 0
        G_residual.add_edge(assigned_provider, hub, capacity=1)

        # 5. Forward edge from provider to sink: capacity decreases by 1
        # 6. Backward edge from sink to provider: capacity increases by 1
        if G_residual.has_edge(assigned_provider, SINK):
            G_residual[assigned_provider][SINK]['capacity'] -= 1
        G_residual.add_edge(SINK, assigned_provider, capacity=1)

    # Visualize Problem 1c
    visualize_graph(G_residual, "Problem 1c: Residual Graph",
                    "figures/residual_graph.png", num_data_hubs, show_zero_capacity=True)

    print("\nAll graphs generated successfully!")
    print("- Problem 1a: figures/source_c_r_graph.png")
    print("- Problem 1b: figures/sink_c_r_graph.png")
    print("- Problem 1c: figures/residual_graph.png")

    return True


def visualize_graph(G, title, filename, num_data_hubs, show_zero_capacity=False):
    """
    Visualize a network flow graph with proper layout and labels.

    Args:
        G: NetworkX DiGraph
        title: Title for the plot
        filename: Output filename
        num_data_hubs: Number of data hubs (for coloring)
        show_zero_capacity: Whether to show edges with capacity 0
    """
    import os

    # Create figures directory if it doesn't exist
    os.makedirs('figures', exist_ok=True)

    # Create a copy of the graph for visualization
    G_vis = G.copy()

    # Remove edges with capacity 0 if show_zero_capacity is False
    if not show_zero_capacity:
        edges_to_remove = [(u, v) for u, v, data in G_vis.edges(data=True)
                          if data.get('capacity', 1) == 0]
        G_vis.remove_edges_from(edges_to_remove)

    # Set up the plot
    plt.figure(figsize=(14, 10))

    # Define node positions using hierarchical layout
    pos = get_hierarchical_layout(G_vis, num_data_hubs)

    # Use single color for all nodes
    node_colors = 'lightblue'

    # Draw nodes
    nx.draw_networkx_nodes(G_vis, pos, node_color=node_colors,
                          node_size=800, alpha=0.9)

    # Draw edges with straight lines
    nx.draw_networkx_edges(G_vis, pos, edge_color='gray',
                          arrows=True, arrowsize=20,
                          arrowstyle='->', width=2)

    # Draw labels
    nx.draw_networkx_labels(G_vis, pos, font_size=10, font_weight='bold')

    plt.title(title, fontsize=14, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {filename}")


def get_hierarchical_layout(G, num_data_hubs):
    """
    Create a hierarchical layout for the graph.
    Layers: Source -> Data Hubs -> Service Providers -> Sink
    """
    pos = {}

    # Layer positions
    SOURCE_X = 0
    DATA_HUB_X = 2
    SERVICE_PROVIDER_X = 4
    SINK_X = 6

    # Position source
    if 'source' in G.nodes():
        pos['source'] = (SOURCE_X, 0)

    # Position data hubs
    data_hubs = [n for n in G.nodes() if isinstance(n, int) and n < num_data_hubs]
    for i, hub in enumerate(sorted(data_hubs)):
        y = (i - len(data_hubs)/2) * 1.5
        pos[hub] = (DATA_HUB_X, y)

    # Position service providers
    service_providers = [n for n in G.nodes() if isinstance(n, int) and n >= num_data_hubs]
    for i, provider in enumerate(sorted(service_providers)):
        y = (i - len(service_providers)/2) * 1.5
        pos[provider] = (SERVICE_PROVIDER_X, y)

    # Position sink
    if 'sink' in G.nodes():
        pos['sink'] = (SINK_X, 0)

    return pos


# Test with the provided example
if __name__ == "__main__":
    result = plan_city_a(
        num_data_hubs=5,
        num_service_providers=5,
        connections={0: [5, 7, 8], 1: [5, 8], 2: [7, 8, 9], 3: [5, 6, 8, 9], 4: [5, 6, 7, 8]},
        provider_capacities=[0]*5 + [0, 1, 0, 2, 2],
        preliminary_assignment={0: 8, 1: 8, 2: 9, 3: 9}
    )
