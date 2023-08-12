from pydantic import BaseModel


class Coordinate(BaseModel):
    x: float
    y: float
    z: float


class Box(BaseModel):
    start: Coordinate
    end: Coordinate
