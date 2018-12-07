'''
generate_wld_file.py
'''
import os
import pyproj
from tileGeoTransfer import *

def generate_wld_file(x, y, z):
	directory = "jgw/"

	if not os.path.exists(directory):
		os.makedirs(directory)

	filePath = directory + "/osm_%d_%d_%d.wld" % (x, y, z)
	f = open(filePath,"w+")

	epsgX, epsgY = calculate(x, y, z)
	epsgX_1, epsgY_1 = calculate(x + 1, y + 1, z)
	
	f.write("%f\n" % ((epsgX_1 - epsgX)/ 256))
	f.write("0\n")
	f.write("0\n")
	f.write("%f\n" % ((epsgY_1 - epsgY)/ 256))
	f.write("%f\n" % epsgX)
	f.write("%f\n" % epsgY)

	f.close()


def calculate(x, y, z):
	'''
	points:	2--3
			|  |
			0--1
	'''
	epsg3857 = pyproj.Proj(init='epsg:3857')
	wgs84 = pyproj.Proj(init='EPSG:4326')

	lat,lng = getGeoFromTile(x, y, z)
	return pyproj.transform(wgs84,epsg3857, lng, lat)


def generate_jpg_points_file(x, y, z):
	'''
	points:	2--3
			|  |
			0--1
	'''
	directory = "jgw/"

	if not os.path.exists(directory):
		os.makedirs(directory)

	filePath = directory + "/osm_%d_%d_%d.jpg.points" % (x, y, z)
	f = open(filePath,"w+")

	# bottom left
	epsgX_0, epsgY_0 = calculate(x, y, z)
	# bottom right
	epsgX_1, epsgY_1 = calculate(x + 1, y, z)
	# top left
	epsgX_2, epsgY_2 = calculate(x, y + 1, z)
	# top right
	epsgX_3, epsgY_3 = calculate(x + 1, y + 1, z)
	
	f.write("mapX,mapY,pixelX,pixelY,enable\n")
	f.write("%f,%f,0,0,1\n" % (epsgX_0, epsgY_0))
	f.write("%f,%f,255,0,1\n" % (epsgX_1, epsgY_1))
	f.write("%f,%f,255,-255,1\n" % (epsgX_2, epsgY_2))
	f.write("%f,%f,0,-255,1\n" % (epsgX_3, epsgY_3))

	f.close()


if __name__ == "__main__":
	for x in xrange(32585, 32588):
		for y in xrange(21632, 21648):
			generate_wld_file(x, y, 16)
			generate_jpg_points_file(x, y, 16)
	
