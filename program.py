
########################################
# Imports 
########################################

from __future__ import division

import sys
import math
import time

import numpy as np

sys.path.append("/usr/local/lib/python/site-packages")
from geographiclib.geodesic import Geodesic
from matrix2latex import matrix2latex
from mpl_toolkits.basemap import Basemap


########################################
# Configuration
########################################

default_dummy_distance = float("inf")


########################################
# Class: coalition
########################################

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


########################################
# distgregime
########################################

def distregime(A, B):
    if A.regime == B.regime:
       return 1
    else: 
       return default_dummy_distance
# return 1 if you do not want the regime
# return default_dummy_distance if you want to insert regime
# End of regime distance


########################################
# normalize
########################################

def normalize(x, 
              input_min, 
              input_max, 
              target_min = 0, 
              target_max = 1):
    """Use function of the form:
    y = a*x + b 
    Determine coefficients so that:
    y(input_min) = target_min and
    y(input_max) = target_max
    """
    
    a = target_max - (target_max - target_min) / (input_max - input_min)
    b = target_min - (input_min * (target_max - target_min))/(input_max - input_min)
    
    return a*x + b
# end of normalize


########################################
# distloc
########################################

def distloc(A, B, 
            input_min=-1, 
            input_max=-1, 
            target_min = 0, 
            target_max = 1):

    distloc_obj = Geodesic.WGS84.Inverse(A.lat, A.lng, B.lat, B.lng)/1000.
    distloc_km = distloc['s12']/1000.
    
    # Per default: do NOT normalize
    if input_min==-1 and input_max ==-1:
        return distloc_km * distregime(A, B)
    else:
        norm_distloc_km = normalize(distloc_km, input_min, input_max, target_min, target_max) 
        return norm_distloc_km * distregime(A, B)
# End of distloc


########################################
# distonlygdp
########################################

def distonlygdp(A, B, 
            input_min=-1, 
            input_max=-1, 
            target_min = 0, 
            target_max = 1):

    distonlygdp = abs(A.gdp - B.gdp)

    # Per default: do NOT normalize
    if input_min==-1 and input_max ==-1:
        return distonlygdp
    else:
        return normalize(distonlygdp, input_min, input_max, target_min, target_max) 
# End of distonlygdp


########################################
# distonlypop
########################################

def distonlypop(A, B, 
            input_min=-1, 
            input_max=-1, 
            target_min = 0, 
            target_max = 1):

    distonlypop = abs(A.pop - B.pop)

    # Per default: do NOT normalize
    if input_min==-1 and input_max ==-1:
        return distonlypop
    else:
        return normalize(distonlypop, input_min, input_max, target_min, target_max) 
# End of distonlypop


########################################
# midpoint
########################################

def midpoint(A,B):
     d = Geodesic.WGS84.Inverse(A.lat, A.lng, B.lat, B.lng)
     h = Geodesic.WGS84.Direct(A.lat, A.lng, d['azi1'], d['s12']/2)
     return h['lat2'], h['lon2']


########################################
# weightedmidpoint
########################################

def weightedmidpoint(A,B):
     w = 1
     d = Geodesic.WGS84.Inverse(A.lat, A.lng, B.lat, B.lng)
     h = Geodesic.WGS84.Direct(A.lat, A.lng, d['azi1'], d['s12']*(w*B.pop+(1-w)*B.gdp)/(w*A.pop+(1-w)*A.gdp+w*B.pop+(1-w)*B.gdp))
     return h['lat2'], h['lon2']


########################################
# merge
########################################

def merge(A, B):
    new_name = "{0}, {1}".format(A.name, B.name)
    new_lat, new_lng = midpoint(A, B) 
    new_pop = A.pop + B.pop
    new_gdp = A.gdp + B.gdp
    new_regime = A.regime

    C = coalition(new_name,
                  new_lat, 
                  new_lng,
                  new_pop,
                  new_gdp,
                  new_regime)
    
    return C
# End of merge


########################################
# Composite distance functions
########################################

# Create a dictionary of distances
distances = {}

# Add the more complicated distregime and distloc functions manuallly:

distances["normdistloc"] = lambda A,B,D: distloc(A, B, D["min_loc"], D["max_loc"])

distances["normdistlocpop"] = lambda A,B,D: distloc(A, B, D["min_loc"], D["max_loc"]) * distonlypop(A, B, D["min_pop"], D["max_pop"])

distances["normdistlocgdp"] = lambda A,B,D: distloc(A, B, D["min_loc"], D["max_loc"]) * distonlygdp(A, B, D["min_gdp"], D["max_gdp"])

distances["normdistlocpopgdp"] = lambda A,B,D: distloc(A, B, D["min_loc"], D["max_loc"]) * distonlypop(A, B, D["min_pop"], D["max_pop"]) * distonlygdp(A, B, D["min_gdp"], D["max_gdp"])





# Choose the distance function here
if len(sys.argv) == 2:
    distance_name = sys.argv[1]
else:
    print "Invalid number of command line arguments"
    print "Usage: program.py ditance_function_name"
    print sys.exit()

distance = distances[distance_name]

in_f = open("input_western_europe.txt", "r")

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
                                float(pop), 
                                float(gdp),
                                int (regime)))

# End of reading coalitions from file


outfile_name = "out_"+distance_name+"_"+time.strftime("%Y_%m_%d_%H%M")+".odt"

out_f = open(outfile_name, "w")

m = [[distance_name],['First coalition', 'Second coalition', 'distance']] # python nested list
n = [[distance_name],['Country', 'pop', 'gdp']] # python nested list


# write countries pop and gdp in table
'''for i, coalition_i in enumerate(coalitions):
    n.append([coalition_i.name, coalition_i.pop, coalition_i.gdp])
 k = matrix2latex(n)
 out_f.write(k)
'''




while len(coalitions)>1:

    # Find maximum and minimum distance for normalization
    minmax_dists = {    
        "max_loc" : -9999,
        "min_loc" : default_dummy_distance,
        "max_gdp" : -9999,
        "min_gdp" : default_dummy_distance,
        "max_pop" : -9999,
        "min_pop" : default_dummy_distance,
    }

    for i, coalition_i in enumerate(coalitions):
        for j, coalition_j in enumerate(coalitions):
      
            if i >= j:
                continue
                
            # Maximum Location Distance
            if distloc(coalition_i, coalition_j) > minmax_dists["max_loc"]:
                minmax_dists["max_loc"] = distloc(coalition_i, coalition_j)
            # Minimum Location Distance
            if distloc(coalition_i, coalition_j) < minmax_dists["min_loc"]:
                minmax_dists["min_loc"] = distloc(coalition_i, coalition_j)
            # Maximum GDP Distance
            if distonlygdp(coalition_i, coalition_j) > minmax_dists["max_gdp"]:
                minmax_dists["max_gdp"]= distonlygdp(coalition_i, coalition_j)
            # Minimum GDP Distance
            if distonlygdp(coalition_i, coalition_j) < minmax_dists["min_gdp"]:
                minmax_dists["min_gdp"] = distonlygdp(coalition_i, coalition_j)
            # Maximum POP Distance
            if distonlypop(coalition_i, coalition_j) > minmax_dists["max_pop"]:
                minmax_dists["max_pop"] = distonlypop(coalition_i, coalition_j)
            # Minimum POP Distance
            if distonlypop(coalition_i, coalition_j) < minmax_dists["min_pop"]:
                minmax_dists["min_pop"] = distonlypop(coalition_i, coalition_j)
    # Done finding maximum and minimum distances for normalization
            
    min_distance = default_dummy_distance
    first_coalition = None
    second_coalition = None

    for i, coalition_i in enumerate(coalitions):
        for j, coalition_j in enumerate(coalitions):

            if i >= j:
                continue
            
            if distance(coalition_i, coalition_j, minmax_dists) < min_distance: 
                min_distance = distance(coalition_i, coalition_j, minmax_dists)
                first_coalition = coalition_i
                second_coalition = coalition_j
           
    coalitions.append(merge(first_coalition, second_coalition))
    coalitions.remove(first_coalition)
    coalitions.remove(second_coalition)


    m.append([first_coalition.name, second_coalition.name, distance(first_coalition, second_coalition, minmax_dists)])
   

   # for c in coalitions:
   #     out_f.write(c.name)
   #     out_f.write(", ")
   # out_f.write("\n\n")

# Latex tables
t = matrix2latex(m)
out_f.write(t)

      



