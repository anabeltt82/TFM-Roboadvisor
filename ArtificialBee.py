import numpy as np

from copy import deepcopy
from abc import ABCMeta
from six import add_metaclass


@add_metaclass(ABCMeta)
class ArtificialBee(object):

    TRIAL_INITIAL_DEFAULT_VALUE = 0
    INITIAL_DEFAULT_PROBABILITY = 0.0

    def __init__(self, obj_function):
        self.pos = obj_function.custom_sample()
        self.obj_function = obj_function
        self.minf = obj_function.minf
        self.maxf = obj_function.maxf
        self.fitness = obj_function.evaluate(self.pos)
        self.trial = ArtificialBee.TRIAL_INITIAL_DEFAULT_VALUE
        self.prob = ArtificialBee.INITIAL_DEFAULT_PROBABILITY

    def evaluate_boundaries(self, pos):
        if (pos < self.minf).any() or (pos > self.maxf).any():
            pos[pos > self.maxf] = self.maxf
            pos[pos < self.minf] = self.minf
        return pos

    def update_bee(self, pos, fitness):
        if fitness <= self.fitness:
            self.pos = pos
            self.fitness = fitness
            self.trial = 0
        else:
            self.trial += 1

    def reset_bee(self, max_trials):
        if self.trial >= max_trials:
            self.__reset_bee()

    def __reset_bee(self):
        self.pos = self.obj_function.custom_sample()
        self.fitness = self.obj_function.evaluate(self.pos)
        self.trial = ArtificialBee.TRIAL_INITIAL_DEFAULT_VALUE
        self.prob = ArtificialBee.INITIAL_DEFAULT_PROBABILITY
        
class EmployeeBee(ArtificialBee):
    
    def explore(self, max_trials):
        if self.trial <= max_trials:
            component = np.random.choice(self.pos)
            phi = np.random.uniform(low=-1, high=1, size=len(self.pos))
            n_pos = self.pos + (self.pos - component) * phi
            n_pos = self.evaluate_boundaries(n_pos)
            n_fitness = self.obj_function.evaluate(n_pos)
            self.update_bee(n_pos, n_fitness)

    def get_fitness(self):
        return 1 / (1 + self.fitness) if self.fitness >= 0 else 1 + np.abs(self.fitness)

    def compute_prob(self, max_fitness):
        self.prob = self.get_fitness() / max_fitness
        
class OnLookerBee(ArtificialBee):
    
    def onlook(self, best_food_sources, max_trials):
        candidate = np.random.choice(best_food_sources)
        self.__exploit(candidate.pos, candidate.fitness, max_trials)

    def __exploit(self, candidate, fitness, max_trials):
        if self.trial <= max_trials:
            component = np.random.choice(candidate)
            phi = np.random.uniform(low=-1, high=1, size=len(candidate))
            n_pos = candidate + (candidate - component) * phi
            n_pos = self.evaluate_boundaries(n_pos)
            n_fitness = self.obj_function.evaluate(n_pos)

            if n_fitness <= fitness:
                self.pos = n_pos
                self.fitness = n_fitness
                self.trial = 0
            else:
                self.trial += 1