import FreeCAD as App
import Part
from FreeCAD import Base

doc = App.newDocument("ChickenCoop")

# Set unit to millimeters
App.ParamGet("User parameter:BaseApp/Preferences/Units").SetInt("UserSchema", 1)

# Parameters
width = 1000
length = 1500
height = 1000
wall_thickness = 50
roof_overhang = 100
roof_height = 500

# Create walls
def create_wall(name, start, end, height, thickness):
    wall = doc.addObject("Part::Box", name)
    wall.Width = thickness
    wall.Length = (end - start).Length
    wall.Height = height
    wall.Placement.Base = start
    return wall

walls = []
walls.append(create_wall("FrontWall", Base.Vector(0, 0, 0), Base.Vector(width, 0, 0), height, wall_thickness))
walls.append(create_wall("BackWall", Base.Vector(0, length, 0), Base.Vector(width, length, 0), height, wall_thickness))
walls.append(create_wall("LeftWall", Base.Vector(0, wall_thickness, 0), Base.Vector(0, length - wall_thickness, 0), height, wall_thickness))
walls.append(create_wall("RightWall", Base.Vector(width - wall_thickness, wall_thickness, 0), Base.Vector(width - wall_thickness, length - wall_thickness, 0), height, wall_thickness))

# Create gable roof
def create_roof(name, start, end, width, height, overhang):
    roof = doc.addObject("Part::Loft", name)
    section1 = Part.makePolygon([start, start + Base.Vector(width, 0, 0), start + Base.Vector(width / 2, 0, height), start])
    section2 = Part.makePolygon([end, end + Base.Vector(width, 0, 0), end + Base.Vector(width / 2, 0, height), end])
    roof.Sections = [section1, section2]
    return roof

roof = create_roof("Roof", Base.Vector(-roof_overhang, -roof_overhang, height), Base.Vector(-roof_overhang, length + roof_overhang, height), width + 2 * roof_overhang, roof_height, roof_overhang)

doc.recompute()
