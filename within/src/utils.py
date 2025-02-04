import math


def compute_bearing(lat1, lon1, lat2, lon2):
    """Computes normalized bearing."""
    lat1_rad, lon1_rad = map(math.radians, [lat1, lon1])
    lat2_rad, lon2_rad = map(math.radians, [lat2, lon2])

    d_lon = lon2_rad - lon1_rad
    x = math.sin(d_lon) * math.cos(lat2_rad)
    y = math.cos(lat1_rad) * math.sin(lat2_rad) - math.sin(lat1_rad) * math.cos(
        lat2_rad
    ) * math.cos(d_lon)
    bearing = math.degrees(math.atan2(x, y))

    return (bearing + 360) % 360


def to_cardinal_direction(bearing_degs):
    """Converts normalized bearing into Cardinal direction."""
    if bearing_degs < 22.5:
        return "north"
    elif bearing_degs < 67.5:
        return "northeast"
    elif bearing_degs < 112.5:
        return "east"
    elif bearing_degs < 157.5:
        return "southeast"
    elif bearing_degs < 202.5:
        return "south"
    elif bearing_degs < 247.5:
        return "southwest"
    elif bearing_degs < 292.5:
        return "west"
    elif bearing_degs < 337.5:
        return "northwest"
    else:
        return "north"
