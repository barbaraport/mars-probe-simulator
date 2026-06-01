import pytest

from app.domain.probe.entities.grid import Grid
from app.domain.probe.exceptions import InvalidSizeError


def test_when_create_grid_entity_with_valid_values_then_creation_should_be_successful():
    grid = Grid(x_size=10, y_size=5)

    assert grid.x_size == 10
    assert grid.y_size == 5


def test_when_create_grid_entity_with_zeroed_values_then_creation_should_not_be_possible():
    with pytest.raises(InvalidSizeError) as exc_info:
        Grid(x_size=0, y_size=0)

    assert str(exc_info.value) == "At least one value (0, 0) must be greater than zero."


def test_when_create_grid_entity_with_x_negative_value_then_creation_should_not_be_possible():
    with pytest.raises(InvalidSizeError) as exc_info:
        Grid(x_size=-1, y_size=0)

    assert str(exc_info.value) == "X (-1) must be a positive integer."


def test_when_create_grid_entity_with_y_negative_value_then_creation_should_not_be_possible():
    with pytest.raises(InvalidSizeError) as exc_info:
        Grid(x_size=5, y_size=-5)

    assert str(exc_info.value) == "Y (-5) must be a positive integer."


@pytest.mark.parametrize(
    ("x", "y"),
    [
        (0, 0),  # lower boundary
        (5, 3),  # upper boundary
        (1, 1),  # inside grid
        (4, 2),  # inside grid
        (0, 3),  # corner
        (5, 0),  # corner
        (5, 3),  # corner
    ],
)
def test_when_moving_inside_grid_limits_then_should_return_true(x: int, y: int):
    grid = Grid(x_size=5, y_size=3)
    assert grid.is_movement_inside_grid_limits(x, y) is True


@pytest.mark.parametrize(
    ("x", "y"),
    [
        (-1, 0),  # x below minimum
        (0, -1),  # y below minimum
        (6, 0),  # x above maximum
        (0, 4),  # y above maximum
        (-1, -1),  # both below minimum
        (6, 4),  # both above maximum
        (-1, 4),  # x below, y above
        (6, -1),  # x above, y below
    ],
)
def test_when_moving_outside_grid_limits_then_should_return_false(x: int, y: int):
    grid = Grid(x_size=5, y_size=3)
    assert grid.is_movement_inside_grid_limits(x, y) is False
