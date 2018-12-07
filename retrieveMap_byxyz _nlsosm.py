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
	im = Image.open(filename) # Can be many different formats.
	pix = im.load()

	# print im.size
	pixel_values = list(im.getdata())
	
	# RGB channel
	if min(pixel_values) == max(pixel_values):
		return True

	return False

def checkBlankImg_nls(filename):
	'''
	input type: file path
	return type: Boolean
	'''
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

	return False


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
	urlBase_osm_map = "https://b.tile.openstreetmap.org/%d/%d/%d.png"
	urlBase_nls_map = "https://nls-1.tileserver.com/5eF1a699E49r/%d/%d/%d.jpg"
	
	stored_directory = "jgw/"
	
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
	getBoundary(52.0100, 52.0500, -1.0000, -0.9500, 16)
	# error happens here: 32698, 21504
	# time.sleep(0.5)
	# getBoundary(52.5000, 53.0000, -1.0000, 1.0000, 16)

'''
F 32697 21647 16
F 32698 21498 16
F 32698 21499 16
success:  32698 21500 16 (52.49615953109709, -0.384521484375)
success:  32698 21501 16 (52.49281508540495, -0.384521484375)
success:  32698 21502 16 (52.48947038534305, -0.384521484375)
F 32698 21503 16
Traceback (most recent call last):
  File "/Users/tresgrand/Documents/Python/retrieveMap/retrieveMap_byxyz _nlsosm.py", line 146, in <module>
    getBoundary(52.0000, 52.5000, -1.0000, 1.0000, 16)
  File "/Users/tresgrand/Documents/Python/retrieveMap/retrieveMap_byxyz _nlsosm.py", line 141, in getBoundary
    retrieveMap_byxyz(start_x, end_x, start_y, end_y, z)
  File "/Users/tresgrand/Documents/Python/retrieveMap/retrieveMap_byxyz _nlsosm.py", line 123, in retrieveMap_byxyz
    getImgFromUrl(url_osm_map, url_nls_map, stored_directory, x, y, z)
  File "/Users/tresgrand/Documents/Python/retrieveMap/retrieveMap_byxyz _nlsosm.py", line 90, in getImgFromUrl
    if checkBlankImg_nls(name_nls) or checkBlankImg_ggl(name_ggl):
  File "/Users/tresgrand/Documents/Python/retrieveMap/retrieveMap_byxyz _nlsosm.py", line 17, in checkBlankImg_ggl
    im = Image.open(filename) # Can be many different formats.
  File "/usr/local/lib/python2.7/site-packages/PIL/Image.py", line 2256, in open
    % (filename if filename else fp))
IOError: cannot identify image file 'folder_16/osm_32698_21504_16.jpg'
[Finished in 21593.4s with exit code 1]
[shell_cmd: python -u "/Users/tresgrand/Documents/Python/retrieveMap/retrieveMap_byxyz _nlsosm.py"]
[dir: /Users/tresgrand/Documents/Python/retrieveMap]
[path: /Library/Frameworks/Python.framework/Versions/3.5/bin:/usr/local/opt/python/libexec/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/X11/bin:/Users/tresgrand/apache-maven-3.5.3/bin]
'''

