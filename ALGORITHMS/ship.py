from time import time
import math

class Vector():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dir = math.atan2(y,x)
        self.mag = math.sqrt(x**2+y**2)

class Location():
    def __init__(self, lat, long):
        self.lat = lat
        self.long = long
        self.latr = lat*(math.pi/180)
        self.longr = long*(math.pi/180)
    
    def __eq__(self,loc2):
        return abs(self.lat-loc2.lat)+abs(self.long-loc2.long) < 0.0001 #small error for float calcs
    
    def __hash__(self):
        return hash((round(self.lat, 5), round(self.lon, 5)))
    
    def distance(self, loc2): #gets distance between locations in kilometers
        dlat = abs(loc2.lat-self.lat)
        dlong = abs(loc2.long-self.long)
        hav = math.sin(dlat/2) * math.sin(dlat/2)
        + math.cos(self.latr) * math.cos(loc2.latr) * math.sin(dlong/2) * math.sin(dlong/2)
        c = 2*math.atan2(math.sqrt(hav), math.sqrt(1-hav))
        return 6371*c
    
    def costTo(self, loc2, wind, current): #TODO: return a distance & time
        return 0
        
