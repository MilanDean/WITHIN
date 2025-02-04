from src.data_provider import DataProvider
from src.models import RouteInput
from src.route_planner import AStarRoutePlanner
from src.route_recommender import RouteRecommender
from src.summarizer import LLMRouteSummarizer

import os
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"


def main():
    # Instantiate our components
    data_provider = DataProvider("Austin, Texas", network_type="drive")
    route_planner = AStarRoutePlanner()
    summarizer = LLMRouteSummarizer()

    # Combine components into a RouteRecommender
    recommender = RouteRecommender(data_provider, route_planner, summarizer)
    recommender.initialize_network()

    route_input = RouteInput(
        # Test example starting at Austin City Hall
        start_lat=30.2672,
        start_lon=-97.7431,
        # Test example ending at UT Austin
        end_lat=30.2814,
        end_lon=-97.7410,
    )

    route_output = recommender.get_human_friendly_route(route_input)

    print("\n--- Route Results ---")
    print("Raw node sequence:", route_output.raw_nodes, "\n")
    print(route_output.text_instructions, "\n")


if __name__ == "__main__":
    main()
