import math
import geopy
from geopy.distance import GreatCircleDistance
from math import radians, degrees, cos, sin, sqrt, atan2, asin, fabs, pi
import sys
sys.path.append("/usr/local/lib/python/site-packages")
from geographiclib.geodesic import Geodesic
import time

default_dummy_distance = 999999999999999
class coalition:
    def __init__(self, 
                 name,
                 lat, 
                 lng, 
                 gdp,
                 pop,
                 regime):
        self.name = name
        self.lat = lat
        self.lng = lng
        self.gdp = gdp
        self.pop = pop
        self.regime = regime
    # End of constructor

def distance_1(A, B):
    dist = Geodesic.WGS84.Inverse(A.lat, A.lng, B.lat, B.lng)
    return dist['s12']/1000
# End of geocode distance dist['s12'] is in meters

def distance_regime(A, B):
    if A.regime = B.regime:
       return 1
    else: 
       return default_dummy_distance
# End of regime type

def distance_2(A, B):
    dist_2 = distance_1(A, B)*abs(A.pop-B.pop)
    return dist_2
# End of geocode distance combination with pop

def distance_2a(A, B):
    dist_2a = distance_1(A, B)*abs(A.pop-B.pop)**2
    return dist_2a
# End of geocode distance combination with quadratic pop 

def distance_3(A, B):
    dist_3 = distance_1(A, B)*abs(A.gdp-B.gdp)
    return dist_3
# End of geocode distance combination with gdp

def distance_3a(A, B):
    dist_3a = distance_1(A, B)*abs(A.gdp-B.gdp)**2
    return dist_3a
# End of geocode distance combination with quadratic gdp

def distance_4(A, B):
    dist_4 = distance_1(A, B)*abs(A.pop-B.pop)*abs(A.gdp-B.gdp)
    return dist_4
# End of geocode distance combination with pop and gdp

def distance_4a(A, B):
    dist_4a = distance_1(A, B)*abs(A.pop-B.pop)**2*abs(A.gdp-B.gdp)**2
    return dist_4a
# End of geocode distance combination with quadratic pop and gdp

def distance_5(A, B):
    dist_5 = distance_1(A, B)*abs(A.pop-B.pop)/abs(A.pop+B.pop)
    return dist_5
# End of geocode distance combination with propotional pop

def distance_6(A, B):
    dist_6 = distance_1(A, B)*abs(A.gdp-B.gdp)/abs(A.gdp+B.gdp)
    return dist_6
# End of geocode distance combination with propotional pop

def midpoint(A,B):
     d = Geodesic.WGS84.Inverse(A.lat, A.lng, B.lat, B.lng)
     h = Geodesic.WGS84.Direct(A.lat, A.lng, d['azi1'], d['s12']/2)
     return h['lat2'], h['lon2']

def merge(A, B):
    new_name = "{0}_{1}".format(A.name, B.name)
    new_lat, new_lng = midpoint(A, B) 
    new_pop = (A.pop + B.pop)/2
    new_gdp = (A.gdp + B.gdp)/2
    new_regime = A.regime

    C = coalition(new_name,
                  new_lat, 
                  new_lng,
                  new_pop,
                  new_gdp,
                  new_regime)
    
    return C
# End of merge

# Choose the distance function here
distance = distance_3a

in_f = open("input_coalitions.txt", "r")

coalitions = []

for line in in_f:    
    
    # Allow comments in the text file
    if "#" in line:
        continue
    
    # split by "," and remove extra whitespace
    [name, lat, lng, pop, gdp, regime] = [x.strip() for x in line.split(",")]

    # Create coalition object and add to list
    coalitions.append(coalition(name, 
                                float(lat), 
                                float(lng), 
                                int(pop), 
                                int(gdp),
                                int (regime)))

# End of reading coalitions from file

print [c.name for c in coalitions]

# for i, coalition_i in enumerate(coalitions):
 #    for j, coalition_j in enumerate(coalitions):
  #       if i >= j:
   #         print distance(coalition_i, coalition_j)

while len(coalitions)>2:

    min_distance = default_dummy_distance
    first_coalition = None
    second_coalition = None

    for i, coalition_i in enumerate(coalitions):
        for j, coalition_j in enumerate(coalitions):

            if i >= j:
                continue

            if distance(coalition_i, coalition_j) < min_distance:
                min_distance = distance(coalition_i, coalition_j)
                first_coalition = coalition_i
                second_coalition = coalition_j
    coalitions.append(merge(first_coalition, second_coalition))
   # print midpoint(first_coalition, second_coalition)
    coalitions.remove(first_coalition)
    coalitions.remove(second_coalition)
    
    #print [c.name for c in coalitions]

    outfile_name = "out_"+time.strftime("%Y_%m_%d_%H%M")+".txt"

    out_f = open(outfile_name, "w")

    for c in coalitions:
        out_f.write(c.name)
        out_f.write("\n\n")

        



