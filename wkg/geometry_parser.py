from wkg.models import Coordinate, Box


def load_geometries_from_file(path: str) -> list[Box]:
    boxes = []

    with open(path, "r") as file:
        for line in file:
            if line.startswith("BOX"):
                _, start_coords, end_coords = line.strip().split()
                x1, y1, z1 = map(float, start_coords[1:-1].split(","))
                x2, y2, z2 = map(float, end_coords[1:-1].split(","))
                box_obj = Box(start=Coordinate(x=x1, y=y1, z=z1),
                              end=Coordinate(x=x2, y=y2, z=z2))
                boxes.append(box_obj)

    return boxes
