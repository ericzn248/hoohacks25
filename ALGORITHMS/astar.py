from ALGORITHMS.ship import Vector, Location
from queue import PriorityQueue
import xarray as xr
import math
import numpy as np
from time import time
import matplotlib.pyplot as plt
import tkinter

ds = xr.open_dataset('final_data/matched_currents_and_winds000.nc')

LATS = ds.latitude.values
LONGS = ds.longitude.values
CURRENTS_X = ds['uo_interp'].values #m/s
CURRENTS_Y = ds['vo_interp'].values
WINDS_X = ds['u10'].values
WINDS_Y = ds['v10'].values

# CURRENT_DCT = {} #can potentially pre-process but kinda slow
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

# lts = [] #for debugging, displayed inputted non-nan winds/currents
# lngs = []
# for i in range(len(LATS)):
#     for j in range(len(LONGS)): 
#         if(math.isnan(WINDS_X[i,j]) or math.isnan(CURRENTS_X[i,j]) or math.isnan(WINDS_Y[i,j]) or math.isnan(CURRENTS_Y[i,j])): continue
#         lts.append(LATS[i])
#         lngs.append(LONGS[j])

# plt.plot(lngs, lts, marker='o', linestyle='-', color='r')

# # Labels and title
# plt.ylabel("Latitudes")
# plt.xlabel("Longitudes")
# plt.title("Non-nans")

# # Display plot
# plt.show()

HCACHE = {}
def getH(loc: Location, dest: Location):
    if (key := (loc,dest)) in HCACHE: return HCACHE[key]
    mxWind = (uvec := Vector(dest.lat-loc.lat,dest.long-loc.long).unit()) * MAX_WIND_MAG
    mxCurrent = uvec * MAX_CURRENT_MAG
    HCACHE[key] = key[0].costTo(key[1], mxWind, mxCurrent)
    return HCACHE[key]


def getNbrs(loc : Location):
    nbrs = []
    nlist = [(-0.25,-0.25),(-0.25,0),(-0.25,0.25),(0,-0.25),(0,0.25),(0.25,-0.25),(0.25,0),(0.25,0.25)]
    # nlist = [(-0.5,-0.5),(-0.5,0),(-0.5,0.5),(0,-0.5),(0,0.5),(0.5,-0.5),(0.5,0),(0.5,0.5)]
    for i in nlist:
        nloc = Location(loc.lat+i[0],loc.long+i[1])
        lat_idx = int(nloc.lat*4)+90
        long_idx = int(nloc.long*4)+180
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
    distSum = 0
    for i in range(len(p[1:])):
        tmp = getNbrs(p[i-1])
        for nbr in tmp:
            (nloc, nwind, ncurrent) = nbr
            if nloc == p[i]: 
                break
        distSum += p[i-1].distance(nloc)
        timeSum += p[i-1].costTo(nloc, nwind, ncurrent)
    print(f"TOTAL DISTANCE OF ROUTE FOUND: {distSum}")
    print(f"TOTAL TIME OF ROUTE FOUND: {timeSum}")
    return [p,distSum,timeSum]
    
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

def displayPath(pList,closedSet = set()):
    longs = []
    lats = []
    for i in pList:
        longs.append(i[1])
        lats.append(i[0])
    clongs = []
    clats = []
    for i in closedSet:
        clats.append(i.lat)
        clongs.append(i.long)
    plt.scatter(clongs, clats, marker='o', color='b')
    plt.plot(longs, lats, marker='o', linestyle='-', color='r')

    plt.ylabel("Latitudes")
    plt.xlabel("Longitudes")
    plt.title("Path Found")

    plt.show()

def astar(start,dest):
    time1 = time()
    nodes_processed = 0
    openSet = PriorityQueue()
    closedSet = set()

    openSet.put((getH(start,dest), 0, start, start))
    path = {start:start}

    while(not openSet.empty()):
        (f,g,loc,parent) = openSet.get()
        if loc in closedSet: continue
        nodes_processed +=1
        if(nodes_processed %1000 == 0): 
            print("1000 processed")
            print(f,loc)

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
    
    [pList, distSum, timeSum] = constructPath(path,dest)
    pList = [i.toTuple() for i in pList]
    print(f"NODES PROCESSED: {nodes_processed}")
    print(f"TIME TAKEN TO PROCESS: {time()-time1}")
    # displayPath(pList,closedSet)
    return [pList, distSum, timeSum]

def generate(lat1,long1,lat2,long2):
    st = Location(lat1,long1)
    dest = Location(lat2,long2)

    print(f"START: {st}, DESTINATION: {dest}")
    print(f"TOTAL DISTANCE: {st.distance(dest)}")
    nmt = st.costTo(dest, Vector(st.lat-dest.lat,st.long-dest.long).unit()*MAX_WIND_MAG/2, Vector(st.lat-dest.lat,st.long-dest.long).unit()*MAX_CURRENT_MAG/2)
    print(f"NAIVE MAXIMAL TIME: {nmt}")
    [pList, distSum, timeSum] = astar(st,dest)
    pctIncrease = 100*(1-(timeSum/nmt))
    return pList, pctIncrease


[pList, pctIncrease] = generate(27.5,-83,21,-86.5)
