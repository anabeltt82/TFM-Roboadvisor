import numpy as np
from bee_base import BeeBase


class EmployeeBee(BeeBase):
    def explore(self) -> None:
        """
        Explora nuevas fuentes de alimentos desde su propia posición
        """
        self._explore(self._position, self.value)

    @property
    def fitness(self) -> float:
        """
        calculo del fitness. Se utiliza para cálculos de probabilidad
        Devuelve:
            float: fitness
        """

        # Preferimos valores negativos
        if self.value > 0:
            fitness = 1 / (self.value+1)  # cambiar el valor por una constante
        else:
            fitness = np.abs(self.value) + 1

        return fitness