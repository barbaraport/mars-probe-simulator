import pytest

from app.domain.probe.entities.probe import Probe
from app.domain.probe.exceptions import InvalidCoordinateError
from app.schemas.direction import Direction


@pytest.mark.parametrize(
    ("x", "y", "direction"),
    [(0, 0, Direction.SOUTH), (1, 0, Direction.SOUTH), (0, 1, Direction.SOUTH)],
)
def test_when_setting_probe_place_with_valid_coordinates_then_should_allow_successfully(
    x: int, y: int, direction: Direction
):
    probe = Probe(x=x, y=y, direction=direction)

    assert probe.x == x
    assert probe.y == y
    assert probe.direction == direction


def test_when_setting_probe_place_with_invalid_x_coordinate_then_should_not_allow():
    with pytest.raises(InvalidCoordinateError) as exc_info:
        Probe(x=-1, y=0, direction=Direction.EAST)

    assert str(exc_info.value) == "-1 (X value) is not a positive integer"


def test_when_setting_probe_place_with_invalid_y_coordinate_then_should_not_allow():
    with pytest.raises(InvalidCoordinateError) as exc_info:
        Probe(x=0, y=-1, direction=Direction.EAST)

    assert str(exc_info.value) == "-1 (Y value) is not a positive integer"
