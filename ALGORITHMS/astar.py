from ship import Vector, Location

openSet = set()
closedSet = set()

[lat, long] = [0, 0]
start = Location(lat,long)

[lat, long] = [0, 0]
destination = Location(lat,long)

openSet.add(start)
