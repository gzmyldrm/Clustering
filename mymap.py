import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap



# Cities names and coordinates
cities = ['London', 'Madrid', 'Moscow']
lat = [51.507778, 40.4, 55.751667]
lon = [-0.128056, -3.683333, 37.617778]

# orthogonal projection of the Earth
m = Basemap(llcrnrlon=-23.,llcrnrlat=36.,urcrnrlon=49.,urcrnrlat=72.,\
            rsphere=(6378137.00,6356752.3142),\
            resolution='l',area_thresh = 1000.0,projection='merc',\
            lat_0=40.,lon_0=-20.)


# draw the borders of the map
m.drawmapboundary()
# draw the coasts borders and fill the continents
m.drawcoastlines()
m.fillcontinents()
m.drawcountries()



# map city coordinates to map coordinates
x, y = m(lon, lat)


# draw a red dot at cities coordinates
plt.plot(x, y, 'ro')



# for each city,
for city, xc, yc in zip(cities, x, y):
# draw the city name in a yellow (shaded) box
  plt.text(xc+250000, yc-150000, city,
    bbox=dict(facecolor='yellow', alpha=0.5))

plt.show()

