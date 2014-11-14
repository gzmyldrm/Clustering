import math
import geopy
from geopy.distance import GreatCircleDistance
from math import radians, degrees, cos, sin, sqrt, atan2, asin, fabs, pi
import sys
sys.path.append("/usr/local/lib/python/site-packages")
from geographiclib.geodesic import Geodesic
import time

default_dummy_distance = float("inf")

class coalition:
    def __init__(self, 
                 name,
                 lat, 
                 lng, 
                 pop,
                 gdp,
                 regime):
        self.name = name
        self.lat = lat
        self.lng = lng
        self.pop = pop
        self.gdp = gdp
        self.regime = regime
    # End of constructor

def distregime(A, B):
    if A.regime == B.regime:
       return 1
    else: 
       return default_dummy_distance
# return 1 if you do not want the regime
# return default_dummy_distance if you want to insert regime
# End of regime distance

def distloc(A, B):
    distloc = Geodesic.WGS84.Inverse(A.lat, A.lng, B.lat, B.lng)
    return (distloc['s12']/1000)*distregime(A, B)
# End of location distance dist['s12'] is in meters


def distpop(A, B):
    distpop = distloc(A, B)*abs(A.pop-B.pop)
    return distpop
# End of geocode distance combination with pop

def distpop2(A, B):
    distpop2 = distloc(A, B)*abs(A.pop-B.pop)**2
    return distpop2
# End of geocode distance combination with quadratic pop 

def distgdp(A, B):
    distgdp = distloc(A, B)*abs(A.gdp-B.gdp)
    return distgdp
# End of geocode distance combination with gdp

def distgdp2(A, B):
    distgdp2 = distloc(A, B)*abs(A.gdp-B.gdp)**2
    return distgdp2
# End of geocode distance combination with quadratic gdp

def distpopgdp(A, B):
    distpopgdp = distloc(A, B)*abs(A.pop-B.pop)*abs(A.gdp-B.gdp)
    return distpopgdp
# End of geocode distance combination with pop and gdp

def distpopgdp2(A, B):
    distpopgdp2 = distloc(A, B)*abs(A.pop-B.pop)**2*abs(A.gdp-B.gdp)**2
    return distpopgdp2
# End of geocode distance combination with quadratic pop and gdp

def distpopratio(A, B):
    distpopratio = distloc(A, B)*abs(A.pop-B.pop)/abs(A.pop+B.pop)
    return distpopratio
# End of geocode distance combination with propotional pop

def distgdpratio(A, B):
    distgdpratio = distloc(A, B)*abs(A.gdp-B.gdp)/abs(A.gdp+B.gdp)
    return distgdpratio
# End of geocode distance combination with propotional gdp

def distpopgdpratio(A, B):
    distpopgdpratio = distloc(A, B)*abs(A.pop-B.pop)/abs(A.pop+B.pop)*abs(A.gdp-B.gdp)/abs(A.gdp+B.gdp)
    return distpopgdpratio
# End of geocode distance combination with propotional pop and gdp 

def distpopgdpratio2(A, B):
    distpopgdpratio2 = distloc(A, B)*(abs(A.pop-B.pop)/abs(A.pop+B.pop))**2*(abs(A.gdp-B.gdp)/abs(A.gdp+B.gdp))**2
    return distpopgdpratio2
# End of geocode distance combination with quadratic propotional pop and gdp 

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
distance = distpopgdpratio2

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

#print [c.name for c in coalitions]

# for i, coalition_i in enumerate(coalitions):
 #    for j, coalition_j in enumerate(coalitions):
  #       if i >= j:
   #         print distance(coalition_i, coalition_j)

outfile_name = "out_"+time.strftime("%Y_%m_%d_%H%M")+".odt"

out_f = open(outfile_name, "w")
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
    #print distance(first_coalition, second_coalition)
    #print midpoint(first_coalition, second_coalition)
    coalitions.remove(first_coalition)
    coalitions.remove(second_coalition)
    
    #print [c.name for c in coalitions]
    
    for c in coalitions:
        out_f.write(c.name)
        out_f.write(", ")
    out_f.write("\n\n")

      



