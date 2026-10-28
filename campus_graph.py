
"""Campus graph data and visualization layout."""

import networkx as nx


def build_campus_graph():
    """Build a weighted, undirected campus walking network."""
    graph = nx.Graph()

    # (x, y) positions are illustrative campus-map coordinates.
    locations = {
        "Main Gate": (0, 2),
        "Administration Block": (2, 3),
        "Library": (4, 4),
        "Engineering Building": (5, 2),
        "Student Center": (3, 0),
        "Cafeteria": (5, -1),
        "Sports Complex": (7, 1),
        "Dormitories": (8, -2),
        "Science Block": (7, 4),
        "Parking Lot": (-2, 1),
    }

    for name, position in locations.items():
        graph.add_node(name, pos=position)

    # (start, destination, walking distance in meters)
    pathways = [
        ("Main Gate", "Administration Block", 180),
        ("Main Gate", "Parking Lot", 100),
        ("Parking Lot", "Student Center", 260),
        ("Administration Block", "Library", 150),
        ("Administration Block", "Student Center", 200),
        ("Library", "Engineering Building", 220),
        ("Library", "Science Block", 170),
        ("Engineering Building", "Student Center", 160),
        ("Engineering Building", "Sports Complex", 200),
        ("Engineering Building", "Science Block", 140),
        ("Student Center", "Cafeteria", 100),
        ("Cafeteria", "Sports Complex", 230),
        ("Cafeteria", "Dormitories", 180),
        ("Sports Complex", "Dormitories", 210),
        ("Science Block", "Sports Complex", 190),
        ("Student Center", "Dormitories", 450),
    ]

    for start, end, distance in pathways:
        graph.add_edge(start, end, weight=distance)

    return graph


def get_positions(graph):
    """Return the fixed positions used for the campus map."""
    return nx.get_node_attributes(graph, "pos")