
"""Interactive Campus Navigation System."""

import matplotlib.pyplot as plt
import networkx as nx
import streamlit as st

from campus_graph import build_campus_graph, get_positions
from dijkstra import dijkstra, get_route_details


st.set_page_config(
    page_title="Campus Navigation System",
    page_icon="🧭",
    layout="wide",
)

WALKING_SPEED_M_PER_MIN = 80  # Approximately 4.8 km/h

# Consistent application styling.
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 2rem;
    }
    div[data-testid="stMetric"] {
        background: rgba(128, 128, 128, 0.08);
        border: 1px solid rgba(128, 128, 128, 0.20);
        padding: 16px;
        border-radius: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

graph = build_campus_graph()
positions = get_positions(graph)
locations = sorted(graph.nodes)

st.title("🧭 Campus Navigation System")
st.caption(
    "Find the shortest walking route between campus landmarks "
    "using Dijkstra's algorithm."
)

# Route selection panel.
with st.container(border=True):
    st.subheader("Plan your journey")

    col1, col2 = st.columns(2)

    with col1:
        source = st.selectbox(
            "Starting Location",
            locations,
            index=locations.index("Main Gate"),
        )

    with col2:
        destination = st.selectbox(
            "Destination",
            locations,
            index=locations.index("Library"),
        )

    find_route = st.button(
        "Find Shortest Path",
        type="primary",
        use_container_width=True,
    )

# Store the last successfully calculated route in this session.
if "route_result" not in st.session_state:
    st.session_state.route_result = None

if find_route:
    try:
        path, total_distance = dijkstra(
            graph, source, destination
        )
        st.session_state.route_result = {
            "source": source,
            "destination": destination,
            "path": path,
            "distance": total_distance,
        }
    except ValueError as error:
        st.session_state.route_result = None
        st.error(str(error))

result = st.session_state.route_result

# Do not show a stale route for newly selected endpoints.
if result and (
    result["source"] != source
    or result["destination"] != destination
):
    result = None

# Draw the full network and overlay the selected shortest path.
def draw_campus_map(campus_graph, route=None):
    fig, ax = plt.subplots(figsize=(11, 6.5))
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")

    nx.draw_networkx_edges(
        campus_graph,
        positions,
        ax=ax,
        edge_color="#C9D2DC",
        width=2,
    )

    # Label every pathway with its distance.
    edge_labels = nx.get_edge_attributes(
        campus_graph, "weight"
    )
    nx.draw_networkx_edge_labels(
        campus_graph,
        positions,
        edge_labels=edge_labels,
        font_size=8,
        font_color="#596579",
        rotate=False,
        ax=ax,
        bbox={
            "alpha": 0.8,
            "color": "white",
            "pad": 1,
            "edgecolor": "none",
        },
    )

    nx.draw_networkx_nodes(
        campus_graph,
        positions,
        ax=ax,
        node_color="#DCE8F5",
        edgecolors="#52677F",
        node_size=1500,
        linewidths=1.5,
    )

    if route:
        route_edges = list(zip(route, route[1:]))

        nx.draw_networkx_edges(
            campus_graph,
            positions,
            edgelist=route_edges,
            ax=ax,
            edge_color="#E63946",
            width=4.5,
        )

        # Highlight the start and destination.
        nx.draw_networkx_nodes(
            campus_graph,
            positions,
            nodelist=[route[0]],
            ax=ax,
            node_color="#2A9D8F",
            edgecolors="#176B62",
            node_size=1750,
        )

        if route[-1] != route[0]:
            nx.draw_networkx_nodes(
                campus_graph,
                positions,
                nodelist=[route[-1]],
                ax=ax,
                node_color="#F4A261",
                edgecolors="#A85D20",
                node_size=1750,
            )

    nx.draw_networkx_labels(
        campus_graph,
        positions,
        ax=ax,
        font_size=8,
        font_weight="bold",
        font_color="#172536",
    )

    ax.set_title(
        "Campus Walking Network",
        fontsize=15,
        fontweight="bold",
        color="#172536",
        pad=18,
    )
    ax.margins(0.18)
    ax.axis("off")
    fig.tight_layout()

    return fig


left, right = st.columns([1.65, 1])

with left:
    st.subheader("Campus map")

    fig = draw_campus_map(
        graph,
        result["path"] if result else None,
    )
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.caption(
        "Gray = available pathways | Red = shortest route | "
        "Teal = start | Orange = destination. "
        "Edge labels show distance in meters."
    )

with right:
    st.subheader("Route details")

    if result:
        path = result["path"]
        distance = result["distance"]
        walking_minutes = distance / WALKING_SPEED_M_PER_MIN

        metric1, metric2 = st.columns(2)
        metric1.metric("Distance", f"{distance:.0f} m")
        metric2.metric("Walking time", f"{walking_minutes:.1f} min")

        st.metric("Locations visited", len(path))

        st.success(
            f"Route found: {result['source']} → "
            f"{result['destination']}"
        )

        st.markdown("**Step-by-step directions**")

        if len(path) == 1:
            st.info("You are already at your destination.")
        else:
            legs = get_route_details(graph, path)

            for index, leg in enumerate(legs, start=1):
                leg_time = leg["distance"] / WALKING_SPEED_M_PER_MIN

                st.markdown(
                    f"**{index}.** {leg['start']} → {leg['end']}"
                )
                st.caption(
                    f"Walk {leg['distance']} m · "
                    f"approximately {leg_time:.1f} min"
                )

            st.markdown("---")
            st.markdown(
                "**Full route:** "
                + " → ".join(path)
            )

        st.caption(
            "Walking time is an estimate at "
            "4.8 km/h and excludes stops or delays."
        )

    else:
        st.info(
            "Select a starting location and destination, "
            "then click **Find Shortest Path**."
        )

        st.markdown("**Available landmarks**")
        for location in locations:
            st.markdown(f"- {location}")

st.divider()

with st.expander("About this application"):
    st.markdown(
        """
        - **Graph:** Weighted, undirected walking network.
        - **Algorithm:** Dijkstra's shortest-path algorithm,
          implemented in `dijkstra.py`.
        - **Distance:** Sum of pathway distances in meters.
        - **Walking time:** Distance divided by 80 meters per minute.
        - **Map:** NetworkX and Matplotlib, with the selected route
          highlighted in red.
        - **Data:** Illustrative campus locations and distances;
          replace these with surveyed campus pathways for real use.
        """
    )