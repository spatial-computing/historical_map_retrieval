'''
tileGeoTransfer.py
'''

import math
from decimal import Decimal

def getTileFromGeo(lat, long, zoom):
	'''
	get tile index from geo location
	:type : float, float, int
	:rtype: tuple(int, int, int)
	'''
	x = math.floor((long + 180) / 360.0 * (2.0 ** zoom))

	tan_y = math.tan(lat * (math.pi / 180.0))
	cos_y = math.cos(lat * (math.pi / 180.0))
	y = math.floor( (1 - math.log(tan_y + 1.0 / cos_y) / math.pi) / 2.0 * (2.0 ** zoom) )
	
	return int(x), int(y), int(zoom)


def getGeoFromTile(x, y, zoom):
	lon_deg = x / (2.0 ** zoom) * 360.0 - 180.0
	lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * y / (2.0 ** zoom))))
	lat_deg = lat_rad * (180.0 / math.pi)
	return lat_deg, lon_deg


if __name__ == "__main__":
	print getGeoFromTile(32628, 20880, 16)
	print getGeoFromTile(32628, 20881, 16)
	print getGeoFromTile(32629, 20880, 16)
	print getGeoFromTile(32629, 20881, 16)
	# x = 32628
	# y = 20880
	# z = 16
	# a, b = getGeoFromTile(x, y, z)
	# print a, b
	# a = 54.5178
	# b = -0.7690
	# print getTileFromGeo(a, b, z)