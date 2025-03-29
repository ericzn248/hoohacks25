from time import time
import math

MASS = 1e7  # mass of ship in kg
RHO = 1.293  # air density
CD = 1.28  # drag coefficient for flat surface
A_PARALLEL = 1500  # frontal area (m^2)
A_PERP = 9000  # side area (m^2)

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
    
     def costTo(self, loc2, wind, current):
        dist_km = self.distance(loc2)
        dist_m = dist_km * 1000

        dx = loc2.long - self.long
        dy = loc2.lat - self.lat
        direction = Vector(dx, dy).unit()
        intended = direction * 18  # Sets ship's intended speed as 18 m/s in that direction

        # Actual boat velocity (intended + current)
        boat_velocity = intended + current

        # Relative wind
        rel_wind = wind - boat_velocity

        # Unit vectors
        u_boat = boat_velocity.unit()
        # Perpendicular unit vector (rotate 90 degrees)
        n_boat = Vector(-u_boat.y, u_boat.x)

        # Wind components
        v_parallel = rel_wind.dot(u_boat)
        v_perp_squared = rel_wind.dot(rel_wind) - v_parallel**2

        # Wind force vector
        F_parallel = 0.5 * RHO * CD * A_PARALLEL * v_parallel**2 * (1 if v_parallel >= 0 else -1)
        F_perp = 0.5 * RHO * CD * A_PERP * v_perp_squared * (1 if rel_wind.dot(n_boat) >= 0 else -1)
        wind_force = u_boat * F_parallel + n_boat * F_perp

        # Time in seconds through the cell
        speed = boat_velocity.mag if boat_velocity.mag > 0 else 0.1  # prevent div by zero
        delta_t = dist_m / speed

        # Momentum update
        delta_p = wind_force * delta_t
        total_momentum = boat_velocity * MASS + delta_p

        # Final velocity = total momentum / mass
        final_velocity = total_momentum * (1 / MASS)

        return dist_m / final_velocity  # This is time in seconds
        
