import board as board_class

# unused
	# def sample_more_points(b, num):
	# 	b.sample_points(num)
	# 	b.render_graph()
	# 	from pathlib import Path
	# 	import os
	# 	path = os.getcwd()
	# 	my_file = Path(path+"\\test triangles_points")
	# 	if my_file.is_file():
	# 		# file exists
	# 		text2 = input("Overwrite current points? (enter ""e"")")
	# 	else:
	# 		text2 = input("Save current points? (enter ""e"")")
	# 	if text2 is "e":
	# 		b.save_to_file("test triangles")
	# 		# "_points"
	# 		print("All Saved")
	# 	else:
	# 		print("Board and Points not saved")
	# 	return b

# make functional
def custom_prompt(text, buttons, actions, args, catch):
	response = input(text)
	index = buttons.index(response) if response in buttons else -1
	if index is not -1:
		if args[index] is not None:
			actions[index](args[index])
		else:
			actions[index]()
	else:
		print(catch)



# START HERE ==================================================================================
print("Board")
num_tri = 6
num_points_sampling = 2
possibleAnswers = ['q','w']
new_board = False
text1 = None
# READ FROM LAST FILE?
while text1 not in possibleAnswers:
	text1 = input("Read from last file?(enter ""q"")\n Create new board?(enter ""w"")")
	if text1 is "q":
		b = board_class.board()
		response1 = b.read_board_from_file("test triangles")
		if response1 is -1:
			text1 = None
			continue
		break
	elif text1 is "w":
		b = board_class.board(num_tri)
		b.create_polygons()
		print()
		new_board = True
		break
	else:
		print("\nError, instruction not q or w\n")
b.render_graph()

possibleAnswers = ['e','r']
text2 = None
# SAVE/OVERWRITE CURRENT TRIANGLES?
while text2 not in possibleAnswers:
	if new_board is True:
		text2 = input("Save/Overwrite current triangles? (enter ""e"")\nContinue without saving?(enter ""r"")")
	else:
		break # if I read it in I dont need to save it 
	if text2 is "e":
		b.save_board_to_file("test triangles")
		break
	elif text2 is "r":
		print("Board not saved")
		break
	else:
		print("\nError, instruction not e or r\n")

touched = False
# POINTS ======================================================
print("\nPoints")
text3 = None
possibleAnswers = ['a','s']
# READ POINTS FROM LAST FILE?
if new_board is False:
	while text3 not in possibleAnswers:
		text3 = input("Read points from last file?(enter ""a"")\nContinue?(enter ""s"")")  # invalid if creating new board
		if text3 is "a": # if yes, include them
			response = b.read_points_from_file("test triangles_points")
			if response is -1:
				text3 = None
				continue
			b.render_graph()
			break
		elif text3 is "s":
			print("\nNo File Read\n")
			break
		else:
			print("\nError, instruction not a or s\n")

text4 = None
possibleAnswers = ['a','s']
# SAMPLE MORE POINTS?
while text4 not in possibleAnswers:
	text4 = input("Sample More Points?(enter ""a"")\nContinue?(enter ""s"")") 
	if text4 is "a":
		b.sample_points(num_points_sampling)
		b.render_graph()
		print()
		touched = True
		text4 = None
	elif text4 is "s":
		print("\nNo More Points Added\n")
		break
	else:
		print("\nError, instruction not a or s\n")
# SAVE POINTS AND BOARD?
if touched is True:
	text5 = None
	possibleAnswers = ['e']
	while text5 not in possibleAnswers:
		text5 = input("Save/Overwrite current points AND board? (enter ""e"")\nContinue?(enter ""r"")")
		if text5 is "e":
			b.save_points_to_file("test triangles_points")
			b.save_board_to_file("test triangles")
			break
		elif text5 is "r":
			print("Not Saved")
			break
		else:
			print("\nError, instruction not e or r\n")

# PRM
print("\nPRM Part\n")
text5 = None
possibleAnswers
if b.num_points is not 0:
	b.calculate_prm_parameter()
	print("radius= ", b.r)
	b.PRM()
	b.render_graph()
else:
	print("No points exist")