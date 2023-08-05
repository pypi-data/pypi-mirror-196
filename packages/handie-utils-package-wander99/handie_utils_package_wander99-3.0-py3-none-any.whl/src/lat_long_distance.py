# © 2022 George Fenn
# Python 3 program to calculate Distance Between Two Points on Earth
# Modified from GeeksforGeeks 
#   https://www.geeksforgeeks.org/program-distance-two-points-earth/
# V2 Changed to raise a RuntimeError Exception when any of the 
# longitudes or any of the latitudes are out of range. 
# V3 Changed the name of the r parameter for the distance method to
# erad for earth radius to make it more readable.

from math import radians, cos, sin, asin, sqrt

def distance(lat1, lat2, lon1, lon2, erad):
	
	if not (-180<=float(lon1)<180):
	  raise RuntimeError('Longitude 1 must be between -180 & 180')
	elif not (-90<=float(lat1)<90):
	  raise RuntimeError('Latitude 1 must be between -90 & 90')
	elif not (-180<=float(lon2)<180):
	  raise RuntimeError('Longitude 2 must be between -180 & 180')
	elif not (-90<=float(lat2)<90):
	  raise RuntimeError('Latitude 2 must be between -90 & 90')
        
	# The math module contains a function named
	# radians which converts from degrees to radians.
	lon1 = radians(float(lon1))
	lon2 = radians(float(lon2))
	lat1 = radians(float(lat1))
	lat2 = radians(float(lat2))
	
	# Haversine formula
	dlon = lon2 - lon1
	dlat = lat2 - lat1
	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2

	c = 2 * asin(sqrt(a))
	
	# calculate the result
	return(c * erad)

# driver code
def main():
	lat1=input('Enter first latitude: ')
	lon1=input('Enter first longitude: ')
	lat2=input('Enter second latitude: ')
	lon2=input('Enter second longitude: ')
	unit=input('Enter distance unit, default is Miles: ')

# Radius of earth in kilometers. Use 3956 for miles
	if unit=='':
		r=3959
		sign='miles'
	elif unit=='k':
		r = 6371
		sign='kilometers'
	try:
	  print(str(distance(lat1,lat2,lon1,lon2,r))+' '+sign)
	except RuntimeError as exc_args:
	  print(exc_args)
	
if __name__ == '__main__':

	main()
