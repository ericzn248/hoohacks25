from ship import Vector, Location, SHIP_SPEED
from queue import PriorityQueue

[lat, long] = [0, 0]
START = Location(lat,long)

[lat, long] = [0, 0]
DESTINATION = Location(lat,long)
MAX_CURRENT = 0

def getH(loc : Location):
    return loc.distance(DESTINATION)/(MAX_CURRENT+SHIP_SPEED) #add wind?

def getNbrs(loc : Location):
    return []

def astar(start,dest):
    openSet = PriorityQueue()
    closedSet = set()

    openSet.put((getH(START), 0, START, START))
    path = {START:START}

    while(not openSet.empty()):
        (f,g,loc,parent) = openSet.get()
        closedSet.add(loc)
        path[loc] = (parent.lat,parent.long)
        if(loc==DESTINATION): break
        
        for nbr in getNbrs(loc):
            if(nbr in closedSet): continue
            ng = g+loc.costTo(nbr)
            nh = getH(loc)
            nf = ng + nh
            openSet.put((nf,ng,nbr,loc))

astar(START,DESTINATION)
    



