from DistanceMatrix import *
import random
import sys
import math

alphaT = 0.95
alphaIter = 1.2
cities = []
distances = [[]]
temperature = 0
n_iter = 10


class Solution:
    def __init__(self,citiesList,cost):
        self.citiesList = citiesList
        self.cost = cost
    
    def getCitiesList(self):
        return self.citiesList
    
    def getCost(self):
       return self.cost

    def setCost(self,cost):
        self.cost = cost

def fallout(temp):
    global temperature
    temperature = alphaT * temp
    var_n_iter()

def create_initial_solution():
    aux = distances[0]
    it = iter(aux)
    next(it)

    cost = 0
    
    c = aux[0]

    while True:
        try: 
            n = next(it)
            cost += distance(distances,c,n)
            c = n
        except StopIteration:
            break
    return Solution(aux,cost)
    

def max_distance():
    maxDistance = 0
    auxDistances = distances[1]
    for j in auxDistances:
        for k in j:
            if k > maxDistance:
                maxDistance = k

    return maxDistance

def min_distance():
    minDistance = max_distance()
    auxDistances = distances[1]
    for j in auxDistances:
        for k in j:
            if k < minDistance:
                minDistance = k

    return minDistance

def initial_temperature():
    return max_distance() - min_distance()

def getNeighbor():
    global current
    citiesL = current.getCitiesList()

    j = random.randint(2,len(citiesL) - 2)
    i = random.randint(0, j - 2)

    neighbor = list(citiesL)

    aux = reversed(neighbor[i+1:j+1])

    neighbor[i+1:j+1] = aux

    cost = distance(distances,citiesL[i],citiesL[j]) - distance(distances,citiesL[i],citiesL[i+1]) \
         + distance(distances,citiesL[i+1],citiesL[j+1]) - distance(distances,citiesL[j],citiesL[j+1])

    newCost = current.getCost() + cost
    
    return Solution(neighbor,newCost)

def var_n_iter():
    global n_iter
    n_iter = math.ceil(alphaIter * n_iter)

def calc_prob(d):
    print(temperature)
    return math.exp(-1*d/temperature)

# MAIN #

#Leitura do ficheiro e criacao de matrizes
fName = "matrixTeste.txt"
cities = readDistanceMatrix(fName)
distances = createSmallMatrix(cities, ['Atroeira', 'Belmar', 'Cerdeira', 'Douro', 'Encosta', 'Freita', 'Gonta', 'Horta', 'Infantado', 'Jardim', 'Lourel', 'Monte', 'Nelas', 'Oura', 'Pinhal', 'Quebrada', 'Roseiral', 'Serra', 'Teixoso', 'Ulgueira', 'Vilar'])

#Inicializacao do algoritmo
current = create_initial_solution()
best = Solution(current.getCitiesList(),current.getCost())
temperature = initial_temperature()
prob = 1.0

while True:
    for i in range(0,n_iter + 1):
        neighbor = getNeighbor()
        d = neighbor.getCost() - current.getCost()
        
        if d < 0:
            current = Solution(neighbor.getCitiesList(),neighbor.getCost())
            
            if current.getCost() < best.getCost():
                best = Solution(current.getCitiesList(),current.getCost())
       
        else:
            prob = calc_prob(d)
            current = (current,Solution(neighbor.getCitiesList(),neighbor.getCost()))[random.random() < prob]


    if prob < 0.000005:
        break
    fallout(temperature)

print(best.getCitiesList(), best.getCost())

