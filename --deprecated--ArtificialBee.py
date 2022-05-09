import numpy as np
from random import uniform


def roulleteWheel(swarm):
    """revisa toda la colmena en busca de una cantidad de nectar elegida al azahar entre 0 y el maximo recolectado por la colmena.           
        Args:
            swarm : colmena
        Devuelve:
        Abeja con acumulación de nectar mayor que el objetivo elegido al azahar
        """   
    max = sum([b.cantidad_nectar for b in swarm])
    objetivo = uniform(0,max) #elegimios un objetivo de manera aleatoria entre 0 y el maximo de nectar
    nectar_actual = 0
    for b in swarm:
        nectar_actual += b.cantidad_nectar
        if nectar_actual > objetivo:
            return b
        
        
class Abeja():
    cycles=0
    cycleLimit = 50
    tipo_Abeja = None
    dimensiones = None
    cantidad_nectar = 0
    posicion = []
    area_busqueda = []
    
    
    history = []
    ExtraElitist=True #con True forzamos exploración

    def calcula_cantidad_nectar(self, posicion=None): 
        """Evalua la cantidad de nectar de una posicion.
            Si no pasamos una posicion evaluará la posicion de la abeja
        Args:
            posicion : Posicion de la abeja            
        """        
        if posicion==None:
            posicion=self.posicion

        return self.area_busqueda[tuple(posicion)]

    def __init__(self, area_busqueda, tipo_Abeja='empleada'):
        """Inicializa en objeto abeja.

        Args:
            area_busqueda: Area de busqueda
            tipo_Abeja: Por defecto empleado
        """
        self.tipo_Abeja = tipo_Abeja
        numero_dim = area_busqueda.ndim
        self.dimensiones = area_busqueda.shape
        posicion_aleatoria_abeja = []
        #Establecemos una posicion aleatoria para la nueva abeja
        for d in self.dimensiones:
            posicion_aleatoria_abeja.append(np.random.randint(d))
        self.posicion = list(posicion_aleatoria_abeja) #añadimos la posicion aleatoria a su lista de posiciones
        self.area_busqueda = area_busqueda #le proporcionamos el total del area de busqueda
        self.cantidad_nectar = self.calcula_cantidad_nectar() #calcula el nectar de la posicion aleatoria 
        
        
    def establece_tipo_abeja(self, tipo_Abeja):
        """Establece el tipo de abeja.

        Args:
            tipo_Abeja: Tipo de abeja            
        """
        self.tipo_Abeja=tipo_Abeja
    

    def actualiza_ciclos(self, reset=False):
        """Actualiza el numero de ciclos de la abeja.

        Args:
            reset: por defecto a falso, si true resetea el numero de ciclos de la abeja            
        """
        if reset:
            cycles=0
            return
        self.cycles+=1
    
    def observar(self, population):
        """Las abejas espectadoras observarán a los mejores empleados e intentarán mejorar esa fuente de alimento. 
        
        Args:
            population: colmena       
        """
        b = roulleteWheel(population) #elegimos Abeja con acumulación de nectar mayor que el objetivo elegido al azahar
        if b.cantidad_nectar > self.cantidad_nectar: #si la abeja asi elegida tiene más nectar que la espectadora 
            self.posicion = b.posicion #la espectadora se desplaza a la posición de la empleada objetivo
            self.cantidad_nectar = self.calcula_cantidad_nectar() #calculamos la cantidad de nectar
        return
    
    def area_de_exploracion(self):#, population):
        """Si ExtraElitist = True buscará, prevalece la exploracion y moveremos las abejas a nuevas posiciones 
        
        Args:
                  
        """
        new_posicion = []
        phi = uniform(0,1)
        
        scoutedposicion = []
        for d in self.dimensiones:
            scoutedposicion.append(int(phi*d))
        if (self.ExtraElitist) and (self.calcula_cantidad_nectar()>self.cantidad_nectar):
            self.posicion = list(scoutedposicion)
            self.cantidad_nectar=self.calcula_cantidad_nectar()
        return
    def dance(self):
        """Zona de danza"""
        #genera una nueva solución
        phi = uniform(-1,1)
        #selecciona un candidato al azahar
        posicion_aleatoria_candidato = []
        #toma posicion aleatoria de una abeja
        for d in self.dimensiones:
            posicion_aleatoria_candidato.append(np.random.randint(d))
            
        candidateSolution = []
        
        for p,d,max_ in zip(self.posicion, posicion_aleatoria_candidato, self.dimensiones):

            v = int(p + phi*(p) * (p-d))

            if v<0:
                v=abs(v)%max_
            elif v>(max_-1): #remove hardcode
                v=v%max_
            candidateSolution.append(v)
        #Calcula la cantidad de nectar de la nueva posicion
        cantidad_nectar_candidato = self.calcula_cantidad_nectar(posicion=candidateSolution)
        #cantidad_nectar_candidato = self.area_busqueda[tuple(candidateSolution)]
        if cantidad_nectar_candidato>self.cantidad_nectar:
            self.cantidad_nectar = cantidad_nectar_candidato
            self.posicion = list(candidateSolution)
            
        self.history.append(self.cantidad_nectar)
        #print(self.posicion, self.nectarAmount)
        
    def shouldScout(self):
        #print(self.cycles)
        if self.cycles>self.cycleLimit:         
            if np.average(self.history[-50:])==self.history[-1:]:
                #print("SCOUTS")
                return True
        return False
    
    def giveNectar(self):
        return (self.posicion, self.cantidad_nectar)
 