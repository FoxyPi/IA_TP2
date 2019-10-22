from DistanceMatrix import *
import random
import sys
import math
import time

alphaT = 0.90
alphaIter = 1.1
cities = []
distances = [[]]
temperature = 0
n_iter = 0
total_iter = 0


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
            cost += distance(distances,c,aux[0])
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
    return -((maxDistance - minDistance) - (second_max_distance(maxDistance) - second_min_distance(minDistance)))/math.log(0.95)

def getNeighbor():
    global current
    citiesL = current.getCitiesList()
    length = len(citiesL)

    j = random.randint(2,length - 1)
    i = random.randint(0, j - 2)

    if i == 0 and j == (length - 1):
        i += 1 

    jplusone = j + 1

    neighbor = list(citiesL)
    

    aux = reversed(neighbor[i+1:jplusone])
    neighbor[i+1:jplusone] = aux

    if jplusone == length:
        jplusone = 0


    cost = distance(distances,citiesL[i],citiesL[j]) - distance(distances,citiesL[i],citiesL[i+1]) \
         + distance(distances,citiesL[i+1],citiesL[jplusone]) - distance(distances,citiesL[j],citiesL[jplusone])

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
citiesL = ['Atroeira', 'Belmar', 'Cerdeira', 'Douro', 'Encosta', 'Freita', 'Gonta', 'Horta', 'Infantado', 'Jardim', 'Lourel', 'Monte', 'Nelas', 'Oura', 'Pinhal', 'Quebrada', 'Roseiral', 'Serra', 'Teixoso', 'Ulgueira', 'Vilar']
distances = createSmallMatrix(cities,citiesL)

#Inicializacao do algoritmo

initialTime = int(round(time.time() * 1000))

current = create_initial_solution()
initialSolution = Solution(current.getCitiesList(),current.getCost())
best = Solution(current.getCitiesList(),current.getCost())
worst = Solution(current.getCitiesList(),current.getCost())
temperature = initial_temperature()
prob = 1.0
finalSolution = 0

n_iter = int(len(citiesL) * (len(citiesL) - 1) / 2)
total_iter += n_iter
print(n_iter)
while True:
    for i in range(0,n_iter + 1):
        neighbor = getNeighbor()
        d = neighbor.getCost() - current.getCost()
        
        if d < 0:
            current = Solution(neighbor.getCitiesList(),neighbor.getCost())
            
            if current.getCost() < best.getCost():
                best = Solution(current.getCitiesList(),current.getCost())
            elif current.getCost() > worst.getCost():
                worst = Solution(current.getCitiesList(),current.getCost())
        else:
            prob = calc_prob(d)
            current = (current,Solution(neighbor.getCitiesList(),neighbor.getCost()))[random.random() < prob]


    if total_iter > 40000:
        finalSolution = current
        break
    fallout(temperature)


finalTime = int(round(time.time() * 1000))

print("TOTAL TIME : " + str(finalTime - initialTime) + "ms \n\n")
print("MELHOR SOLUÇÃO : \n\tPERCURSO: " + str(best.getCitiesList()) + "\n\tCUSTO: " + str(best.getCost()) + "\n")
print("PIOR SOLUÇÃO : \n\tPERCURSO: " + str(worst.getCitiesList()) + "\n\tCUSTO: " + str(worst.getCost()) + "\n")
print("PRIMEIRA SOLUÇÃO : \n\tPERCURSO: " + str(initialSolution.getCitiesList()) + "\n\tCUSTO: " + str(initialSolution.getCost()) + "\n")
print("ULTIMA SOLUÇÃO : \n\tPERCURSO: " + str(finalSolution.getCitiesList()) + "\n\tCUSTO: " + str(finalSolution.getCost()) + "\n")

