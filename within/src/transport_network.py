import math
from scipy.spatial import KDTree


class TransportNetwork:
    """
    Builds and stores a custom adjacency structure from the OSMnx graph.
    Uses a KDTree to speed up nearest node retrieval.
    """

    def __init__(self):
        self.node_coords = {}
        self.adjacency = {}
        self.kd_tree = None
        self.nodes_list = []

    def build_from_osm(self, osm_graph):
        """
        Builds the network from the OSMnx graph and initializes the KDTree.
        """
        points = []
        for node_id, data in osm_graph.nodes(data=True):
            lat = data.get("y")
            lon = data.get("x")
            self.node_coords[node_id] = (lat, lon)
            points.append((lat, lon))
            self.nodes_list.append(node_id)

        # Build the KDTree for fast nearest-neighbor queries.
        self.kd_tree = KDTree(points)

        # Process edges
        for u, v, edge_data in osm_graph.edges(data=True):
            distance = edge_data.get("length", 1.0)
            traffic_factor = 1.0
            street_name = edge_data.get("name", "Unnamed Road")
            self.add_edge(u, v, distance, traffic_factor, street_name)

    def add_edge(self, u, v, distance, traffic_factor=1.0, street_name=""):
        """
        Adds an edge from node u to node v with the specified attributes.
        """
        if u not in self.adjacency:
            self.adjacency[u] = []
        self.adjacency[u].append((v, distance, traffic_factor, street_name))

    def get_nearest_node(self, lat, lon):
        """
        Retrieves the nearest node to the given latitude and longitude using the KDTree.
        """
        if self.kd_tree is None:
            raise ValueError(
                "KDTree not initialized. Please call build_from_osm first."
            )

        # Query the KDTree for the nearest point.
        _, index = self.kd_tree.query((lat, lon))
        return self.nodes_list[index]

    @staticmethod
    def haversine_distance(lat1, lon1, lat2, lon2):
        """
        Computes the haversine distance (in meters) between two latitude/longitude points.
        """
        R = 6371000

        d_lat = math.radians(lat2 - lat1)
        d_lon = math.radians(lon2 - lon1)

        a = (
            math.sin(d_lat / 2) ** 2
            + math.cos(math.radians(lat1))
            * math.cos(math.radians(lat2))
            * math.sin(d_lon / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return R * c
