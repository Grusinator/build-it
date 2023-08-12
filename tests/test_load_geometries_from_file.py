import pytest

from wkg.geometry_parser import load_geometries_from_file
from wkg.models import Coordinate


def test_load_geometries_from_file():
    # Create a sample file with box data
    with open('sample_data.txt', 'w') as f:
        f.write("BOX (1,2,3) (4,5,6)\n")
        f.write("BOX (0,0,0) (1,1,1)\n")

    boxes = load_geometries_from_file('sample_data.txt')

    assert len(boxes) == 2, "Expected 2 boxes to be loaded."

    # Check the coordinates of the first box
    box1 = boxes[0]
    assert box1.start == Coordinate(x=1, y=2, z=3), "Box1 start coordinates are incorrect."
    assert box1.end == Coordinate(x=4, y=5, z=6), "Box1 end coordinates are incorrect."

    # Check the coordinates of the second box
    box2 = boxes[1]
    assert box2.start == Coordinate(x=0, y=0, z=0), "Box2 start coordinates are incorrect."
    assert box2.end == Coordinate(x=1, y=1, z=1), "Box2 end coordinates are incorrect."


@pytest.mark.parametrize(
    'input_file',
    ['wkg/example_files/house.wkg']  # you can add more filenames if needed
)
def test_load_geometries_from_file_regression(data_regression, input_file):
    loaded_boxes = load_geometries_from_file(input_file)
    data = [box.model_dump() for box in loaded_boxes]
    data_regression.check(data)