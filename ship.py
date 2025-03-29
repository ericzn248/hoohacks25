from time import time
import math

class Vector():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dir = math.atan2(y,x)
        self.mag = math.sqrt(x**2+y**2)

class Location():
    def __init__(self, lat, long, wind, current):
        self.lat = lat
        self.long = long
        self.wind = wind
        self.latr = lat*(math.pi/180)
        self.longr = long*(math.pi/180)
        self.current = current
    
    def distance(self, loc2): #gets distance between locations in kilometers
        dlat = abs(loc2.lat-self.lat)
        dlong = abs(loc2.long-self.long)
        hav = math.sin(dlat/2) * math.sin(dlat/2)
        + math.cos(self.latr) * math.cos(loc2.latr) * math.sin(dlong/2) * math.sin(dlong/2)
        c = 2*math.atan2(math.sqrt(hav), math.sqrt(1-hav))
        return 6371*c
    
    def costTo(self, loc2): #TODO: return a distance & time
        return 0
        
