'''
Challenge 1
'''

def cards_game(m, n, k, counts):
    from collections import deque

    cards = []
    for person, card_list in counts.items():
        for value, color in card_list:
            cards.append((person, value, color))

    num_cards = len(cards)
    if num_cards == 0:
        return 0

    source = 0
    sink = num_cards + 1

    capacity = {}

    def add_edge(u, v, cap):
        capacity[(u, v)] = capacity.get((u, v), 0) + cap

    for idx, (person, value, color) in enumerate(cards):
        node = idx + 1
        if value == 1:
            add_edge(source, node, 1)

    for idx, (person, value, color) in enumerate(cards):
        node = idx + 1
        if value == m:
            add_edge(node, sink, 1)

    for i, (p1, v1, c1) in enumerate(cards):
        node1 = i + 1
        for j, (p2, v2, c2) in enumerate(cards):
            if i == j:
                continue

            node2 = j + 1

            next_person = (p1 % n) + 1
            if p2 != p1 and p2 != next_person:
                continue

            if (c2 == c1 and v2 == v1 + 1) or (c2 != c1 and v2 == v1):
                add_edge(node1, node2, 1)

    def bfs():
        parent = {}
        visited = {source}
        queue = deque([source])

        while queue:
            u = queue.popleft()

            if u == sink:
                return parent
            
            for (a, b) in capacity:
                if a == u and b not in visited and capacity[(a, b)] > 0:
                    visited.add(b)
                    parent[b] = u
                    queue.append(b)

        return None

    max_flow = 0

    while True:
        parent = bfs()
        if parent is None:
            break

        path_flow = float('inf')
        v = sink
        while v != source:
            u = parent[v]
            path_flow = min(path_flow, capacity[(u, v)])
            v = u

        v = sink
        while v != source:
            u = parent[v]
            capacity[(u, v)] -= path_flow
            capacity[(v, u)] = capacity.get((v, u), 0) + path_flow
            v = u

        max_flow += path_flow

    return max_flow
