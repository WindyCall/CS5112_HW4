# Problem 1a,b,c
# NOTE: Problem B and C are to be implemented in this file as well

import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout

def plan_city_a(num_data_hubs, num_service_providers, connections, provider_capacities, preliminary_assignment) -> bool:
    SOURCE = 'source'
    SINK = 'sink'

    G_1a = nx.DiGraph()

    G_1a.add_node(SOURCE)

    for hub in range(num_data_hubs):
        G_1a.add_node(hub)
        G_1a.add_edge(SOURCE, hub, capacity=1)

    for provider in range(num_data_hubs, num_data_hubs + num_service_providers):
        G_1a.add_node(provider)

    for hub, providers in connections.items():
        for provider in providers:
            G_1a.add_edge(hub, provider, capacity=1)

    G_1a.add_node(SINK)

    visualize_graph(G_1a, "Problem 1a: Source -> Data Hubs -> Service Providers",
                    "figures/source_c_r_graph.png", num_data_hubs)


    G_1b = G_1a.copy()

    G_1b.add_node(SINK)

    for provider in range(num_data_hubs, num_data_hubs + num_service_providers):
        capacity = provider_capacities[provider]
        if capacity > 0:  # Only add edge if capacity > 0
            G_1b.add_edge(provider, SINK, capacity=capacity)

    visualize_graph(G_1b, "Problem 1b: Full Network with Sink",
                    "figures/sink_c_r_graph.png", num_data_hubs)


    G_residual = G_1b.copy()

    for hub, assigned_provider in preliminary_assignment.items():
        if G_residual.has_edge(SOURCE, hub):
            G_residual[SOURCE][hub]['capacity'] = 0
        G_residual.add_edge(hub, SOURCE, capacity=1)

        if G_residual.has_edge(hub, assigned_provider):
            G_residual[hub][assigned_provider]['capacity'] = 0
        G_residual.add_edge(assigned_provider, hub, capacity=1)

        if G_residual.has_edge(assigned_provider, SINK):
            G_residual[assigned_provider][SINK]['capacity'] -= 1
        G_residual.add_edge(SINK, assigned_provider, capacity=1)

    visualize_graph(G_residual, "Problem 1c: Residual Graph",
                    "figures/residual_graph.png", num_data_hubs, show_zero_capacity=True)

    return True


def visualize_graph(G, title, filename, num_data_hubs, show_zero_capacity=False):
    import os

    os.makedirs('figures', exist_ok=True)

    G_vis = G.copy()

    if not show_zero_capacity:
        edges_to_remove = [(u, v) for u, v, data in G_vis.edges(data=True)
                          if data.get('capacity', 1) == 0]
        G_vis.remove_edges_from(edges_to_remove)

    plt.figure(figsize=(14, 10))

    pos = get_hierarchical_layout(G_vis, num_data_hubs)

    labels = {}
    for node in G_vis.nodes():
        if node == 'source':
            labels[node] = 'source'
        elif node == 'sink':
            labels[node] = 'sink'
        elif isinstance(node, int):
            if node < num_data_hubs:
                labels[node] = f'hub{node}'
            else:
                labels[node] = f'prov{node - num_data_hubs}'

    node_colors = 'lightblue'

    nx.draw_networkx_nodes(G_vis, pos, node_color=node_colors,
                          node_size=800, alpha=0.9)

    nx.draw_networkx_edges(G_vis, pos, edge_color='gray',
                          arrows=True, arrowsize=20,
                          arrowstyle='->', width=2)

    nx.draw_networkx_labels(G_vis, pos, labels, font_size=10, font_weight='bold')

    plt.title(title, fontsize=14, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {filename}")


def get_hierarchical_layout(G, num_data_hubs):
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