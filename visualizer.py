
import numpy as np

from base_visualizer import BaseVisualizer
"""abejas empleadas como marcadores rojos"""
"""abejas espectadoras se visualizan como marcadores azules"""
"""Las mejores abejas de todas las iteraciones (anteriores) se indican con marcadores amarillos"""
"""Cuando una abeja empleada excedió sus intentos máximos, a la abeja se le asigna una nueva posición aleatoria. Esto se visualiza mediante una transición gris oscuro """
"""Se omite la transición de espectadora a empleada (las abejas espectadoras toman la posición de una abeja empleada al azar)"""

class Visualizer(BaseVisualizer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        ax = self._fig.gca(label='BaseAxis')
        self.__best_bees_artist, = ax.plot([], [], 'o', color='#FFA500' if self._dark else '#ffff00', ms=6) #naranja sino amarillo las mejores
        self.__best_bees = [[], []]

        self.__onlooker_bee_positions = [] #abejas espectadoras
        self.__onlooker_bees_artist, = ax.plot([], [], 'o', color='darkblue' if self._dark else 'blue', ms=6)

        self._abandon_map = []

    def add_data(self, **kwargs) -> None:
        """añadimos los datos a la visualización/tablero"""
        employee_positions, employee_reset = zip(*[(bee.position, bee.is_reset) for bee in kwargs['employee_bees']])
        kwargs['positions'] = employee_positions
        super().add_data(**kwargs)

        # Indica si la abeja se generó en esta iteración o no
        self._abandon_map.append(np.array(employee_reset))

        # tratamiento posiciones del observador
        onlooker_positions = [bee.position for bee in kwargs['onlooker_bees']]

        self.__onlooker_bee_positions.append(np.transpose(onlooker_positions))

        # tratamiento de las mejores abejas
        x_pos, y_pos = kwargs['best_position']
        self.__best_bees[0].append(x_pos)
        self.__best_bees[1].append(y_pos)

        # inicializacion
        if len(self.__onlooker_bee_positions) == 1:
            self._abandon_map.append(np.array(employee_reset))
            self.__onlooker_bee_positions.append(np.transpose(onlooker_positions))
            self.__best_bees[0].append(x_pos)
            self.__best_bees[1].append(y_pos)

    def _init(self):
        """"Inicializamos la visualización de las abejas"""
        base_artists = super()._init()
        self.__best_bees_artist.set_data([], [])
        self.__onlooker_bees_artist.set_data([], [])

        return [*base_artists, self.__best_bees_artist, self.__onlooker_bees_artist]

    def _animate(self, i: int, frames: int):
        #pintamos las transiciones de las abejas
        if self._index < len(self._abandon_map)-1:
            # Colorea de un color diferente cuando la abeja empleada se resetea
            self._vel_color = np.where(self._abandon_map[self._index+1], '#373737', '#CFCFCF') #gris oscuro sino gris claro
        base_artists = super()._animate(i, frames)

        self.__best_bees_artist.set_data(self.__best_bees[0][:self._index], self.__best_bees[1][:self._index])
        self.__best_bees_artist.set_markersize(self._marker_size)

        x_pos, y_pos = self.__onlooker_bee_positions[self._index]
        self.__onlooker_bees_artist.set_data(x_pos, y_pos)
        self.__onlooker_bees_artist.set_markersize(self._marker_size)

        return [*base_artists, self.__best_bees_artist, self.__onlooker_bees_artist]