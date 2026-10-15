import Rhino

# Create a new Rhino document
doc = Rhino.RhinoDoc.ActiveDoc

# Define the box dimensions
box_width = 10.0
box_height = 10.0
box_depth = 10.0

# Create the box geometry
box_plane = Rhino.Geometry.Plane.WorldXY
box = Rhino.Geometry.Box(box_plane, box_width, box_height, box_depth)

# Add the box to the document
box_id = doc.Objects.AddBox(box)

# Redraw the Rhino view to show the new box
doc.Views.Redraw()
