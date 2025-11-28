# Problem 1e

from collections import defaultdict, deque

def plan_city_e(num_data_hubs, num_service_providers, connections, provider_capacities, preliminary_assignment):
    """
    Provide the final connectivity map if feasible, or indicate which provider capacities to increase.

    Args:
        num_data_hubs: Number of data hubs (n)
        num_service_providers: Number of service providers (k)
        connections: Dictionary mapping data hub -> list of service providers
        provider_capacities: List where index i has capacity (0 for hubs, actual capacity for providers)
        preliminary_assignment: Dictionary mapping data hub -> assigned service provider (excludes last hub)

    Returns:
        list: If feasible - list of service provider assignments for each hub
              If not feasible - list of zeros for hubs + indicators for which providers need capacity increase
    """

    # Define special node names
    SOURCE = 'source'
    SINK = 'sink'

    # Build the residual graph
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

    # Step 5: Track flow assignments to reconstruct the solution
    # We need to track actual flow for reconstruction
    flow_graph = defaultdict(lambda: defaultdict(int))

    # Initialize flow with preliminary assignments
    for hub, provider in preliminary_assignment.items():
        flow_graph[SOURCE][hub] = 1
        flow_graph[hub][provider] = 1
        flow_graph[provider][SINK] = 1

    # Step 6: Run Edmonds-Karp and track the flow
    max_flow = edmonds_karp_with_flow(residual_graph, SOURCE, SINK, flow_graph)

    # Total flow = preliminary assignments + additional flow
    total_flow = len(preliminary_assignment) + max_flow

    # Step 7: Check if assignment is feasible
    if total_flow >= num_data_hubs:
        # Feasible - extract the assignment from flow_graph
        assignment = extract_assignment(flow_graph, num_data_hubs)
        return assignment
    else:
        # Not feasible - determine which provider capacities should be increased
        # Find min-cut: edges from reachable to non-reachable nodes
        reachable = find_reachable_from_source(residual_graph, SOURCE)

        # Providers that need capacity increase are those with saturated edges to sink
        # that are part of the min-cut
        capacity_increase = [0] * num_data_hubs  # Zeros for data hubs

        for provider in range(num_data_hubs, num_data_hubs + num_service_providers):
            # Check if this provider is on the min-cut
            # A provider needs capacity increase if:
            # 1. The provider is reachable from source
            # 2. There's a saturated edge from provider to sink (capacity 0 in residual)
            # 3. Sink is not reachable (which means we're at the cut)

            if provider in reachable and SINK not in reachable:
                # Provider is reachable, sink is not
                # Check if provider->sink edge exists and is saturated
                original_capacity = provider_capacities[provider]
                residual_capacity = residual_graph[provider].get(SINK, 0)

                # If there was original capacity and it's now saturated, this is a bottleneck
                if original_capacity > 0 and residual_capacity == 0:
                    capacity_increase.append(1)
                else:
                    capacity_increase.append(0)
            else:
                capacity_increase.append(0)

        return capacity_increase


def edmonds_karp_with_flow(residual_graph, source, sink, flow_graph):
    """
    Edmonds-Karp algorithm that also updates the flow graph.
    """
    max_flow = 0

    while True:
        # Find augmenting path using BFS
        parent = bfs_find_path(residual_graph, source, sink)

        if parent is None:
            break

        # Find minimum capacity along the path
        path_flow = float('inf')
        current = sink
        while current != source:
            prev = parent[current]
            path_flow = min(path_flow, residual_graph[prev][current])
            current = prev

        # Update residual capacities and flow graph
        current = sink
        while current != source:
            prev = parent[current]
            residual_graph[prev][current] -= path_flow
            residual_graph[current][prev] += path_flow

            # Update flow graph
            flow_graph[prev][current] += path_flow

            current = prev

        max_flow += path_flow

    return max_flow


def bfs_find_path(residual_graph, source, sink):
    """
    BFS to find an augmenting path from source to sink.
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

    return None


def extract_assignment(flow_graph, num_data_hubs):
    """
    Extract the assignment of data hubs to service providers from the flow graph.
    """
    assignment = [0] * num_data_hubs

    for hub in range(num_data_hubs):
        # Find which provider this hub is connected to (flow > 0)
        # Look for positive flow from hub to provider
        for provider, flow in flow_graph[hub].items():
            if flow > 0 and isinstance(provider, int) and provider >= num_data_hubs:
                assignment[hub] = provider
                break

    return assignment


def find_reachable_from_source(residual_graph, source):
    """
    Find all nodes reachable from source in the residual graph (for min-cut).
    """
    visited = set([source])
    queue = deque([source])

    while queue:
        current = queue.popleft()

        for neighbor, capacity in residual_graph[current].items():
            if neighbor not in visited and capacity > 0:
                visited.add(neighbor)
                queue.append(neighbor)

    return visited