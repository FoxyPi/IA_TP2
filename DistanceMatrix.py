# reads a distance matrix (composed of a list of cities and the matrix itself)
# given file name fName
def readDistanceMatrix(fName):

    cities = []
    distances = []
    
    with open(fName, 'r') as f:
        i=0
        for line in f:
            if i == 0:
                l = [line.rstrip().split()]
                city = l[0][1]
                cities.append(city)
            else:
                row = []
                l = [line.rstrip().split()]
                city = l[0][0]
                cities.append(city)
                j = 1
                while j<= i:
                    row.append(l[0][j])
                    j += 1
                distances.append(row)
            i += 1
    f.close()
    
    dm = []
    dm.append(cities)
    dm.append(distances)
    return dm

# creates a distance matrix given another, m, and a list containing a subset
# of the cities occurring in m
def createSmallMatrix(m,clist):

    cities = clist
    distances = []
    
    for c in range(1,len(cities)):
        row = []
       
        for v in range(0,c):
            row.append(distance(m,cities[c],cities[v]))
        
        distances.append(row)
    
    dm = []
    dm.append(cities)
    dm.append(distances)
    return dm
    
# Returns the distance between two cities c1 and c2 given distance matrix m
def distance (m,c1,c2):
    index1 = m[0].index(c1)
    index2 = m[0].index(c2)
    
    if index1<index2:
        return int(m[1][index2-1][index1])
    else:
        return int(m[1][index1-1][index2])
        
# Shows the distance matrix m
def showDistances(m):
    cities = '         '
    for i in range(0,len(m[0])-1):
        cities = cities + ' ' + "{:>9}".format(m[0][i])
    print(cities)
    for i in range(0,len(m[1])):
        row = "{:>9}".format(m[0][i+1])
        for j in range(0,len(m[1][i])):
            row = row + ' ' + "{:>9}".format(m[1][i][j])
        print(row)