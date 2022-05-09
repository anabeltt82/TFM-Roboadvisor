import numpy as np
import pyvista as pv
from sympy import true

#values = np.linspace(0, 10, 15470).reshape((34, 35, 13))

values = np.zeros(shape=15470)
values[5] = 1
values[10]=1
values[1] = 1
values = values.reshape((34, 35, 13))
print(values.shape)

grid = pv.UniformGrid()
grid.dimensions = np.array(values.shape) + 1
grid.origin = (100, 33, 55.6)  # The bottom left corner of the data set
grid.spacing = (8, 8, 8)  # These are the cell sizes along each axis
# Add the data values to the cell data
grid.cell_data["values"] = values.flatten(order="F")  # Flatten the array!


plotter = pv.Plotter(shape=(1, 2))

# Note that the (0, 0) location is active by default
# load and plot an airplane on the left half of the screen
plotter.add_text("Entorno 1\n", font_size=20)
#plotter.add_mesh(grid, show_edges=True,opacity=0.85, color=True)
plotter.add_mesh(grid, show_edges=True,opacity=0.65)


# load and plot the uniform data example on the right-hand side
plotter.subplot(0, 1)
plotter.add_text("Entorno 2\n", font_size=20)
plotter.add_mesh(grid, show_edges=True,opacity=0.85, color=True)

# Display the window
plotter.show()


