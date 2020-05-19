import os
import urllib
import math
import time
from decimal import Decimal
from PIL import Image

from tileGeoTransfer import * # getTileFromGeo & getGeoFromTile



def checkBlankImg_ggl(filename):
	'''
	input type: file path
	return type: Boolean
	'''
	try:
		im = Image.open(filename) # Can be many different formats.
		pix = im.load()

		# print im.size
		pixel_values = list(im.getdata())
		
		# RGB channel
		if min(pixel_values) == max(pixel_values):
			return True
		else:
			return False
	except Exception as e:
		print e
		return True

def checkBlankImg_nls(filename):
	'''
	input type: file path
	return type: Boolean
	'''
	try:

		im = Image.open(filename)
		pix = im.load()

		# print im.size
		pixel_values = list(im.getdata())
		zipped = zip(pixel_values)

		# RGB channel
		if min(zipped[0][0]) == max(zipped[0][0]) \
			and min(zipped[1][0]) == max(zipped[1][0]) \
			and min(zipped[2][0]) == max(zipped[2][0]):
			return True
		else:
			return False
	except Exception as e:
		print e
		return True


def store_4Geo_Boundary(lnglat_path, x, y, z):
	f = open(lnglat_path,"w+")

	# bottom right
	lat, lng = getGeoFromTile(x, y, z)
	f.write("%f %f\n"%(lat, lng))

	# bottom left
	lat, lng = getGeoFromTile(x + 1, y, z)
	f.write("%f %f\n"%(lat, lng))

	# top right
	lat, lng = getGeoFromTile(x, y + 1, z)
	f.write("%f %f\n"%(lat, lng))

	# top left
	lat, lng = getGeoFromTile(x + 1, y + 1, z)
	f.write("%f %f\n"%(lat, lng))

	f.close()



def getImgFromUrl(url_ggl, url_nls, stored_directory, x, y, z):
	obj_nls = urllib.urlopen(url_nls)
	obj_ggl = urllib.urlopen(url_ggl)


	if obj_nls.getcode() == 200 and obj_ggl.getcode() == 200:

		if not os.path.exists(stored_directory):
			os.makedirs(stored_directory)

		name_nls = stored_directory + "nls_%d_%d_%d.jpg" % (x, y, z)
		name_ggl = stored_directory + "osm_%d_%d_%d.jpg" % (x, y, z)
		urllib.urlretrieve(url_nls, name_nls)
		urllib.urlretrieve(url_ggl, name_ggl)


		# Check if the image is blank, i.e: sea, plain grass
		if checkBlankImg_nls(name_nls) or checkBlankImg_ggl(name_ggl):
			if os.path.exists(name_nls) and os.path.exists(name_ggl):
				os.remove(name_nls)
				os.remove(name_ggl)
				print "delete: ", x, y, z
			else:
				print "file does not exist"
		else:
			lnglat_dir = stored_directory + "lnglat/"
			if not os.path.exists(lnglat_dir):
				os.makedirs(lnglat_dir)

			lnglat_path = lnglat_dir + "nls_%d_%d_%d.txt" % (x, y, z)
			store_4Geo_Boundary(lnglat_path, x, y, z)
			
			print "success: ", x, y, z, getGeoFromTile(x, y, z)
	else:
		print "F", x, y, z



def retrieveMap_byxyz(x_start, x_end, y_start, y_end, z):
	#urlBase_osm_map = "https://b.tile.openstreetmap.org/%d/%d/%d.png"
	urlBase_osm_map = "https://tiles.wmflabs.org/osm-no-labels/%d/%d/%d.png"
	
	#urlBase_nls_map = "https://nls-1.tileserver.com/5eF1a699E49r/%d/%d/%d.jpg"
	urlBase_nls_map = "https://nls-2.tileserver.com/nls/%d/%d/%d.png"
	
	stored_directory = "z13/"
	
	for x in xrange(x_start, x_end + 1):
		for y in xrange(y_start, y_end + 1):
			print x, y
			url_osm_map = urlBase_osm_map % (z, x, y)
			url_nls_map = urlBase_nls_map % (z, x, y)
			
			getImgFromUrl(url_osm_map, url_nls_map, stored_directory, x, y, z)
			time.sleep(0.005)
		# time.sleep(1)



def getBoundary(start_lat, end_lat, start_long, end_long, zoom):
	x0, y0, z = getTileFromGeo(start_lat, start_long, zoom)
	x1, y1, z = getTileFromGeo(start_lat, end_long, zoom)
	x2, y2, z = getTileFromGeo(end_lat, start_long, zoom)
	x3, y3, z = getTileFromGeo(end_lat, end_long, zoom)

	start_x = min(x0, x1, x2, x3)
	end_x = max(x0, x1, x2, x3)
	start_y = min(y0, y1, y2, y3)
	end_y = max(y0, y1, y2, y3)

	print start_x, end_x, start_y, end_y
	retrieveMap_byxyz(start_x, end_x, start_y, end_y, z)



if __name__ == "__main__":
	
	#getBoundary(50.600, 57.500, -6.5000, 1.7500, 9)
	getBoundary(51.000, 53.500, -4.000, 0.000, 13) # 4004 4096 2649 2742
	# error happens here: 32698, 21504
	# time.sleep(0.5)
	# getBoundary(52.5000, 53.0000, -1.0000, 1.0000, 16)

