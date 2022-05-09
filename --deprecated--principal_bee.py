import numpy as np
from random import uniform
from ArtificialBee import Abeja

from matplotlib import pyplot as plt

#mock solution space
print("start memory allocation")
area = np.random.rand(200,200)
print(area)
print("memory allocation done")

     
#Inicializa las abejas        
Swarm = []
swarmSize=5
best = []
Runs = 100
minimalRuns = 50
maximumRunsWithoutChange = 30
saveImgs = False
for i in range(swarmSize):
    Swarm.append(Abeja(area)) #Crea tantas abejas como tamaño colmena crea todas como empleadas
    
#start
bestSolutions = []

for i in range(Runs): #durante el numero de ejecuciones establecido

    nectarAmounts = []
    for b in Swarm: #por cada abeja
        nectarAmounts.append(b.giveNectar())
    
    pltarea = area.copy()
    if saveImgs:
        print(i,50*"-")
        
        plt.figure()
        plt.title("Artificial Bee Colony\n"+"Swarm Size = "+str(swarmSize)+", Run = "+str(i))
        plt.imshow(pltarea)
        for n in nectarAmounts:
            plt.plot(n[0][0], n[0][1], "or")
        #plt.show()
        plt.savefig(str(i)+".png")
        plt.close()

    
    bestSolutions.append(sorted(nectarAmounts, key=lambda x: x[1], reverse=True)[0])
    #print(len(bestSolutions))
   
    
    if len(bestSolutions) > minimalRuns and round(np.average([x[1] for x in bestSolutions][-maximumRunsWithoutChange:]),5) == round(bestSolutions[-1][1],5):
        print("End condition satisfied at", len(bestSolutions))
        break
    for b in Swarm:
        b.dance()
        b.observar(Swarm)
        b.actualiza_ciclos()
        if b.shouldScout():
            b.area_de_exploracion()
    
    
print("Best possible solution", np.max(area))
print("Best Solution Found: ", bestSolutions[-1])
#print(bestSolutions.shape())
plt.figure()
plt.xlabel("Migrations")
plt.ylabel("Nectar Amount")
plt.title("Artificial Bee Colony finding best solution")

plt.plot([x[1] for x in bestSolutions])
plt.show()

