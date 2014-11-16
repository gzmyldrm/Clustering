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

# Create a dictionary of distances
distances = {}

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

# Add the more complicated distregime and distloc functions manuallly:
distances["distregime"] = distregime
distances["distloc"] = distloc

# And for the rest, use lambda magic (-;

# geocode distance combination with pop
distances["distpop"] = lambda A,B: distloc(A, B)*abs(A.pop-B.pop)

# distance combination with quadratic pop d
distances["distpop2"] = lambda A,B: distloc(A, B)*abs(A.pop-B.pop)**2

# geocode distance combination with gdp
distances["distgdp"] = lambda A,B: distloc(A, B)*abs(A.gdp-B.gdp)

# geocode distance combination with quadratic gdp
distances["distgdp2"] = lambda A,B: distloc(A, B)*abs(A.gdp-B.gdp)**2

# geocode distance combination with pop and gdp
distances["distpopgdp"] = lambda A,B: distloc(A, B)*abs(A.pop-B.pop)*abs(A.gdp-B.gdp)

# geocode distance combination with quadratic pop and gdp
distances["distpopgdp2"] = lambda A,B: distloc(A, B)*abs(A.pop-B.pop)**2*abs(A.gdp-B.gdp)**2

# geocode distance combination with propotional pop
distances["distpopratio"] = lambda A,B: distloc(A, B)*abs(A.pop-B.pop)/abs(A.pop+B.pop)

# geocode distance combination with propotional gdp
distances["distgdpratio"] = lambda A,B: distloc(A, B)*abs(A.gdp-B.gdp)/abs(A.gdp+B.gdp)

# geocode distance combination with propotional pop and gdp 
distances["distpopgdpratio"] = lambda A,B: distloc(A, B)*abs(A.pop-B.pop)/abs(A.pop+B.pop)*abs(A.gdp-B.gdp)/abs(A.gdp+B.gdp)

# geocode distance combination with quadratic propotional pop and gdp 
distances["distpopgdpratio2"] = lambda A,B: distloc(A, B)*(abs(A.pop-B.pop)/abs(A.pop+B.pop))**2*(abs(A.gdp-B.gdp)/abs(A.gdp+B.gdp))**2

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
if len(sys.argv == 2):
    distance_name = sys.argv[1]
else:
    print "Invalid number of command line arguments"
    print "Usage: program.py ditance_function_name"
    print sys.exit()

distance = distances[distance_name]

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
    
    tmp_lat, tmp_lng =  midpoint(first_coalition, second_coalition)
    out_f.write(first_coalition.name) 
    out_f.write(", ")
    
    out_f.write(second_coalition.name)
    out_f.write("\n")
    out_f.write('distance is {0}'.format(distloc(first_coalition, second_coalition)))
    out_f.write("\n")
    out_f.write('midpoint is lat={0} / lng={1}'.format(tmp_lat, tmp_lng))
    out_f.write("\n")
    #print [c.name for c in coalitions]
    
    for c in coalitions:
        out_f.write(c.name)
        out_f.write(", ")
    out_f.write("\n\n")

      



