import pyproj

epsg3857 = pyproj.Proj(init='epsg:3857')
wgs84 = pyproj.Proj(init='EPSG:4326')
latlng = (-0.7690, 54.5179)
print "bottom left", pyproj.transform(wgs84,epsg3857,latlng[0],latlng[1])

latlng = (-0.7636, 54.5179)
print "bottom right", pyproj.transform(wgs84,epsg3857,latlng[0],latlng[1])

latlng = (-0.7690, 54.5210)
print "top left", pyproj.transform(wgs84,epsg3857,latlng[0],latlng[1])

latlng = (-0.7636, 54.5210)
print "top right", pyproj.transform(wgs84,epsg3857,latlng[0],latlng[1])