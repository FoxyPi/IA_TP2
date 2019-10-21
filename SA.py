from DistanceMatrix import *
import random
import sys
import math

alphaT = 0.95
alphaIter = 1.01
cities = []
distances = [[]]
temperature = 0
total_iter = 0
n_iter = 20

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
    global total_iter
    temperature =  alphaT*temp
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
            cost += distance(distances,c,aux[0])
            break
    return Solution(aux,cost)
    
def shuffleSolution(citiesList):
    it = iter(citiesList)
    next(it)

    cost = 0

    c = citiesList[0]

    while True:
        try:
            n = next(it)
            cost += distance(distances,c,n)
            c = n
        except StopIteration:
            cost += distance(distances,c,citiesList[0])
            break
    return Solution(citiesList,cost)


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

def second_max_distance(max):
    maxDistance = 0
    auxDistances = distances[1]
    for j in auxDistances:
        for k in j:
            if k > maxDistance and k < max:
                maxDistance = k

    return maxDistance


def second_min_distance(min):
    minDistance = max_distance()
    auxDistances = distances[1]
    for j in auxDistances:
        for k in j:
            if k < minDistance and k > min:
                minDistance = k

    return minDistance

def initial_temperature():
    maxDistance = max_distance()
    minDistance = min_distance()
    return (maxDistance - minDistance) + (second_max_distance(maxDistance) - second_min_distance(minDistance))



def getNeighbor(current):
    citiesL = list(current.getCitiesList())
    length = len(citiesL)

    i = random.randint(0,length - 1)

    neighbor = citiesL

    if i >= length - 2:
        j = random.randint((i+2) % length, (i - 2))
    else:
        j = random.randint((i + 2), (i + length) - 2)


    j = j % length

    if (i+1) % length < j:
        aux = reversed(neighbor[(i+1)%length:j+1])
        neighbor[(i+1)%length:j+1] = aux
    else:
        aux = reversed(neighbor[(j + 1):(i+1)])
        neighbor[(j+1):(i+1)] = aux

    cost = distance(distances,citiesL[i],citiesL[j]) - distance(distances,citiesL[i],citiesL[(i+1)%length]) \
         + distance(distances,citiesL[(i+1)%length],citiesL[(j+1)%length]) - distance(distances,citiesL[j],citiesL[(j+1)%length])

    newCost = current.getCost() + cost

    return Solution(neighbor,newCost)

def var_n_iter():
    global n_iter
    global total_iter
    n_iter = math.ceil(alphaIter * n_iter)
    total_iter += n_iter

def calc_prob(d):
    return math.exp(-1*d/temperature)

# MAIN #

#Leitura do ficheiro e criacao de matrizes


fName = "matrixTeste.txt"
cities = readDistanceMatrix(fName)
citiesList = ['Atroeira', 'Belmar', 'Cerdeira', 'Douro', 'Encosta', 'Freita', 'Gonta', 'Horta', 'Infantado', 'Jardim', 'Lourel', 'Monte', 'Nelas', 'Oura', 'Pinhal', 'Quebrada', 'Roseiral', 'Serra', 'Teixoso', 'Ulgueira', 'Vilar']
distances = createSmallMatrix(cities, citiesList)
#distances = createSmallMatrix(cities, ["Atroeira", "Douro", "Pinhal", "Teixoso", "Ulgueira", "Vilar"])

#Inicializacao do algoritmo
current = create_initial_solution()
best = Solution(current.getCitiesList(),current.getCost())
temperature = initial_temperature()
prob = 1.0

print(getNeighbor(current).getCitiesList())
while True:
    for i in range(n_iter + 1):
        neighbor = getNeighbor(current)
        d = neighbor.getCost() - current.getCost()
        
        if d < 0:
            current = Solution(neighbor.getCitiesList(),neighbor.getCost())
            
            if current.getCost() < best.getCost():
                best = Solution(current.getCitiesList(),current.getCost())

        else:
            prob = calc_prob(d)
            current = (current,Solution(neighbor.getCitiesList(),neighbor.getCost()))[random.random() <= prob]

    if temperature < 1:
        break
    fallout(temperature)

    random.shuffle(citiesList)
    current = shuffleSolution(citiesList)

print(best.getCitiesList(), "\n" + str(best.getCost()))

