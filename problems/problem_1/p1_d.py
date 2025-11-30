# Problem 1d

from collections import defaultdict, deque

def plan_city_d(num_data_hubs, num_service_providers, connections, provider_capacities, preliminary_assignment):
    SOURCE = 'source'
    SINK = 'sink'

    residual_graph = defaultdict(lambda: defaultdict(int))

    for hub in range(num_data_hubs):
        residual_graph[SOURCE][hub] = 1

    for hub, providers in connections.items():
        for provider in providers:
            residual_graph[hub][provider] = 1

    for provider in range(num_data_hubs, num_data_hubs + num_service_providers):
        capacity = provider_capacities[provider]
        if capacity > 0:
            residual_graph[provider][SINK] = capacity

    for hub, assigned_provider in preliminary_assignment.items():

        if residual_graph[SOURCE][hub] > 0:
            residual_graph[SOURCE][hub] -= 1
            residual_graph[hub][SOURCE] += 1

        if residual_graph[hub][assigned_provider] > 0:
            residual_graph[hub][assigned_provider] -= 1
            residual_graph[assigned_provider][hub] += 1

        if residual_graph[assigned_provider][SINK] > 0:
            residual_graph[assigned_provider][SINK] -= 1
            residual_graph[SINK][assigned_provider] += 1

    max_flow = edmonds_karp(residual_graph, SOURCE, SINK)

    required_flow = num_data_hubs

    total_flow = len(preliminary_assignment) + max_flow

    return total_flow >= required_flow


def edmonds_karp(residual_graph, source, sink):
    max_flow = 0

    while True:
        parent = bfs_find_path(residual_graph, source, sink)

        if parent is None:
            break

        path_flow = float('inf')
        current = sink
        while current != source:
            prev = parent[current]
            path_flow = min(path_flow, residual_graph[prev][current])
            current = prev

        current = sink
        while current != source:
            prev = parent[current]
            residual_graph[prev][current] -= path_flow
            residual_graph[current][prev] += path_flow
            current = prev

        max_flow += path_flow

    return max_flow


def bfs_find_path(residual_graph, source, sink):
    visited = set([source])
    queue = deque([source])
    parent = {}

    while queue:
        current = queue.popleft()

        if current == sink:
            return parent
        for neighbor, capacity in residual_graph[current].items():
            if neighbor not in visited and capacity > 0:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)

    return None