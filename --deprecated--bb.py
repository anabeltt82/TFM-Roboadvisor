
import pandas as pd
import numpy as np
import pyvista as pv


values = np.linspace(0, 10, 15470).reshape((34, 35, 13))
values.shape

# Create the spatial reference
grid = pv.UniformGrid()

# Set the grid dimensions: shape + 1 because we want to inject our values on
#   the CELL data
grid.dimensions = np.array(values.shape) + 1

# Edit the spatial reference
grid.origin = (100, 33, 55.6)  # The bottom left corner of the data set
grid.spacing = (5, 5, 5)  # These are the cell sizes along each axis

# Add the data values to the cell data
grid.cell_data["values"] = values.flatten(order="F")  # Flatten the array!

# Now plot the grid!
grid.plot(show_edges=True)

#cell_labels = values.flatten(order="F")
# Label the Z position
values = grid.points[:, 2]

# Create plotting class and add the unstructured grid
plotter = pv.Plotter()
# color mesh according to z value
plotter.add_mesh(grid, scalars=values,
                 scalar_bar_args={'title': 'Z Position'},
                 show_edges=True)

# Add labels to points on the yz plane (where x == 0)
mask = grid.points[:, 0] == 0
points = grid.points
plotter.add_point_labels(points[mask], values[mask].tolist(), font_size=10)

# add some text to the plot
plotter.add_text('Ejemplo')
plotter.camera_position = 'xy'
plotter.show()


