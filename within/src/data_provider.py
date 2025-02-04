import osmnx as ox


class DataProvider:
    """Fetch OSM data for a given place and network type."""

    def __init__(self, place_name="Austin, Texas", network_type="drive"):
        self.place_name = place_name
        self.network_type = network_type

    def fetch_osm_data(self):
        """
        Use OSMnx to get street network graph from OSM.
        """
        print(
            f"Fetching OSM data for '{self.place_name}' (network_type={self.network_type})..."
        )
        G = ox.graph_from_place(self.place_name, network_type=self.network_type)

        return G
