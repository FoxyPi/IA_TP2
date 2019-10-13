from DistanceMatrix import *

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

# MAIN #
fName = "matrixTeste.txt"

cities = readDistanceMatrix(fName)
distances = createSmallMatrix(cities, ["Belmar","Freita","Jardim","Quebrada","Vilar"])
create_initial_solution()
best = current
temperature = initial_temperature()

repeat
    for n = 1 to n_iter do
        próximo <- vizinho(corrente)
        d <- distância(próximo) - distância(corrente)
        if d < 0 then
            corrente <- próximo
            if distância(corrente) < distância(melhor) then melhor <- corrente
        else corrente <- próximo apenas com probabilidade exp(-d/T)
    if criterio_de_paragem(...) then retorna melhor
    n_iter <- var_n_iter(n_iter)
    T <- decaimento(T)

print(current,'\n',temperature)