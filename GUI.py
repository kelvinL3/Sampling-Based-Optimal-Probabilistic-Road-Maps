# different limitations on polygons
	# area limitation
	# spread(obtuse vs acute)
	# too small? 
		# hard to analyze
		# as more polygons are added, more small polygons will be created
# when do we stop adding polygons?
	# conditionally? 
		# when a sample of straight lines from either side have more than p chance of non intersection with polygons?
	# number? 


# import matplotlib as mp
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpl_poly
from matplotlib.collections import PatchCollection
import Intersect as Intersect

fig, ax = plt.subplots()
patches = []

# TESTING OVERLAP
# xy = [[ 0.42022916,0.17503104],[ 0.61084358,  0.08841899],[ 0.01424765,  0.69477272]]
#  # [(.2,.1),(.4,.3),(.6,.2)]
# patches.append(mpl_poly.Polygon(xy, True))
# xy = [[ 0.33397184 , 0.62561336],[ 0.12316831 , 0.97132741],[ 0.93531812,  0.22693919]]
# patches.append(mpl_poly.Polygon(xy, True))
# xy = [[ 0.36967405 , 0.70385883],[ 0.38377754,  0.99359803],[ 0.31418433 , 0.81352441]]
# patches.append(mpl_poly.Polygon(xy, True))

def area(pts): # take a 3 by 2 array of points and calculates the triangular area
	area = abs(pts[0][0]*(pts[1][1]-pts[2][1]) + pts[1][0]*(pts[2][1]-pts[0][1]) + pts[2][0]*(pts[0][1]-pts[1][1]))/2
	print("area=", area)
	return area


current_area = 0 
total_area = 1
		
# TESTING AREA
xy = [[0, 0],[0.3,0.3],[0,0.3]]
patches.append(mpl_poly.Polygon(xy, True))
area(xy)



# num_poly = 2
# edges = 3
# for i in range(num_poly):
# 	# create polygon
# 	polygon = mpl_poly.Polygon(np.random.rand(edges, 2), closed=False)
# 	# put in graph
# 	patches.append(polygon)
# 	# if i is 0:
# 	# 	p1 = polygon.get_xy()
# 	# elif i is 1:
# 	# 	p2 = polygon.get_xy()

# for polygon in patches:
# 	print(polygon.get_xy())


# density = .5
# area = 1
# while current_area<density*area:
# 	# create triangle
# 	polygon = mpl_poly.Polygon(np.random.rand(edges, 2), True)
# 	if intersect(polygon) is True:
# 		# put in graph
# 		patches.append(polygon)
# 		# update current_area
# 		current_area = current_area + area(polygon)


colors = 100*np.random.rand(len(patches))
p = PatchCollection(patches, alpha=0.4)
p.set_array(np.array(colors))
ax.add_collection(p)
# fig.colorbar(p, ax=ax)

plt.show()
# plt.scatter(x,y)
# plt.xlim(0,1)
# plt.ylim(0,1)
# plt.xlim(-0.01,1.01)
# plt.ylim(-0.01,1.01)
# plt.show()