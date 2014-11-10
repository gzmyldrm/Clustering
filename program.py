import math
import geopy
from geopy.distance import GreatCircleDistance
from math import radians, degrees, cos, sin, sqrt, atan2, asin, fabs, pi
import sys
sys.path.append("/usr/local/lib/python/site-packages")
from geographiclib.geodesic import Geodesic

class coalition:
    def __init__(self, 
                 name,
                 lat, 
                 lng, 
                 gdp = -1,
                 pop = -1):
        self.name = name
        self.lat = lat
        self.lng = lng
        self.gdp = gdp
        self.pop = pop
    # End of constructor

def distance_1(A, B):
    dist = Geodesic.WGS84.Inverse(A.lat, A.lng, B.lat, B.lng)
    return dist['s12']
# End of geocode distance

def midpoint(A,B):
     d = Geodesic.WGS84.Inverse(A.lat, A.lng, B.lat, B.lng)
     h = Geodesic.WGS84.Direct(A.lat, A.lng, d['azi1'], d['s12']/2)
     return h['lat2'], h['lon2']

def merge(A, B):
    new_name = "{0}_{1}".format(A.name, B.name)
    new_lat, new_lng = midpoint(A, B) 
    new_pop = (A.pop + B.pop)/2
    new_gdp = (A.gdp + B.gdp)/2

    C = coalition(new_name,
                  new_lat, 
                  new_lng,
                  new_pop,
                  new_gdp)
    
    return C
# End of merge

# Choose the distance function here
distance = distance_1

coalitions = [
coalition("Albania", 41.3275459, 19.8186982, 1227),
coalition("Austria", 48.2081743, 16.3738189, 6935),
coalition("Belgium", 50.8503396, 4.3517103, 8639),
coalition("Bulgaria", 42.6977082, 23.3218675, 7251),
coalition("Czech Republic", 50.0755381, 14.4378005, 12389),
coalition("Denmark",  55.6760968, 12.5683371, 4271),
coalition("Finland", 60.17332440000001, 24.9410248, 4009),
coalition("France",  48.856614, 2.3522219,42518),
coalition("East Germany", 52.5200066, 13.404954, 18388),
coalition("West Germany", 50.73743, 7.0982068, 50958),
coalition("Greece", 37.983917, 23.7293599, 7566),
coalition("Hungary", 47.497912, 19.040235, 9338),
coalition("Iceland", 64.133333, -21.933333, 143),
coalition("Ireland", 53.3498053, -6.2603097, 2963),
coalition("Italy", 41.8723889, 12.4801802, 47105),
coalition("Liechtenstein", 47.14137, 9.5207, 14),
coalition("Luxembourg", 49.815273, 6.129583, 296),
coalition("Monaco",  43.73841760000001, 7.4246158, 18),
coalition("Netherlands", 52.3702157, 4.895167900000001, 10114),
coalition("Norway", 59.9138688, 10.7522454, 3265),
coalition("Poland", 52.2296756, 21.0122287, 24824),
coalition("Portugal",  38.7222524, -9.1393366, 8443),
coalition("Romania", 44.4325, 26.103889, 16311),
coalition("Soviet Union", 55.755826, 37.6173, 179571),
coalition("Spain", 40.4167754, -3.7037902, 28063),
coalition("Sweden", 59.3293235, 18.0685808, 7014),
coalition("Switzerland", 46.9479222, 7.4446085,4694),
coalition("United Kingdom",  51.5073509, -0.1277583, 50127),
coalition("Yugoslavia", 44.816667, 20.466667, 16298),
]

# Google map - according to the capitals 1950
print [c.name for c in coalitions]

# for i, coalition_i in enumerate(coalitions):
 #    for j, coalition_j in enumerate(coalitions):
  #       if i >= j:
   #         print distance(coalition_i, coalition_j)

while len(coalitions)>3:

    min_distance = 999999999999999.
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
    
   
    print [c.name for c in coalitions]
    



            




        



