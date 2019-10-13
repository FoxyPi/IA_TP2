from DistanceMatrix import *
import random

alpha = 0.9
cities = []
distances = [[]]
current = []
best = []
temperature = 0

def fallout(temp):
    global temperature
    temperature = alpha * temp

def create_initial_solution():
    global current 
    current = distances[0]

def initial_temperature():
    auxDistances = distances[1]
    maxDistance = 0
    for j in auxDistances:
        for k in j:
            if k > maxDistance:
                maxDistance = k
    
    return maxDistance

def neighbor():
    global current

    j = random.randint(2,len(current) - 2)
    i = random.randint(0, j - 2)

    print("j : " + str(j))
    print("i : " + str(i))

    neighbor = list(current)

    aux = reversed(neighbor[i+1:j+1])

    neighbor[i+1:j+1] = aux

    return neighbor



# MAIN #
fName = "matrixTeste.txt"

cities = readDistanceMatrix(fName)
distances = createSmallMatrix(cities, ["Belmar","Freita","Jardim","Quebrada","Vilar"])
create_initial_solution()
best = current
temperature = initial_temperature()
neighbor = neighbor()

print("CURRENT : " + str(current))
print ("NEIGHBOR: " + str(neighbor))