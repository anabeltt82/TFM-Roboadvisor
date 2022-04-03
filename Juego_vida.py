import pyvista as pv
import numpy as np
from sympy import true
import time



def randomGrid(N,M,vals):
    "" "Genero un entorno aleatorio" ""    
    values = np.random.choice(vals, N * M, p=[0.2, 0.8]).reshape(N, M, 1)    
    return values

def update(grid, N, M, ON, OFF):
    """
         Actualizo el grid de acuerdo con las reglas del juego.
         : grid: coordenadas
         : N: tamaño2
         : devolver: el nuevo grid
    """
    newGrid = grid.copy()

    print(grid)
    for i in range(N):
        for j in range(M):
            # Calculo la suma de ocho celdas circundantes (0, 255), calcul cuántas vidas hay alrededor
            #% N se usa para considerar las condiciones de contorno
            total = int((grid[i, (j - 1) % M] + grid[i, (j + 1) % M] +
                         grid[(i - 1) % N, j] + grid[(i + 1) % N, j] +
                         grid[(i - 1) % N, (j - 1) % M] + grid[(i - 1) % N, (j + 1) % M] +
                         grid[(i + 1) % N, (j - 1) % M] + grid[(i + 1) % N, (j + 1) % M]) / ON)
            # Reglas de actualización de la vida
            if grid[i, j] == ON: #'viva'
                if (total < 2) or (total > 3):
                    newGrid[i, j] = OFF #muere
            else:
                if total == 3: #si esta muerta y tiene tres vecinas vivas nace
                    newGrid[i, j] = ON
       
    return newGrid


def main():
    # Establecer el tamaño del entorno
    N = 177
    M = 136
    i = 0
    ON = 255
    OFF = 0
    vals = [ON, OFF]
    
    # Establecer el tiempo de intervalo de actualización predeterminado ms
    updateInterval = 1
    
    # Creo aleatoriamente el primer entorno
    grid = np.array([])
    grid = randomGrid(N,M,vals)
    #print(grid.shape)
    tablero = pv.UniformGrid()
    tablero.dimensions = np.array(grid.shape) + 1
    tablero.spacing = (1, 1, 1)  # tamaño de los cuadros
    
    tablero.cell_data["values"] = grid.flatten(order="F") # aplano el array

    plotter = pv.Plotter(shape=(1, 1))
    # Cambio la posición, foco y the up vector de la visualización
    plotter.camera_position = [(110.24222162420345, 34.29405443814952, 292.28709395107853),(88.5, 68.0, 0.5),(0.012287372804874503, -0.9932143411475222, -0.11564727843078623)]
    plotter.add_text("El juego de la vida\n", font_size=20)
    plotter.add_mesh(tablero, show_edges=True)
    plotter.show(interactive_update=True)
    
    # Animación
    
    for i in range(5, 1000):
        # establezco el crono
        time.sleep(updateInterval)
        
        #actualizo la matriz con las normas del juego
        grid = update(grid, N, M, ON, OFF)
       
        tablero.cell_data["values"] = grid.flatten(order="F") # Flatten del array
        pos = plotter.camera_position
        print(pos)
        # repinto
        plotter.update()
  
   
    
# Ejecutar
if __name__ == '__main__':
    main()