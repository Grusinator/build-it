import FreeCAD as App
import Part
from FreeCAD import Base
import math

doc = App.newDocument("ChickenCoop")

# Set unit to millimeters
App.ParamGet("User parameter:BaseApp/Preferences/Units").SetInt("UserSchema", 1)

# Assuming the frames and walls are ready

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
plank_thickness = 20
plank_width = 100
plank_spacing = 10
roof_overhang = 100
roof_height = 500

# Parameters
width = 1000
length = 1500
height = 1000
plank_thickness = 20
plank_width = 100
plank_spacing = 10
beam_thickness = 50
roof_overhang = 100
roof_height = 500

# Create planks for walls
def create_wall_planks(start, end, height, plank_width, plank_thickness, plank_spacing, orientation='horizontal'):
    wall_planks = []
    if orientation == 'horizontal':
        num_planks = int((end - start).Length / (plank_width + plank_spacing))
        for i in range(num_planks):
            plank = doc.addObject("Part::Box", f"Plank_{len(wall_planks)}")
            plank.Width = plank_thickness
            plank.Length = plank_width
            plank.Height = height
            plank.Placement.Base = start + Base.Vector((plank_width + plank_spacing) * i, 0, 0)
            wall_planks.append(plank)
    elif orientation == 'vertical':
        num_planks = int(height / (plank_width + plank_spacing))
        for i in range(num_planks):
            plank = doc.addObject("Part::Box", f"Plank_{len(wall_planks)}")
            plank.Width = plank_thickness
            plank.Length = (end - start).Length
            plank.Height = plank_width
            plank.Placement.Base = start + Base.Vector(0, 0, (plank_width + plank_spacing) * i)
            wall_planks.append(plank)
    return wall_planks

front_wall_planks = create_wall_planks(Base.Vector(0, 0, 0), Base.Vector(width, 0, 0), height, plank_width, plank_thickness, plank_spacing, orientation='horizontal')
back_wall_planks = create_wall_planks(Base.Vector(0, length, 0), Base.Vector(width, length, 0), height, plank_width, plank_thickness, plank_spacing, orientation='horizontal')
left_wall_planks = create_wall_planks(Base.Vector(0, plank_thickness, 0), Base.Vector(0, length - plank_thickness, 0), height, plank_width, plank_thickness, plank_spacing, orientation='vertical')
right_wall_planks = create_wall_planks(Base.Vector(width - plank_thickness, plank_thickness, 0), Base.Vector(width - plank_thickness, length - plank_thickness, 0), height, plank_width, plank_thickness, plank_spacing, orientation='vertical')

# Create gable roof
def create_roof(name, start, end, width, height, overhang):
    roof = doc.addObject("Part::Loft", name)
    section1 = Part.makePolygon([start, start + Base.Vector(width, 0, 0), start + Base.Vector(width / 2, 0, height), start])
    section2 = Part.makePolygon([end, end + Base.Vector(width, 0, 0), end + Base.Vector(width / 2, 0, height), end])
    roof.Sections = [section1, section2]
    return roof

roof = create_roof("Roof", Base.Vector(-roof_overhang, -roof_overhang, height), Base.Vector(-roof_overhang, length + roof_overhang, height), width + 2 * roof_overhang)




# Assuming wall plank functions are ready
# ...

# Create corner posts
def create_corner_post(name, position, height, thickness):
    post = doc.addObject("Part::Box", name)
    post.Width = thickness
    post.Length = thickness
    post.Height = height
    post.Placement.Base = position
    return post

corner_posts = []
corner_posts.append(create_corner_post("FrontLeftPost", Base.Vector(0, 0, 0), height, beam_thickness))
corner_posts.append(create_corner_post("FrontRightPost", Base.Vector(width - beam_thickness, 0, 0), height, beam_thickness))
corner_posts.append(create_corner_post("BackLeftPost", Base.Vector(0, length - beam_thickness, 0), height, beam_thickness))
corner_posts.append(create_corner_post("BackRightPost", Base.Vector(width - beam_thickness, length - beam_thickness, 0), height, beam_thickness))

# Create intermediate vertical posts
def create_vertical_posts(start, end, height, thickness, spacing):
    posts = []
    num_posts = int((end - start).Length / spacing)
    for i in range(1, num_posts):
        post = doc.addObject("Part::Box", f"VerticalPost_{len(posts)}")
        post.Width = thickness
        post.Length = thickness
        post.Height = height
        post.Placement.Base = start + Base.Vector((spacing * i) - (thickness / 2), 0, 0)
        posts.append(post)
    return posts

intermediate_vertical_posts = create_vertical_posts(Base.Vector(0, 0, 0), Base.Vector(width, 0, 0), height, beam_thickness, 500)

# Create horizontal beams
def create_horizontal_beam(name, start, end, thickness):
    beam = doc.addObject("Part::Box", name)
    beam.Width = (end - start).Length
    beam.Length = thickness
    beam.Height = thickness
    beam.Placement.Base = start
    return beam

horizontal_beams = []
horizontal_beams.append(create_horizontal_beam("TopFrontBeam", Base.Vector(0, 0, height - beam_thickness), Base.Vector(width, 0, height - beam_thickness), beam_thickness))
horizontal_beams.append(create_horizontal_beam("TopBackBeam", Base.Vector(0, length - beam_thickness, height - beam_thickness), Base.Vector(width, length - beam_thickness, height - beam_thickness), beam_thickness))
horizontal_beams.append(create_horizontal_beam("BottomFrontBeam", Base.Vector(0, 0, 0), Base.Vector(width, 0, 0), beam_thickness))
horizontal_beams.append(create_horizontal_beam("BottomBackBeam", Base.Vector(0, length - beam_thickness, 0), Base.Vector(width, length - beam_thickness, 0), beam_thickness))

doc.recompute()

# Parameters for the door
door_width = 600
door_height = 700
door_thickness = plank_thickness
door_start = Base.Vector((width - door_width) / 2, 0, 100)  # position of the bottom-left corner of the door

# Create door frame
def create_door_frame(start, width, height, thickness):
    frame = []
    frame.append(create_horizontal_beam("DoorTopBeam", start + Base.Vector(0, 0, height), start + Base.Vector(width, 0, height), thickness))
    frame.append(create_horizontal_beam("DoorBottomBeam", start, start + Base.Vector(width, 0, 0), thickness))
    frame.append(create_vertical_posts(start, start + Base.Vector(0, 0, height), height, thickness, width))
    frame.append(create_vertical_posts(start + Base.Vector(width - thickness, 0, 0), start + Base.Vector(width - thickness, 0, height), height, thickness, width))
    return frame

door_frame = create_door_frame(door_start, door_width, door_height, beam_thickness)

# Create door planks
door_planks = create_wall_planks(door_start + Base.Vector(0, beam_thickness, 0), door_start + Base.Vector(door_width - beam_thickness, beam_thickness, 0), door_height - 2 * beam_thickness, plank_width, door_thickness, plank_spacing, orientation='vertical')

# Create horizontal and diagonal beams for the door
door_horizontal_beam_1 = create_horizontal_beam("DoorHorizontalBeam1", door_start + Base.Vector(0, beam_thickness, door_height / 3), door_start + Base.Vector(door_width - beam_thickness, beam_thickness, door_height / 3), beam_thickness)
door_horizontal_beam_2 = create_horizontal_beam("DoorHorizontalBeam2", door_start + Base.Vector(0, beam_thickness, 2 * door_height / 3), door_start + Base.Vector(door_width - beam_thickness, beam_thickness, 2 * door_height / 3), beam_thickness)

def create_diagonal_beam(name, start, end, thickness):
    length = (end - start).Length
    angle = math.atan2(end.z - start.z, end.x - start.x)
    beam = doc.addObject("Part::Box", name)
    beam.Width = thickness
    beam.Length = length
    beam.Height = thickness
    beam.Placement.Base = start
    beam.Placement.Rotation = App.Rotation(App.Vector(0, 1, 0), math.degrees(angle))
    return beam

door_diagonal_beam = create_diagonal_beam("DoorDiagonalBeam", door_start + Base.Vector(0, beam_thickness, door_height / 3), door_start + Base.Vector(door_width - beam_thickness, beam_thickness, 2 * door_height / 3), beam_thickness)

doc.recompute()
