import matplotlib.pyplot as plt
import matplotlib.patches as mpl_poly
from matplotlib.collections import MPLCollections
import numpy as np
# import GUI # add this in later when compartemtalizing
import Intersect as Intersect
import math
import collections # for nested dictionaries 

import shapely.geometry as SG

class board:
	def __init__(self, max_num_poly=None):
		# array(1) of other arrays(2)
		# arrays(2) is an array of 3 pairs of points, each pair being a tuple array(3)
		self.polygon_points = []
		self.num_poly = 0
		self.max_num_poly = max_num_poly
		self.edges = 3
		
		self.points = []
		self.num_points = 0
		
		self.edges = collections.defaultdict(dict) # nested dictionaries
		self.lines = []
		
		# heuristic for number of triangles to put in
		self.max_density = .7
		self.current_area = 0
		self.total_area = 1
		
		self.area_heuristic_val = 0.7
		# heuristics comments
			# adding extra heuristics is worse than creating a better algorithm to bound triangle areas
				# could use 
			# self.regularity_upper_heuristic = 0.00125
			# self.regularity_lower_heuristic = 0.05
			# self.convexity_heuristic = 90
		
		self.step_size = 0.005
		self.d = 2
		self.r = None
		self.lebesgue = 2
	
	def create_polygons(self):
		if self.max_num_poly is None:
			print("self.max_num_poly is uninitialized")
			import sys
			sys.exit(0)
		self.current_area = 0
		tryNum = 1
		while self.current_area<self.max_density*self.total_area and self.num_poly<self.max_num_poly:
			# print(self.current_area, self.density*self.total_area)
			temp_polygon = np.random.rand(self.edges, 2) # create triangle
			temp_area = self.area(temp_polygon)
			if self.heuristic(temp_polygon, temp_area) is False:
				continue
			# print("candidate polygon NUMBER %d try %d:" % (self.num_poly, tryNum), temp_polygon)
			tryNum+=1
			if self.intersect(temp_polygon) is not True:
				tryNum=1
				self.num_poly+=1
				self.polygon_points.append(temp_polygon) # put in graph
				self.current_area = self.current_area + temp_area # update current_area
		
		# DEBUGGING
		# if not self.current_area<self.max_density*self.total_area: 
		# 	print("condition area")
		# elif not self.num_poly<10:
		# 	print("condition iteration")

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
		# print(temp_area,self.total_area,self.current_area,self.area_heuristic_val)
		if temp_area>((self.total_area-self.current_area)*self.area_heuristic_val*math.exp(-self.num_poly/5)): # if it fails the condition
			return False
		return True

	def area(self, pts):
		return SG.Polygon(pts).area

	def intersect(self, temp_polygon): # if two triangles intersect
		# patches[0].get_xy()
		if len(self.polygon_points) is 0:
			return False
		for polygon in self.polygon_points:
			if SG.Polygon(temp_polygon).intersects(SG.Polygon(polygon)):
				return True
		return False

	def sample_points(self, num_pts):
		self.num_points += num_pts
		for i in range(num_pts):
			# choose point
			pt = self.new_point()
			self.points.append(pt)

	def new_point(self):
		num = 0
		pt = np.random.rand(2)
		while self.legal_point(pt) is False:
			pt = np.random.rand(2)
			num+=1
			if num is 100:
				import sys
				print("TOO DENSE")
				sys.exit(0)
		return pt

	def legal_point(self, point):
		for polygon in self.polygon_points:
			if SG.Polygon(polygon).contains(SG.Point(point)):
				return False
		return True

	def calculate_prm_parameter(self):
		k = 2*pow((1+1/self.d), 1/self.d) * pow((self.lebesgue)/(math.pi), 1/self.d)
		self.r = k * pow(math.log(self.num_points,math.e)/self.num_points, 1/self.d)

	def PRM(self):
		if self.num_points is 0:
			print("\nNo points sampled\n")
			return
		self.calculate_prm_parameter()
		# set up KD tree
		from scipy.spatial import KDTree
		T = KDTree(self.points)
		# calculate edges
		for pt1 in self.points:
			idx = T.query_ball_point(pt,r=self.r)
			for indx2 in idx:
				self.edges[pt1][self.points[indx2]] = True
			# print("In neighborhood of ", pt, ": ", idx)
		
		# go through edges
		for pt1, list2 in d.items():
			for pt2, true in list2.items():
				# TO DO check edge
				if self.connect_two_points(pt1, pt2) is True:
					# TO DO add to plot
					self.lines.append([pt1,pt2])
				try:
					# TO DO remove itself
					del self.edges[pt1][pt2]
				except:
					print("Error A1")
				try:
					# TO DO remove identical one
					del self.edges[pt2][pt1]
				except:
					print("Error A2, not symmetric???1!?")
				

	def connect_two_points(self, pt1, pt2):
		# self.polygon_points
		# PAGE 213 IN PRM.pdf
		d = distance(pt1, pt2)
		num_steps = ceil(d/self.step_size)
		alpha = self.step_size/d
		unit_step = (pt2-pt1)*alpha
		for i in range(1, num_steps):
			# evaluate the point here
			if not self.legal_point(pt1+i*unit_step):
				return False
		return True

	def render_graph(self):
		self.fig, self.ax = plt.subplots()
		self.patches = []
		
		# range of visual display
		self.y_range = (-0.00,1.00)
		self.x_range = (-0.00,1.00)
		
		# put all polygon_points into patches
		for points in self.polygon_points:
			polygon = mpl_poly.Polygon(points, True)
			self.patches.append(polygon)
		
		colors = 100*np.random.rand(len(self.patches))
		p = MPLCollections(self.patches, alpha=0.4)
		p.set_array(np.array(colors))
		self.ax.add_collection(p)
		# self.fig.colorbar(p, ax=self.ax)
		
		# put POINTS into graph
		if len(self.points) is not 0:
			x, y = zip(*self.points)
			plt.scatter(x, y)
		
		# put edges into lines into graph
		
		
		plt.show()

	def save_board_to_file(self, name, dir=None):
		import os
		if dir is None:
			path = os.getcwd()
		file = open(os.path.join(path, name+".txt"),"w")
		
		for line in self.polygon_points:
			for point in line:
				for coor in point:
					file.write(str(coor)+",")
				file.write(";")
			file.write("\n")
		file.close()

	def save_points_to_file(self, name, dir=None):
		# save sampled points, if there are any
		import os
		if dir is None:
			path = os.getcwd()
		if len(self.points) is not 0:
			file = open(os.path.join(path, name+".txt"),"w")
			for line in self.points:
				file.write(str(line)+"\n")

	def read_board_from_file(self, name, dir=None):
		if len(self.polygon_points) is not 0:
			text = input("This will overwrite current points\nContinue?(enter ""y"")")
			if text is not "y":
				return
		import os
		from pathlib import Path
		if dir is None:
			path = os.getcwd()
		try:
			file = open(path + "\\" + name+".txt")
		except:
			print("\nfile not found")
			return -1
		print("Reading from", file.name)
		self.polygon_points = []
		for line in file:
			point_array = np.zeros(shape=(3,2))
			i=0
			line = line[:-2]
			current_line = line.split(";")
			for point in current_line:
				point = point[:-1]
				current_point = point.split(",")
				input_point = []
				for coor in current_point:
					input_point.append(float(coor))
				point_array[i] = input_point
				i+=1
			self.polygon_points.append(point_array)

	def read_points_from_file(self, name, dir=None):
		import os
		from pathlib import Path
		if dir is None:
			path = os.getcwd()
		try: # opening file
			file = open(path+"\\"+name+".txt")
		except:
			print("\nfile not found\n")
			return -1
		print("\nReading from", file.name,"\n")
		try: # reading from file
			for line in file:
				line = line[2:-2]
				self.points.append(np.array(line.split()).astype(float))
				self.num_points += 1
		except:
			print("Error Reading in File")
	
	def print_points(self):
		for line in self.polygon_points:
			print(line)

def distance(p1, p2):
	pow(pow(p1[0]-p2[0],2) + pow(p1[1]-p2[1],2),.5)