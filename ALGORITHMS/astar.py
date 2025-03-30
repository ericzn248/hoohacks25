from ship import Vector, Location, SHIP_SPEED
from queue import PriorityQueue

[lat, long] = [0, 0]
START = Location(lat,long)

[lat, long] = [1, 1]
DESTINATION = Location(lat,long)
print(START,DESTINATION)
MAX_CURRENT = 0 #TODO

print(START.distance(DESTINATION))

def getH(loc : Location):
    return loc.distance(DESTINATION)/(MAX_CURRENT+SHIP_SPEED) #TODO: add wind?

def getNbrs(loc : Location):
    return [DESTINATION]

def astar(start,dest):
    openSet = PriorityQueue()
    closedSet = set()

    openSet.put((getH(start), 0, start, start))
    path = {start:start}

    while(not openSet.empty()):
        (f,g,loc,parent) = openSet.get()
        closedSet.add(loc)
        path[loc] = parent
        if(loc==dest): break

        for nbr in getNbrs(loc):
            if(nbr in closedSet): continue
            ng = g+loc.costTo(nbr,Vector(0,0),Vector(0,0)) #TODO: replace first vector with wind, second vector with current
            nh = getH(loc)
            nf = ng + nh
            # print(ng)
            openSet.put((nf,ng,nbr,loc))

astar(START,DESTINATION)
    



