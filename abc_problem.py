"""basandonos en la clase abstracta problem definimos el problema concreto a resolver"""
from copy import deepcopy
from functools import reduce


from employee_bee import EmployeeBee
from onlooker_bee import OnlookerBee
from visualizer import Visualizer
from problem_base import ProblemBase


class ABCProblem(ProblemBase):
    

    def __init__(self, **kwargs):
        """
        Inicializa una nueva instancia de la clase ABCProblem
        """
        super().__init__(**kwargs)
        self.__iteration_number = kwargs['iteration_number']
        self.__employee_bees = [
            EmployeeBee(**kwargs, bit_generator=self._random)
            for _ in range(kwargs['bees'])
        ]

        self.__onlooker_bees = [
            OnlookerBee(**kwargs, bit_generator=self._random)
            for _ in range(kwargs['bees'])
        ]

        self._visualizer = Visualizer(**kwargs)

    def solve(self):
        """
        Resuelve el ABCProblem
        """
        best = min(self.__employee_bees + self.__onlooker_bees, key=lambda bee: bee.value) #coge el menor valor de todos
        self._visualizer.add_data(employee_bees=self.__employee_bees, onlooker_bees=self.__onlooker_bees, best_position=best.position) #pintamos en el juego
        #print("abejas pintadas")
        for iteration in range(self.__iteration_number):
            # Fase empleado            
            for bee in self.__employee_bees:
                bee.explore()

            # Calcule los valores y probabilidades de fitness de las abejas empleadas
            overall_fitness = reduce(lambda acc, curr: acc + curr.fitness, self.__employee_bees, 0)
            employee_bees_fitness_probs = [bee.fitness/overall_fitness for bee in self.__employee_bees] #calculamos las probabilidades en funcion del fitness general

            # Elija las posiciones de las abejas empleadas proporcionales a su fitness
            choices = self._random.choice(self.__employee_bees, size=len(self.__employee_bees), p=employee_bees_fitness_probs)

            # Fase observadores
            #print("onloker")
            # Explore nuevas fuentes de alimentos basadas en las fuentes de alimentos de los empleados elegidos
            for bee, choice in zip(self.__onlooker_bees, choices):
                bee.explore(choice.position, choice.value)

            # Fase Scout            
            for bee in self.__employee_bees + self.__onlooker_bees:
                bee.reset()

            #Actualizamos la mejor fuente de alimento (minimo entre empleados + observadores)
            print("update best food source")
            current_best = min(self.__employee_bees + self.__onlooker_bees)
            if current_best < best:
                best = deepcopy(current_best)
                print("Interacción " , iteration+1 , " Encontrada una nueva mejor solución= ", best.value , " en la posición= ", best.position)

            # actualizamos la vista            
            self._visualizer.add_data(employee_bees=self.__employee_bees, onlooker_bees=self.__onlooker_bees, best_position=best.position)

        return best