import matplotlib.pyplot as plt
import matplotlib.patches as mpl_poly
from matplotlib.collections import PatchCollection
import numpy as np
# import GUI # add this in later when compartemtalizing
import Intersect as Intersect


class board:
	def __init__(self):
		# array(1) of other arrays(2)
		# arrays(2) is an array of 3 pairs of points, each pair being a tuple array(3)
		self.polygon_points = []
		
		self.num_poly = 0
		self.edges = 3
		# heuristic for number of triangles to put in
		self.max_density = .7
		self.current_area = 0
		self.total_area = 1
		
		self.area_heuristic_val = 0.7
		# adding extra heuristics is worse than creating a better algorithm to bound triangle areas
		# self.regularity_upper_heuristic = 0.00125
		# self.regularity_lower_heuristic = 0.05
		# self.convexity_heuristic = 90
	
	def create_polygons(self):
		self.current_area = 0
		tryNum = 1
		while self.current_area<self.max_density*self.total_area and self.num_poly<2:
			# print(self.current_area, self.density*self.total_area)
			temp_polygon = np.random.rand(self.edges, 2) # create triangle
			temp_area = self.area(temp_polygon)
			if self.heuristic(temp_polygon, temp_area) is False:
				continue
				# print("area was ", temp_area, "CONTINUE")
				import sys
				sys.exit(0)
			
			print("candidate polygon NUMBER %d try %d:" % (self.num_poly, tryNum), temp_polygon)
			tryNum+=1
			if self.intersect(temp_polygon) is not True:
				tryNum=1
				self.num_poly+=1
				self.polygon_points.append(temp_polygon) # put in graph
				self.current_area = self.current_area + temp_area # update current_area
		
		# DEBUGGING
		if not self.current_area<self.max_density*self.total_area: 
			print("condition area")
		elif not self.num_poly<10:
			print("condition iteration")
	
	def heuristic(self, temp_polygon, temp_area):
		if self.area_heuristic(temp_area) is False:
			return False
		# if temp_area<self.regularity_lower_heuristic or temp_area>self.regularity_upper_heuristic:
		# 	print(temp_area, self.regularity_lower_heuristic, self.regularity_upper_heuristic)
		# 	return False
		# if self.angle(temp_polygon)>self.convexity_heuristic:
		# 	return False
		return True
	
	def area_heuristic(self, temp_area):
		print(temp_area,self.total_area,self.current_area,self.area_heuristic_val)
		if temp_area>((self.total_area-self.current_area)*self.area_heuristic_val): # if it fails the condition
			return False
		return True
	
	def area(self, pts): # take a 3 by 2 array of points and calculates the triangular area
		area = abs(pts[0][0]*(pts[1][1]-pts[2][1]) + pts[1][0]*(pts[2][1]-pts[0][1]) + pts[2][0]*(pts[0][1]-pts[1][1]))/2
		print("area=", area)
		return area
	
	def intersect(self, temp_polygon):
		# patches[0].get_xy()
		if len(self.polygon_points) is 0:
			return False
		# for i in range(len(self.polygon_points)):
		# 	# print("len(self.polygon_points)", len(self.polygon_points))
		# 	if Intersect.PolyOverlaps(temp_polygon, self.polygon_points[i]): # if not an empty array
		# 		return True # return intersect as true
		for polygon in self.polygon_points:
			if Intersect.PolyOverlaps(temp_polygon, polygon): # if not an empty array
				return True # return intersect as true
		# for polygon in self.patches:
		# 	if not len(SA.clip(polygon1.get_xy(), polygon.get_xy())) == 0: # if not an empty array
		# 		return True # return intersect as true
		return False
	
	# def sample_points(n, self):
	# 	self.x.extend(np.random.random(n))
	# 	self.y.extend(np.random.random(n))
	
	def render_graph(self):
		self.fig, self.ax = plt.subplots()
		self.patches = []
		
		# put all polygon_points into patches
		for points in self.polygon_points:
			polygon = mpl_poly.Polygon(points, True)
			self.patches.append(polygon)
		
		# range of visual display
		self.x_range = (-0.00,1.00)
		self.y_range = (-0.00,1.00)
		
		colors = 100*np.random.rand(len(self.patches))
		p = PatchCollection(self.patches, alpha=0.4)
		p.set_array(np.array(colors))
		self.ax.add_collection(p)
		# self.fig.colorbar(p, ax=self.ax)
		plt.show()
	
	# incomplete	
	def save_to_file(self, dir, name):
		import os
		if dir is None:
			path = os.getcwd()
		file = open(os.path.join(path, name+"txt"),"w")
		
		for line in self.polygon_points:
			file.write(line)
			file.write("\n")
		file.close()
	
	# incomplete
	def read_from_file(self, path):
		if len(self.polygon_points) is not 0:
			print()
			text = input("This will overwrite current points\nContinue?(enter ""y"")")
			if text is not "y":
				return
		file = open(path)
		self.polygon_points = []
		for line in file:
			self.polygon_points.append(line)

if __name__ == "__main__":
	print("test area heuristic to make sure calculation is right")
	print("implement convexity_heuristic")
	b = board()
	b.create_polygons()
	b.render_graph()
	# b.save_to_file(None, "pointsFile")
	# b.read_from_file("pointsFile.txt")