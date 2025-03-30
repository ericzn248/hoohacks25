from ship import Vector, Location, SHIP_SPEED
from queue import PriorityQueue
import xarray as xr
import math
import numpy as np
from time import time
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature



ds = xr.open_dataset('final_data/matched_currents_and_winds000.nc')

LATS = ds.latitude.values
LONGS = ds.longitude.values
CURRENTS_X = ds['uo_interp'].values #m/s
CURRENTS_Y = ds['vo_interp'].values
WINDS_X = ds['u10'].values
WINDS_Y = ds['v10'].values

# CURRENT_DCT = {}
# time1 = time()
# for i in range(len(LATS)):
#     for j in range(len(LONGS)):
#         if(math.isnan(CURRENTS_X[i,j])): continue
#         CURRENT_DCT[(LATS[i],LONGS[j])] = Vector(CURRENTS_X[i,j],CURRENTS_Y[i,j])

# WIND_DCT = {}
# for i in range(len(LATS)):
#     for j in range(len(LONGS)):
#         if(math.isnan(WINDS_X[i,j])): continue
#         CURRENT_DCT[(LATS[i],LONGS[j])] = Vector(WINDS_X[i,j],WINDS_Y[i,j])
# print(f"Python pre-processing time: {time()-time1}s")

MAX_CURRENT_MAG = 0 #m/s 
for i in range(len(LATS)):
    for j in range(len(LONGS)):
        if(math.isnan(CURRENTS_X[i,j])): continue
        if (tmp := CURRENTS_X[i,j]**2+CURRENTS_Y[i,j]**2) > MAX_CURRENT_MAG:
            MAX_CURRENT_MAG = tmp
MAX_CURRENT_MAG = math.sqrt(MAX_CURRENT_MAG)

MAX_WIND_MAG = 0 #m/s 
for i in range(len(LATS)):
    for j in range(len(LONGS)):
        if(math.isnan(WINDS_X[i,j])): continue
        if (tmp := WINDS_X[i,j]**2+WINDS_Y[i,j]**2) > MAX_WIND_MAG:
            MAX_WIND_MAG = tmp
MAX_WIND_MAG = math.sqrt(MAX_WIND_MAG)

HCACHE = {}
def getH(loc: Location, dest: Location):
    if (key := (loc,dest)) in HCACHE: return HCACHE[key]
    mxWind = (uvec := Vector(dest.lat-loc.lat,dest.long-loc.long).unit()) * MAX_WIND_MAG
    mxCurrent = uvec * MAX_CURRENT_MAG
    HCACHE[key] = key[0].costTo(key[1], mxWind, mxCurrent)
    return HCACHE[key]


def getNbrs(loc : Location):
    nbrs = []
    for i in [(-0.25,-0.25),(-0.25,0),(-0.25,0.25),(0,-0.25),(0,0.25),(0.25,-0.25),(0.25,0),(0.25,0.25)]:
        nloc = Location(loc.lat+i[0],loc.long+i[1])
        lat_idx = int(nloc.lat*4)
        long_idx = int(nloc.long*4)
        if math.isnan(CURRENTS_X[lat_idx,long_idx]) or math.isnan(WINDS_X[lat_idx,long_idx]): continue
        nbrs.append((nloc,Vector(CURRENTS_X[lat_idx,long_idx],CURRENTS_Y[lat_idx,long_idx]),
                     Vector(WINDS_X[lat_idx,long_idx],WINDS_Y[lat_idx,long_idx])))
    return nbrs

def constructPath(paths,dest):
    p = [dest]
    loc = dest
    while(paths[loc] != loc):
        loc = paths[loc]
        p.append(loc)
    p = p[::-1]
    timeSum = 0
    for i in range(len(p[1:])):
        tmp = getNbrs(p[i-1])
        for nbr in tmp:
            (nloc, nwind, ncurrent) = nbr
            if nloc == p[i]: 
                break
        timeSum += p[i-1].costTo(nloc, nwind, ncurrent)
    print(f"TOTAL TIME OF ROUTE FOUND: {timeSum}")
    lats = []
    longs = []

    for i in p:
        lats.append(i.lat)
        longs.append(i.long)
    
    # fig, ax = plt.subplots(subplot_kw={"projection": ccrs.PlateCarree()})

    # # Add map features
    # ax.add_feature(cfeature.LAND, edgecolor='black')
    # ax.add_feature(cfeature.OCEAN)
    # ax.add_feature(cfeature.BORDERS, linestyle=':')
    # ax.add_feature(cfeature.COASTLINE)

    # # Plot points on the map
    # ax.plot(lats, longs, marker='o', linestyle='-', color='red', markersize=5, label="Path")

    # # Labels and title
    # plt.title("Overlay Plot on Map")
    # ax.legend()

    # # Show plot
    # plt.show()

    plt.plot(lats, longs, marker='o', linestyle='-', color='r')

    # Labels and title
    plt.xlabel("Latitudes")
    plt.ylabel("Longitudes")
    plt.title("Path Found")

    # Show legend
    plt.legend()

    # Display plot
    plt.show()
    return p

def astar(start,dest):
    nodes_processed = 0
    openSet = PriorityQueue()
    closedSet = set()

    openSet.put((getH(start,dest), 0, start, start))
    path = {start:start}

    while(not openSet.empty()):
        (f,g,loc,parent) = openSet.get()
        if loc in closedSet: continue
        nodes_processed +=1
        # if(nodes_processed %2000 == 0): 
        #     print("2000 processed")
        #     print(f,loc)

        closedSet.add(loc)
        path[loc] = parent
        # print(f"LOC: {loc}")
        if(loc==dest): break

        for nbr in getNbrs(loc):
            (nloc, nwind, ncurrent) = nbr
            if nloc in closedSet: continue
            ng = g+loc.costTo(nloc,nwind,ncurrent)
            nh = getH(loc,dest)
            nf = ng + nh
            # print(ng)
            openSet.put((nf,ng,nloc,loc))
    
    print(constructPath(path,dest))
    print(f"NODES PROCESSED: {nodes_processed}")
    print(len(closedSet))

[lat, long] = [26, -82]
START = Location(lat,long)

[lat, long] = [20, -91.25]
DESTINATION = Location(lat,long)

print(f"START: {START}, DESTINATION: {DESTINATION}")
# print(f"TOTAL DISTANCE: {START.distance(DESTINATION)}")
# print(f"NAIVE MAXIMAL TIME: {START.costTo(DESTINATION, Vector(START.lat-DESTINATION.lat,START.long-DESTINATION.long).unit()*MAX_WIND_MAG, Vector(START.lat-DESTINATION.lat,START.long-DESTINATION.long).unit()*MAX_CURRENT_MAG)}")

time1 = time()
astar(START,DESTINATION)
print(f"PROCESSING TIME TAKEN: {time()-time1}")