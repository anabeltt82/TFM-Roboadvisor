"""definimos nuestro entorno """
from typing import Iterable, Tuple

import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.cm import get_cmap
import numpy as np

from visualizer_base import VisualizerBase


class BaseVisualizer(VisualizerBase):
    def __init__(self, **kwargs):
        self.__lower_boundary = kwargs.get('lower_boundary', 0.)
        self.__upper_boundary = kwargs.get('upper_boundary', 4.)
        self.__iteration_number = kwargs.get('iteration_number', 10)
        self.__intervals = self.__iteration_number + 2  #punto de partida y de final
        self.__interval_ms = kwargs.get('interval', 1000)
        self.__continuous = kwargs.get('continuous', False)
        self._dark = kwargs.get('dark', False)

        self.__function = kwargs['function']

        self._marker_size = 0
        self._index = 0
        self._vel_color = '#CFCFCF'
        self._marker_color = '#0078D7' if self._dark else '#FF0000'
        self._marker_colors = np.empty(0)

        self._positions = []
        self._velocities = []
        self.__frame_interval = 50  # ms

        if self._dark:
            plt.style.use('dark_background')

        x = np.linspace(self.__lower_boundary, self.__upper_boundary, 800)
        y = np.linspace(self.__lower_boundary, self.__upper_boundary, 800)
        X, Y = np.meshgrid(x, y)
        z = self.__function([X, Y])

        self._fig = plt.figure()

        ax = self._fig.add_subplot(1, 1, 1, label='BaseAxis')
        cs = ax.contourf(X, Y, z, cmap=get_cmap('inferno' if self._dark else 'PuBu_r'))
        self._fig.colorbar(cs)

        # Trazar todas las posiciones de partículas
        self.__particles = ax.scatter([], [], marker='o', zorder=2)

        # Trazar todas las velocidades
        self.__particle_vel = ax.quiver([], [], [], [], angles='xy', scale_units='xy', scale=1)

        self.__rectangle = plt.Rectangle([self.__lower_boundary, self.__lower_boundary],
                                         self.__upper_boundary-self.__lower_boundary,
                                         self.__upper_boundary-self.__lower_boundary,
                                         ec='none', lw=2, fc='none')
        ax.add_patch(self.__rectangle)

    def add_data(self, **kwargs) -> None:
        positions: Iterable[Tuple[float, float]] = kwargs['positions']

        self._positions.append(np.transpose(positions))

        if len(self._positions) == 1:
            # Primera posicion inanimada
            self._positions.append(np.transpose(positions))

        # Calcular en el tiempo t la velocidad para el paso t-1
        self._velocities.append(self._positions[-1] - self._positions[-2])

    def replay(self, **kwargs):
        # sobreescribimos la velocidad a ceros
        self._velocities.append(np.zeros(self._velocities[-1].shape))

        # Cantidad de fotogramas a reproducir teniendo en cuenta que un intervalo debe durar __interval ms.
        frames = int(self.__intervals*self.__interval_ms/self.__frame_interval)

        # iteration_number+1 para el marco de inicialización
        _ = animation.FuncAnimation(self._fig, self._animate, frames=frames, interval=self.__frame_interval,
                                    blit=True, init_func=self._init, repeat=self.__continuous, fargs=[frames])

        plt.show()
        

    def _init(self):
        """
        Función de inicio para animaciones. Solo se usa para FuncAnimation
        """
       # self.__particles.set_offsets([[]])
        self._marker_colors = np.full(len(self._positions[0][0]), self._marker_color)  # Creamos el array del tamaño correcto
        self.__particle_vel.X = []
        self.__particle_vel.Y = []
        self.__particle_vel.XY = []
        self.__particle_vel.U = []
        self.__particle_vel.V = []

        self.__rectangle.set_edgecolor('none')

        return self.__particles, self.__rectangle, self.__particle_vel

    def _animate(self, i: int, frames: int):
        """
         Función de animacion para animaciones. Solo se usa para FuncAnimation
        """

        self._marker_size = int(50 * self._fig.get_figwidth()/self._fig.dpi)
        self.__rectangle.set_edgecolor('k')
        ax = self._fig.gca(label='BaseAxis')

        # Obtener el índice de los datos actuales para mostrar
        self._index = int(np.floor(i / (frames/self.__intervals)))

        self._fig.canvas.set_window_title(f'Iteration {np.minimum(self._index, self.__iteration_number)}/{self.__iteration_number}')

        # Calcular la escala a aplicar a los datos para generar una visualización más dinámica
        scale = i / (frames/self.__intervals) - self._index

        # Calcular la posición y la velocidad a escala
        pos = self._positions[self._index]
        vel = self._velocities[self._index]
        pos_scaled = np.clip(pos + scale * vel, a_min=self.__lower_boundary, a_max=self.__upper_boundary)
        vel_scaled = (1-scale)*vel

        # Actualizar la posición de la partícula
        self.__particles.set_offsets(np.transpose(pos_scaled))
        self.__particles.set_sizes(np.full(len(pos_scaled[0]), self._marker_size**2))
        self.__particles.set_color(self._marker_colors)

        # Actualizo las velocidades
        self.__particle_vel = ax.quiver(pos_scaled[0], pos_scaled[1], vel_scaled[0], vel_scaled[1], angles='xy', scale_units='xy', scale=1, color=self._vel_color, width=self._marker_size*0.001)

        return self.__particles, self.__rectangle, self.__particle_vel