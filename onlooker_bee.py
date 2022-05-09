
from typing import Tuple
from bee_base import BeeBase

class OnlookerBee(BeeBase):
    def explore(self, starting_position: Tuple[float, float], start_value: float) -> None:
        """
        Explore nuevas fuentes de alimentos a partir de la dada
        Args:
            starting_position ([type]): [description]
            start_value (float): [description]
        """
        self._explore(starting_position, start_value) #genera una mejor posicion y se queda con la mejor de las dos