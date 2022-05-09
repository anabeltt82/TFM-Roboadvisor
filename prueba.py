from abc_problem import ABCProblem
from functions import FUNCTIONS

problem = ABCProblem(bees=10, iteration_number=100, function=FUNCTIONS['michalewicz'])
best_bee = problem.solve()
problem.replay()



""""La funcion que utilizamos con el objetivo de minimizar es:

def michalewicz(x, m=10):
    '''Michalewicz Function
    Parameters
    ----------
        x : list
        m : float
    Returns
    -------
        float
    Notes
    -----
    The parameter m defines the steepness of they valleys and ridges; a larger m leads to a more difficult search. The recommended value of m is m = 10.
    global minimum for 2D: f(x)=-1.8013 at x*=(2.20,1.57)
    bounds: x_i in [0, π] for i=1,..., d
    '''
    d = len(x)
    result = 0
    for i in range(d):
        result -= sin(x[i])*(sin((i+1)*x[i]**2/pi))**(2*m)
    return result

"""