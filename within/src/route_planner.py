import heapq


class RoutePlanner:
    """Base class (interface) for route planning."""

    def find_route(self, network, start_node, end_node):
        raise NotImplementedError


class AStarRoutePlanner(RoutePlanner):
    """
    Implements a basic A* search on our custom adjacency structure,
    which stores tuples of the form:
        (neighbor_node, distance, traffic_factor, street_name)
    """

    def find_route(self, network, start_node, end_node):
        """
        Returns a list of node IDs from start_node to end_node.
        If no path is found, returns an empty list.
        """
        # Priority queue of (f_score, node)
        open_set = []
        heapq.heappush(open_set, (0, start_node))

        came_from = {}
        g_score = {start_node: 0.0}
        f_score = {
            start_node: self.heuristic_cost_estimate(network, start_node, end_node)
        }
        closed_set = set()

        while open_set:
            _, current = heapq.heappop(open_set)

            if current in closed_set:
                continue
            closed_set.add(current)

            # Goal check
            if current == end_node:
                return self.reconstruct_path(came_from, current)

            # Explore neighbors
            neighbors = network.adjacency.get(current, [])
            for (nbr, base_dist, traffic_factor, st_name) in neighbors:
                # Actual cost so far + edge cost
                tentative_g = g_score[current] + base_dist * traffic_factor

                # If this neighbor hasn't been visited or we found a cheaper path
                if nbr not in g_score or tentative_g < g_score[nbr]:
                    came_from[nbr] = current
                    g_score[nbr] = tentative_g
                    f_score[nbr] = tentative_g + self.heuristic_cost_estimate(
                        network, nbr, end_node
                    )
                    heapq.heappush(open_set, (f_score[nbr], nbr))

        return []

    def heuristic_cost_estimate(self, network, node_id, goal_id):
        """
        Straight-line (haversine) distance as our heuristic.
        """
        lat1, lon1 = network.node_coords[node_id]
        lat2, lon2 = network.node_coords[goal_id]
        return network.haversine_distance(lat1, lon1, lat2, lon2)

    def reconstruct_path(self, came_from, current):
        """
        Build the path by backtracking 'came_from'.
        """
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        return list(reversed(path))
