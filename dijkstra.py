
"""Dijkstra's shortest-path algorithm."""

import heapq
import math


def dijkstra(graph, source, destination):
    """
    Find the shortest weighted path between two campus locations.

    Returns:
        (path, distance)
        path: list of location names, including both endpoints
        distance: total distance in meters

    Raises:
        ValueError: if a location is unknown or the destination is
                    unreachable.
    """
    if source not in graph:
        raise ValueError(f"Unknown starting location: {source}")

    if destination not in graph:
        raise ValueError(f"Unknown destination: {destination}")

    if source == destination:
        return [source], 0

    distances = {node: math.inf for node in graph.nodes}
    previous = {node: None for node in graph.nodes}

    distances[source] = 0
    priority_queue = [(0, source)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(
            priority_queue
        )

        # Ignore obsolete queue entries.
        if current_distance > distances[current_node]:
            continue

        if current_node == destination:
            break

        for neighbor, edge_data in graph[current_node].items():
            weight = edge_data["weight"]

            if weight < 0:
                raise ValueError(
                    "Dijkstra's algorithm requires non-negative weights."
                )

            new_distance = current_distance + weight

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = current_node

                heapq.heappush(
                    priority_queue,
                    (new_distance, neighbor),
                )

    if math.isinf(distances[destination]):
        raise ValueError(
            f"No walking route exists from {source} to {destination}."
        )

    # Reconstruct the route by walking backward from the destination.
    path = []
    current = destination

    while current is not None:
        path.append(current)
        current = previous[current]

    path.reverse()

    return path, distances[destination]


def get_route_details(graph, path):
    """Return each leg of a calculated route."""
    legs = []

    for start, end in zip(path, path[1:]):
        distance = graph[start][end]["weight"]

        legs.append({
            "start": start,
            "end": end,
            "distance": distance,
        })

    return legs