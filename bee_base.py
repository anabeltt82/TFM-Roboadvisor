
from typing import Tuple
from coordinate import Coordinate
from levy_flight import levy_flight


class BeeBase(Coordinate):

    def __init__(self, **kwargs) -> None:
        """
        Inicializa una nueva instancia de la clase abeja base
        """
        super().__init__(**kwargs)
        self.__limit = kwargs.get('trials', 3)
        self.__lambda = kwargs.get('lambda', 1.5) #para calculo de la nueva posicion
        self.__alpha = kwargs.get('alpha', 1.) #para calculo de la nueva posicion
        self.__trials = 0
        self.__reset = True

    @property
    def is_reset(self) -> bool:
        """
        Indica si la abeja se reinicia o no.
        Devuelve:
            bool: Verdadero si la abeja se restableció de lo contrario Falso
        """
        return self.__reset

    def reset(self) -> None:
        """
        Resetea la abeja si esta excedió los intentos "trials"
        """
        if self.__trials >= self.__limit:
            self._initialize()
            self.__trials = 0
            self.__reset = True

    def _explore(self, starting_position: Tuple[float, float], start_value: float) -> None:
        """
        Intenta generar una nueva posición y guarda la mejor de las dos
        Args:
            starting_position (Tuple[float, float]): Posicion inicial
            start_value (float): valor de la posicion inicial
        """
        new_pos = levy_flight(starting_position, self.__alpha, self.__lambda, self._random) #nueva posicion
        new_value = self._function(new_pos) #valor de la nueva posicion

        if new_value < start_value: #si el valor es mejor guarda la nueva posicion y establece reset a falso y trials a 0
            self._position = new_pos
            self.__trials = 0
            self.__reset = False
        else:
            self.__trials += 1 #si la nueva posicion no es mejor suma 1 a trials