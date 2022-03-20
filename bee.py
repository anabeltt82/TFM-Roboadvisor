import pyvista
from pyvista import examples


pl = pyvista.Plotter()
pl.import_gltf("./bee_animation_rigged/scene")
pl.set_environment_texture("./bee_animation_rigged/textures/")
pl.camera.zoom(1.7)
pl.show()
block = pyvista.read("./bee_animation_rigged/scene")
mesh = block[0][0][0]
mesh.plot(color='tan', show_edges=True, cpos='xy')