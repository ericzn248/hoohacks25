from ship import Vector, Location, SHIP_SPEED
from queue import PriorityQueue

[lat, long] = [0, 0]
START = Location(lat,long)

[lat, long] = [1, 1]
DESTINATION = Location(lat,long)
print(START,DESTINATION)
MAX_CURRENT = 0 #TODO

print(START.distance(DESTINATION))
print(START.costTo(DESTINATION, Vector(0,0), Vector(0,0)))

def getH(loc : Location):
    return loc.distance(DESTINATION)/(MAX_CURRENT+SHIP_SPEED) #TODO: add wind?

def getNbrs(loc : Location):
    return [(DESTINATION,Vector(0,0),Vector(0,0))]
    nbrs = []
    for i in [(-0.25,-0.25),(-0.25,0),(-0.25,0.25),(0,-0.25),(0,0.25),(0.25,-0.25),(0.25,0),(0.25,0.25)]:
        nloc = Location(loc.lat+i[0],loc.long+i[1])
    return nbrs

def constructPath(paths,dest):
    p = [dest]
    loc = dest
    while(paths[loc] != loc):
        loc = paths[loc]
        p.append(loc)
    return p[::-1]


def astar(start,dest):
    openSet = PriorityQueue()
    closedSet = set()

    openSet.put((getH(start), 0, start, start))
    path = {start:start}

    while(not openSet.empty()):
        (f,g,loc,parent) = openSet.get()
        closedSet.add(loc)
        path[loc] = parent
        # print(f"LOC: {loc}")
        if(loc==dest): break

        for nbr in getNbrs(loc):
            (nloc, nwind, ncurrent) = nbr
            if(nloc in closedSet): continue
            ng = g+loc.costTo(nloc,nwind,ncurrent) #TODO: replace first vector with wind, second vector with current
            nh = getH(loc)
            nf = ng + nh
            # print(ng)
            openSet.put((nf,ng,nloc,loc))
    
    print(constructPath(path,dest))

    

astar(START,DESTINATION)
    



