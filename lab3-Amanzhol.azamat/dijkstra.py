# dijkstra.py
import heapq
import time

def dijkstra(graph_obj, start, end, mode="distance"):
    """
    Дайын кітапханасыз, heapq көмегімен жазылған Дейкстра алгоритмі.
    mode: "distance" немесе "time"
    """
    adj = graph_obj.adjacency_list
    if start not in adj or end not in adj:
        return None, float('inf'), 0, 0

    # Инициализация
    distances = {node: float('inf') for node in adj}
    previous = {node: None for node in adj}
    distances[start] = 0
    
    # Басымдық кезегі: (ағымдағы_салмақ, төбе)
    pq = [(0, start)]
    
    nodes_visited_count = 0
    start_time = time.perf_counter()

    while pq:
        current_dist, u = heapq.heappop(pq)
        nodes_visited_count += 1

        # Егер соңғы нүктеге жетсек және ол ең қысқа болса
        if u == end:
            break

        if current_dist > distances[u]:
            continue

        for v, weights in adj[u].items():
            # Егер жол уақытша жабылған болса, оны аттап өтеміз
            if (u, v) in graph_obj.closed_edges:
                continue

            weight = weights[mode]
            distance_through_u = current_dist + weight

            # Релаксация шарты
            if distance_through_u < distances[v]:
                distances[v] = distance_through_u
                previous[v] = u
                heapq.heappush(pq, (distance_through_u, v))

    end_time = time.perf_counter()
    execution_time = end_time - start_time

    # Маршрутты қалпына келтіру (Backtracking)
    path = []
    curr = end
    if distances[end] != float('inf'):
        while curr is not None:
            path.append(curr)
            curr = previous[curr]
        path.reverse()

    return path, distances[end], nodes_visited_count, execution_time
