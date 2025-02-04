from ..src.utils import compute_bearing, to_cardinal_direction


def test_compute_bearing_zero_distance():
    bearing = compute_bearing(30, -97, 30, -97)
    assert bearing == 0, "Bearing should be 0 if start and end are identical"


def test_compute_bearing_east_direction():
    bearing = compute_bearing(0, 0, 0, 1)
    assert 85 < bearing < 95, f"Expected bearing ~90, got {bearing}"


def test_to_cardinal_direction():
    assert to_cardinal_direction(0) == "north"
    assert to_cardinal_direction(45) == "northeast"
    assert to_cardinal_direction(90) == "east"
    assert to_cardinal_direction(180) == "south"
    assert to_cardinal_direction(270) == "west"
    assert to_cardinal_direction(359) == "north"
