# Problem 1d

from collections import defaultdict, deque

def plan_city_d(num_data_hubs, num_service_providers, connections, provider_capacities, preliminary_assignment):
    """
    Determine if each data hub can be connected to a service provider.

    Uses Ford-Fulkerson (Edmonds-Karp) algorithm to find maximum flow.
    Returns True if all data hubs (including the last one) can be connected.

    Args:
        num_data_hubs: Number of data hubs (n)
        num_service_providers: Number of service providers (k)
        connections: Dictionary mapping data hub -> list of service providers
        provider_capacities: List where index i has capacity (0 for hubs, actual capacity for providers)
        preliminary_assignment: Dictionary mapping data hub -> assigned service provider (excludes last hub)

    Returns:
        bool: True if all data hubs can be connected, False otherwise
    """

    # Define special node names
    SOURCE = 'source'
    SINK = 'sink'

    # Build the residual graph
    # residual_graph[u][v] = residual capacity from u to v
    residual_graph = defaultdict(lambda: defaultdict(int))

    # Step 1: Add edges from source to data hubs (capacity 1)
    for hub in range(num_data_hubs):
        residual_graph[SOURCE][hub] = 1

    # Step 2: Add edges from data hubs to service providers (capacity 1)
    for hub, providers in connections.items():
        for provider in providers:
            residual_graph[hub][provider] = 1

    # Step 3: Add edges from service providers to sink (based on provider_capacities)
    for provider in range(num_data_hubs, num_data_hubs + num_service_providers):
        capacity = provider_capacities[provider]
        if capacity > 0:
            residual_graph[provider][SINK] = capacity

    # Step 4: Apply preliminary assignments to create residual graph
    for hub, assigned_provider in preliminary_assignment.items():
        # Flow of 1 has been sent through: source -> hub -> provider -> sink

        # Update source -> hub edge (reduce capacity by 1, add backward edge)
        if residual_graph[SOURCE][hub] > 0:
            residual_graph[SOURCE][hub] -= 1
            residual_graph[hub][SOURCE] += 1

        # Update hub -> provider edge (reduce capacity by 1, add backward edge)
        if residual_graph[hub][assigned_provider] > 0:
            residual_graph[hub][assigned_provider] -= 1
            residual_graph[assigned_provider][hub] += 1

        # Update provider -> sink edge (reduce capacity by 1, add backward edge)
        if residual_graph[assigned_provider][SINK] > 0:
            residual_graph[assigned_provider][SINK] -= 1
            residual_graph[SINK][assigned_provider] += 1

    # Step 5: Run Edmonds-Karp (BFS-based Ford-Fulkerson) to find if we can assign the last hub
    # We need to check if max flow equals num_data_hubs
    max_flow = edmonds_karp(residual_graph, SOURCE, SINK)

    # Total flow needed is num_data_hubs (one for each hub)
    # We already have flow for preliminary_assignment hubs, so we need to check
    # if we can add one more flow for the last hub
    required_flow = num_data_hubs

    # Actually, the max_flow should equal num_data_hubs if all hubs can be connected
    # Since we already applied preliminary assignments, max_flow represents additional flow
    # Total flow = len(preliminary_assignment) + max_flow
    total_flow = len(preliminary_assignment) + max_flow

    return total_flow >= required_flow


def edmonds_karp(residual_graph, source, sink):
    """
    Edmonds-Karp algorithm for finding maximum flow.
    Uses BFS to find augmenting paths.

    Args:
        residual_graph: Adjacency dict of dicts representing residual capacities
        source: Source node
        sink: Sink node

    Returns:
        int: Maximum flow value
    """
    max_flow = 0

    while True:
        # Find augmenting path using BFS
        parent = bfs_find_path(residual_graph, source, sink)

        if parent is None:
            # No more augmenting paths
            break

        # Find minimum capacity along the path
        path_flow = float('inf')
        current = sink
        while current != source:
            prev = parent[current]
            path_flow = min(path_flow, residual_graph[prev][current])
            current = prev

        # Update residual capacities along the path
        current = sink
        while current != source:
            prev = parent[current]
            residual_graph[prev][current] -= path_flow
            residual_graph[current][prev] += path_flow
            current = prev

        max_flow += path_flow

    return max_flow


def bfs_find_path(residual_graph, source, sink):
    """
    BFS to find an augmenting path from source to sink.

    Args:
        residual_graph: Adjacency dict of dicts representing residual capacities
        source: Source node
        sink: Sink node

    Returns:
        dict: Parent pointers for reconstructing path, or None if no path exists
    """
    visited = set([source])
    queue = deque([source])
    parent = {}

    while queue:
        current = queue.popleft()

        if current == sink:
            return parent

        # Explore neighbors with positive residual capacity
        for neighbor, capacity in residual_graph[current].items():
            if neighbor not in visited and capacity > 0:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)

    return None  # No path found