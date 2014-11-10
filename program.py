import math
import geopy
from geopy.distance import GreatCircleDistance
from math import radians, degrees, cos, sin, sqrt, atan2, asin, fabs, pi
import sys
sys.path.append("/usr/local/lib/python/site-packages")
from geographiclib.geodesic import Geodesic
import time

class coalition:
    def __init__(self, 
                 name,
                 lat, 
                 lng, 
                 gdp,
                 pop):
        self.name = name
        self.lat = lat
        self.lng = lng
        self.gdp = gdp
        self.pop = pop
    # End of constructor

def distance_1(A, B):
    dist = Geodesic.WGS84.Inverse(A.lat, A.lng, B.lat, B.lng)
    return dist['s12']/1000
# End of geocode distance dist['s12'] is in meters

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

    C = coalition(new_name,
                  new_lat, 
                  new_lng,
                  new_pop,
                  new_gdp)
    
    return C
# End of merge

# Choose the distance function here
distance = distance_3a

file = open("Coalitions geodistance.txt", "w")

coalitions = [
coalition("Albania", 41.3275459, 19.8186982, 1227, 1229),
coalition("Austria", 48.2081743, 16.3738189, 6935, 25702),
coalition("Belgium", 50.8503396, 4.3517103, 8639, 47190),
coalition("Bulgaria", 42.6977082, 23.3218675, 7251, 11971),
coalition("Czech Republic", 50.0755381, 14.4378005, 12389, 43368),
coalition("Denmark",  55.6760968, 12.5683371, 4271, 29654),
coalition("Finland", 60.17332440000001, 24.9410248, 4009, 17051),
coalition("France",  48.856614, 2.3522219,42518, 220492),
coalition("East Germany", 52.5200066, 13.404954, 18388, 51412), 
coalition("West Germany", 50.73743, 7.0982068, 50958, 213942),
coalition("Greece", 37.983917, 23.7293599, 7566, 14489),
coalition("Hungary", 47.497912, 19.040235, 9338, 23158),
coalition("Iceland", 64.133333, -21.933333, 143, 762),
coalition("Ireland", 53.3498053, -6.2603097, 2963, 10231),
coalition("Italy", 41.8723889, 12.4801802, 47105, 164957),
coalition("Liechtenstein", 47.14137, 9.5207, 14, 159),
coalition("Luxembourg", 49.815273, 6.129583, 296, 2481),
coalition("Monaco",  43.73841760000001, 7.4246158, 18, 158),
coalition("Netherlands", 52.3702157, 4.895167900000001, 10114, 60642),
coalition("Norway", 59.9138688, 10.7522454, 3265, 17728),
coalition("Poland", 52.2296756, 21.0122287, 24824, 60742),
coalition("Portugal",  38.7222524, -9.1393366, 8443, 17615),
coalition("Romania", 44.4325, 26.103889, 16311, 19279),
coalition("Soviet Union", 55.755826, 37.6173, 179571, 510243),
coalition("Spain", 40.4167754, -3.7037902, 28063,61429),
coalition("Sweden", 59.3293235, 18.0685808, 7014, 47478),
coalition("Switzerland", 46.9479222, 7.4446085, 4694, 42545),
coalition("United Kingdom",  51.5073509, -0.1277583, 50127, 347850),
coalition("Yugoslavia", 44.816667, 20.466667, 16298, 25277),
]

# Google map - according to the capitals 1950

# GDP for eat and west germany http://books.google.at/books?id=YeoEiNLtrLsC&pg=PA178&lpg=PA178&dq=Maddison,+1950+east+german+gdp&source=bl&ots=TAkNRGDaAR&sig=jzG_cfbPVLdkOeLOug4zHlDyCjA&hl=en&sa=X&ei=JNJgVLPJA4GOPcuSgLAB&ved=0CB8Q6AEwAA#v=onepage&q=Maddison%2C%201950%20east%20german%20gdp&f=false

#Population for east and west germany https://www.destatis.de/EN/FactsFigures/SocietyState/Population/CurrentPopulation/Tables_/lrbev03.html

# Gdp for iceland http://www.theworldeconomy.org/histostats/histostats-table01-4.pdf

# for lichtenstein and monaco took the average of 9 countries(ALMOST SAME think about it)
print [c.name for c in coalitions]

# for i, coalition_i in enumerate(coalitions):
 #    for j, coalition_j in enumerate(coalitions):
  #       if i >= j:
   #         print distance(coalition_i, coalition_j)

while len(coalitions)>2:

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
    
    #print [c.name for c in coalitions]

    outfile_name = "out_"+time.strftime("%Y_%m_%d_%H%M")+".txt"

    out_f = open(outfile_name, "w")

    for c in coalitions:
        out_f.write(c.name)
        out_f.write("\n\n")

        



