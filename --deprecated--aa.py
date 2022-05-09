
import numpy as np
# Load module and example file
import pyvista as pv
from pyvista import examples

# Load example beam file
grid = pv.UnstructuredGrid(examples.hexbeamfile)

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
#plotter.add_point_labels(points[mask], values[mask].tolist(), font_size=24)

cell_labels = [f'Cell {i}' for i in range(grid.n_cells)]
plotter.add_point_labels(grid.cell_centers(), cell_labels, font_size=24)

# add some text to the plot
plotter.add_text('Example showing plot labels')

plotter.view_vector((-6, -3, -4), (0.,-1., 0.))
plotter.show()