from src.models import RouteInput, RouteOutput
from src.transport_network import TransportNetwork

from src.utils import compute_bearing, to_cardinal_direction


class RouteRecommender:
    """
    Orchestrates data fetching, network creation, pathfinding, and summarization.
    """

    def __init__(self, data_provider, route_planner, summarizer=None):
        self.data_provider = data_provider
        self.route_planner = route_planner
        self.summarizer = summarizer
        self.network = TransportNetwork()

    def initialize_network(self):
        osm_graph = self.data_provider.fetch_osm_data()
        self.network.build_from_osm(osm_graph)

    def get_human_friendly_route(self, route_input: RouteInput) -> RouteOutput:
        start_node = self.network.get_nearest_node(
            route_input.start_lat, route_input.start_lon
        )
        end_node = self.network.get_nearest_node(
            route_input.end_lat, route_input.end_lon
        )
        path_nodes = self.route_planner.find_route(self.network, start_node, end_node)

        edge_list = []
        total_distance = 0.0

        for i in range(len(path_nodes) - 1):
            curr_node = path_nodes[i]
            next_node = path_nodes[i + 1]

            # Look up the adjacency info
            neighbors = self.network.adjacency.get(curr_node, [])
            edge_data = None
            for (nbr, dist, t_fact, st_name) in neighbors:
                if nbr == next_node:
                    # Found the correct edge
                    # Compute the bearing so we can get a direction
                    lat1, lon1 = self.network.node_coords[curr_node]
                    lat2, lon2 = self.network.node_coords[next_node]
                    bearing_degs = compute_bearing(lat1, lon1, lat2, lon2)
                    direction = to_cardinal_direction(bearing_degs)

                    edge_data = (st_name, dist, direction)
                    total_distance += dist
                    break

            if edge_data:
                st_name, dist, direction = edge_data
                edge_list.append((st_name, dist, direction))

        merged_steps = []
        if edge_list:
            current_street, current_dist, current_dir = edge_list[0]
            for i in range(1, len(edge_list)):
                st_name, dist, direction = edge_list[i]
                if st_name == current_street and direction == current_dir:
                    current_dist += dist
                else:
                    merged_steps.append((current_street, current_dist, current_dir))
                    current_street, current_dist, current_dir = st_name, dist, direction

            # Add the last group
            merged_steps.append((current_street, current_dist, current_dir))

        # Build the final textual instructions
        steps_text = []
        for (st_name, dist, direction) in merged_steps:
            steps_text.append(f"Continue {direction} on {st_name} for approximately {dist:.0f} meters.")

        route_description = (
            f"Recommended route (~{total_distance:.0f} meters):\n" +
            "\n".join(steps_text)
        )

        # Run this through LLM summarizer
        if self.summarizer:
            friendly_text = self.summarizer.summarize_route(route_description)
        else:
            friendly_text = route_description

        return RouteOutput(raw_nodes=path_nodes, text_instructions=friendly_text)
