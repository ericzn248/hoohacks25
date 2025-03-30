from time import time
import math

MASS = 1.5e8  # mass of ship in kg
RHO = 1.293  # air density
CD = 1.28  # drag coefficient for flat surface
A_PARALLEL = 1500  # frontal area (m^2)
A_PERP = 9000  # side area (m^2)
SHIP_SPEED = 9.26 #18 knots => m/s

def knots2kmh(s):
    return 1.852*s

def deg2rad(d):
    return math.pi*(d/180)

class Vector():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dir = math.atan2(y,x)
        self.mag = math.sqrt(x**2+y**2)

    def __eq__(self, vec2):
        return abs(self.x-vec2.x)+abs(self.y-vec2.y) > 0.0001
    
    def __add__(self, vec2):
        return Vector(self.x+vec2.x, self.y+vec2.y)

    def __sub__(self, vec2):
        return Vector(self.x-vec2.x, self.y-vec2.y)
    
    def __mul__(self, scalar):
        return Vector(self.x*scalar, self.y*scalar)
    
    def __truediv__(self, scalar):
        return Vector(self.x/scalar, self.y/scalar)
    
    def __hash__(self):
        return hash((round(self.x, 6), round(self.y, 6)))
    
    def dot(self, vec2):
        return self.x*vec2.x + self.y*vec2.y
    
    def unit(self):
        return Vector(self.x/self.mag, self.y/self.mag)

class Location():
    def __init__(self, lat, long):
        self.lat = lat
        self.long = long
        self.latr = lat*(math.pi/180)
        self.longr = long*(math.pi/180)
    
    def __eq__(self,loc2):
        return abs(self.lat-loc2.lat)+abs(self.long-loc2.long) < 0.0001 #small error for float calcs
    
    def __hash__(self):
        return hash((round(self.lat, 6), round(self.long, 6)))
    
    def __repr__(self):
        return f"Location({self.lat}, {self.long})"
    
    def distance(self, loc2): #gets distance between locations in kilometers
        dlat = deg2rad(loc2.lat-self.lat)
        dlong = deg2rad(loc2.long-self.long)
        hav = math.sin(dlat/2) * math.sin(dlat/2) + \
            math.cos(self.latr) * math.cos(loc2.latr) * \
            math.sin(dlong/2) * math.sin(dlong/2)
        c = 2*math.atan2(math.sqrt(hav), math.sqrt(1-hav))
        return 6371*c
    
   def costTo(self, loc2, wind, current):
    dist_km = self.distance(loc2)
    dist_m = dist_km * 1000

    dt = 300  # Time step in seconds
    dx = loc2.long - self.long
    dy = loc2.lat - self.lat
    direction = Vector(dx, dy).unit()

    # Initial velocity includes current only once
    velocity = direction * SHIP_SPEED + current

    position = 0.0
    time_elapsed = 0.0
    total_v = 0
    count = 0

    while position < dist_m:
        # Use current-adjusted velocity directly
        rel_wind = wind - velocity

        u_boat = velocity.unit()
        n_boat = Vector(-u_boat.y, u_boat.x)

        v_parallel = rel_wind.dot(u_boat)
        v_perp_squared = rel_wind.dot(rel_wind) - v_parallel**2

        F_parallel = 0.5 * RHO * CD * A_PARALLEL * v_parallel * abs(v_parallel)
        F_perp = 0.5 * RHO * CD * A_PERP * v_perp_squared * (1 if rel_wind.dot(n_boat) >= 0 else -1)
        wind_force = u_boat * F_parallel + n_boat * F_perp

        acceleration = wind_force / MASS

        # Dampened adjustment
        dampen = 0.01 / (1 + time_elapsed / 3600)
        velocity = velocity + acceleration * dt * dampen

        if velocity.mag < 0.1:
            print("Ship stopped due to excessive drag.")
            break

        position += velocity.mag * dt
        time_elapsed += dt
        total_v += velocity.mag
        count += 1

    actual_avg_velocity = total_v / count if count > 0 else 0
    adjusted_time_elapsed = dist_m / actual_avg_velocity if actual_avg_velocity > 0 else 0

    return adjusted_time_elapsed

        
