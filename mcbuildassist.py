from collections import deque
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
import PIL
from PIL import Image, ImageDraw
from PIL import Image, ImageTk
from load_build import *
import time
import os


#0 = default orientation
#1 = 90 deg CCW
#2 = 180 deg CCW
#3 = 270 deg CCW

mystuff = [0, 1, 2, 3, 4, 5]

class topLevelLoadBuildGUI(object):
	def __init__(self, root, world_names):
		#super().__init__()
		self.root = root
		self.world_names = world_names
		self.selected_world = ""
		self.new_project_name = ""
		self.selected_nw_x = 0
		self.selected_nw_z = 0
		self.selected_se_x = 0
		self.selected_se_z = 0
		self.lowest_y = 0

	def loadButtonCallback(self, event):
		self.selected_world = self.world_select_combobox.get()
		self.new_project_name = self.project_name_text.get("1.0", 'end-1c')
		nw_x = self.nw_x_coord_text.get("1.0", 'end-1c')
		nw_z = self.nw_z_coord_text.get("1.0", 'end-1c')
		se_x = self.se_x_coord_text.get("1.0", 'end-1c')
		se_z = self.se_z_coord_text.get("1.0", 'end-1c')
		y = self.y_text.get("1.0", 'end-1c')
		self.selected_nw_x = int(nw_x)
		self.selected_nw_z = int(nw_z)
		self.selected_se_x = int(se_x)
		self.selected_se_y = int(se_z)
		self.lowest_y = int(y)



	def topLevel(self):
		self.top = Toplevel(self.root)
		self.top.title("Load a Build from a Minecraft World")
		self.base_frame = Frame(self.top)
		part1 = "The purpose of this feature is to allow you to view a build in a Minecraft world from a top-down perspective.\n"
		part2 = "This can be useful when trying to replicate a build done in one particular world elsewhere.\n"
		part3 = "Your build will be saved in a project file, and you can update it in the Minecraft Build Helper by\nsimply loading it again.\n"
		part4 = "To begin:\n"
		part5 = "	1. Find the most NORTHWEST and SOUTHEAST coordinate points and lowest Y-level that encompasses your build.\n	The north-south and east-west distance should not exceed 40 blocks.\n"
		part6 = "	2. Enter the coordinate values, as well as the name of the build (to be used in the project file) and the\n 	name of the Minecraft world in the fields below.\n"
		part7 = "	3. Press the Load button below.\n"
		directions_text = part1 + part2 + part3 + part4 + part5 + part6 + part7
		self.base_frame.grid(column = 0, row = 0)
		self.header = Label(self.base_frame, font=("Arial", 12), text="IMPORTANT! Read all of the following directions to properly use this feature.\n")
		self.directions = Label(self.base_frame, text=directions_text)
		self.input_frame = Frame(self.top)
		world_select_stringvar = StringVar()
		world_select_stringvar.set(self.world_names[0])
		world_select_label = Label(self.input_frame, text="Select a World: ")
		self.world_select_combobox = Combobox(self.input_frame, width=20, textvariable=world_select_stringvar)
		self.world_select_combobox['values'] = self.world_names
		project_name_label = Label(self.input_frame, text="New Project Name: ")
		self.project_name_text = Text(self.input_frame, height=1, width=30)
		nw_x_coord_label = Label(self.input_frame, text="Northwest Block Coordinate X: ")
		self.nw_x_coord_text = Text(self.input_frame, height=1, width=6)
		nw_y_coord_label = Label(self.input_frame, text="Northwest Block Coordinate Z: ")
		self.nw_z_coord_text = Text(self.input_frame, height=1, width=6)
		se_x_coord_label = Label(self.input_frame, text="Southeast Block Coordinate X: ")
		self.se_x_coord_text = Text(self.input_frame, height=1, width=6)
		se_y_coord_label = Label(self.input_frame, text="Southeast Block Coordinate Z: ")
		self.se_z_coord_text = Text(self.input_frame, height=1, width=6)
		y_label = Label(self.input_frame, text="Enter the LOWEST y coordinate of your project: ")
		self.y_text = Text(self.input_frame, height=1, width=6)
		load_button = Button(self.input_frame, text="Load")
		load_button.bind("<Button-1>", self.loadButtonCallback)
		world_select_label.grid(column=0, row=0)
		self.world_select_combobox.grid(column=1, row = 0, columnspan=2)
		project_name_label.grid(column=0, row=2)
		self.project_name_text.grid(column=1, row=2, columnspan=2)
		nw_x_coord_label.grid(column=0, row=3)
		self.nw_x_coord_text.grid(column=1, row=3)
		nw_y_coord_label.grid(column=2, row=3)
		self.nw_z_coord_text.grid(column=3, row=3)
		se_x_coord_label.grid(column=0, row=4)
		self.se_x_coord_text.grid(column=1, row=4)
		se_y_coord_label.grid(column=2, row=4)
		self.se_z_coord_text.grid(column=3, row=4)
		y_label.grid(column=0, row=5)
		self.y_text.grid(column=1, row=5)
		self.header.grid(column=0, row=0)
		self.directions.grid(column=0, row=1)
		self.input_frame.grid(column=0, row=2, sticky=(W))
		load_button.grid(column=0, row=6, columnspan=3)
		self.top.mainloop()

class BlocksHelper(object):

	def __init__(self):
		self.blocks = {}
		self.block_names = []

	def loadBlocks(self):
		image = Image.open("terrain.png")
		width, height = image.size
		print(width)
		print(height)
		x = 0
		y = 0
		block_width = 16
		block_height = 16
		draw_x = 8
		draw_y = 8
		block_data = open("blocks_real.txt")
		loaded_blocks = block_data.readlines()
		for block in loaded_blocks:
			block = block.rstrip('\n').split("-")
			x = int(block[1]) * 16
			y = int(block[2]) * 16
			name = block[0]
			block_image = image.crop((x, y, x + block_width, y + block_height))
			block_image_90_ccw = block_image.rotate(90)
			block_image_180_ccw = block_image.rotate(180)
			block_image_270_ccw = block_image.rotate(270)
			block_image_32x32 = block_image.resize((32, 32))
			block_image_photoimage = ImageTk.PhotoImage(block_image)
			block_image_32x32_photoimage = ImageTk.PhotoImage(block_image_32x32)
			block_image_90_ccw_32x32 = block_image_90_ccw.resize((32, 32))
			block_image_90_ccw_photoimage = ImageTk.PhotoImage(block_image_90_ccw)
			block_image_90_ccw_32x32_photoimage = ImageTk.PhotoImage(block_image_90_ccw_32x32)
			block_image_180_ccw_32x32 = block_image_180_ccw.resize((32, 32))
			block_image_180_ccw_photoimage = ImageTk.PhotoImage(block_image_180_ccw)
			block_image_180_ccw_32x32_photoimage = ImageTk.PhotoImage(block_image_180_ccw_32x32)
			block_image_270_ccw_32x32 = block_image_270_ccw.resize((32, 32))
			block_image_270_ccw_photoimage = ImageTk.PhotoImage(block_image_270_ccw)
			block_image_270_ccw_32x32_photoimage = ImageTk.PhotoImage(block_image_270_ccw_32x32)
			self.blocks[name] = [
				[
				block_image_photoimage,
				block_image_32x32_photoimage,
				],
				[
				block_image_90_ccw_photoimage,
				block_image_90_ccw_32x32_photoimage,
				],
				[
				block_image_180_ccw_photoimage,
				block_image_180_ccw_32x32_photoimage,
				],
				[
				block_image_270_ccw_photoimage,
				block_image_270_ccw_32x32_photoimage,
				]
			]
			self.block_names.append(name)
		image.close()

	def get_block_image(self, block_id):
		return self.getRotatedBlockImage(block_id, 0)

	def getRotatedBlockImage(self, block_id, rotation, zoom_level):
		return self.blocks[self.block_names[block_id]][rotation][zoom_level]


blocks_helper = None

class ZoomHelper(object):
	def __init__(self):
		self.zoom_level = 0
		self.zoom_level_information = [
			{
				"blocks per side": 40,
				"pixels/block": 16,
				"left": 19,
				"right": 20,
				"up": 19,
				"down": 20 
			},
			{
				"blocks per side": 20,
				"pixels/block": 32,
				"left": 9,
				"right": 10,
				"up": 9,
				"down": 10
			},
		]
		self.zoom_square_upper_left_x = 0
		self.zoom_square_upper_left_y = 0
		self.zoom_square_bottom_right_x = 39 
		self.zoom_square_bottom_right_y = 39


	def getBlocksPerSide(self):
		return self.zoom_level_information[self.zoom_level]["blocks per side"]

	def getPixelsPerBlock(self):
		return self.zoom_level_information[self.zoom_level]["pixels/block"]

	def getLeftDist(self):
		return self.zoom_level_information[self.zoom_level]["left"]

	def getRightDist(self):
		return self.zoom_level_information[self.zoom_level]["right"]

	def getUpDist(self):
		return self.zoom_level_information[self.zoom_level]["up"]

	def getDownDist(self):
		return self.zoom_level_information[self.zoom_level]["down"]

	def getZoomSquareUpperLeftX(self):
		return self.zoom_square_upper_left_x

	def getZoomSquareUpperLeftY(self):
		return self.zoom_square_upper_left_y

	def getZoomSquareBottomRightX(self):
		return self.zoom_square_bottom_right_x

	def getZoomSquareBottomRightY(self):
		return self.zoom_square_bottom_right_y

	def getZoomLevel(self):
		return self.zoom_level

	def setZoomLevel(self, zoom_level):
		self.zoom_level = zoom_level

	def setZoomSquareUpperLeftX(self, zoom_square_upper_left_x):
		self.zoom_square_upper_left_x = zoom_square_upper_left_x

	def setZoomSquareUpperLeftY(self, zoom_square_upper_left_y):
		self.zoom_square_upper_left_y = zoom_square_upper_left_y

	def setZoomSquareBottomRightX(self, zoom_square_bottom_right_x):
		self.zoom_square_bottom_right_x = zoom_square_bottom_right_x

	def setZoomSquareBottomRightY(self, zoom_square_bottom_right_y):
		self.zoom_square_bottom_right_y = zoom_square_bottom_right_y

	def shiftZoomWindowRight(self):
		self.zoom_square_upper_left_x += 1
		self.zoom_square_bottom_right_x += 1

	def shiftZoomWindowLeft(self):
		self.zoom_square_upper_left_x -= 1
		self.zoom_square_bottom_right_x -= 1

	def shiftZoomWindowUp(self):
		self.zoom_square_upper_left_y -= 1
		self.zoom_square_bottom_right_y -= 1

	def shiftZoomWindowDown(self):
		self.zoom_square_upper_left_y += 1
		self.zoom_square_bottom_right_y += 1

	def getZoomInCoordinates(self, zoom_x, zoom_y):
		print("Zooming in on (" + str(zoom_x) + ", " + str(zoom_y) + ")")
		self.zoom_level += 1
		topleft_x = 0
		topleft_y = 0
		bottomright_x = 0
		bottomright_y = 0
		if zoom_x + self.getRightDist() <= 39 and zoom_x - self.getLeftDist() >= 0:
			topleft_x = zoom_x - self.getLeftDist()
			bottomright_x = zoom_x + self.getRightDist()
		else:
			if zoom_x + self.getRightDist() > 39:
				bottomright_x = 39
				topleft_x = zoom_x - (self.getLeftDist() + (self.getRightDist() - (39 - zoom_x)))
			elif zoom_x - self.getLeftDist() < 0:
				topleft_x = 0
				bottomright_x = zoom_x + self.getRightDist() + (self.getLeftDist() - zoom_x)
			else:
				print("Error")
		if zoom_y + self.getDownDist() <= 39 and zoom_y - self.getUpDist() >= 0:
			bottomright_y = zoom_y + self.getDownDist()
			topleft_y = zoom_y - self.getUpDist()
		else:
			if zoom_y + self.getDownDist() > 39:
				bottomright_y = 39
				topleft_y = zoom_y - (self.getUpDist() + (self.getDownDist() - (39 -zoom_y)))				
			elif zoom_y - self.getUpDist() < 0:
				topleft_y = 0
				bottomright_y = zoom_y + self.getDownDist() + (self.getUpDist() - zoom_y)
			else:
				print("Error")
		self.zoom_square_upper_left_x = topleft_x
		self.zoom_square_upper_left_y = topleft_y
		self.zoom_square_bottom_right_x = bottomright_x
		self.zoom_square_bottom_right_y = bottomright_y
		#print("Upper left: (" + str(self.zoom_square_upper_left_x) + ", " + str(self.zoom_square_upper_left_y) + ")")
		#print("Lower right: (" + str(self.zoom_square_bottom_right_x) + ", " + str(self.zoom_square_bottom_right_y) + ")")

	def getZoomOutCoordinates(self, zoom_x, zoom_y):
		print("Zooming out at (" + str(zoom_x) + ", " + str(zoom_y))
		self.zoom_level -= 1
		if zoom_x + self.getRightDist() <= 39 and zoom_x - self.getLeftDist() >= 0:
			topleft_x = zoom_x - self.getLeftDist()
			bottomright_x = zoom_x + self.getRightDist()
		else:
			if zoom_x + self.getRightDist() > 39:
				bottomright_x = 39
				topleft_x = zoom_x - (self.getLeftDist() + (self.getRightDist() - (39 - zoom_x)))
			elif zoom_x - self.getLeftDist() < 0:
				topleft_x = 0
				bottomright_x = zoom_x + self.getRightDist() + (self.getLeftDist() - zoom_x)
			else:
				print("????")				
		if zoom_y + self.getDownDist() <= 39 and zoom_y - self.getUpDist() >= 0:
			bottomright_y = zoom_y + self.getDownDist()
			topleft_y = zoom_y - self.getUpDist()
		else:
			if zoom_y + self.getDownDist() > 39:
				bottomright_y = 39
				topleft_y = zoom_y - (self.getUpDist() + (self.getDownDist() - (39 -zoom_y)))				
			elif zoom_y - self.getUpDist() < 0:
				topleft_y = 0
				bottomright_y = zoom_y + self.getDownDist() + (self.getUpDist() - zoom_y)
			else:
				print("?????")
		self.zoom_square_upper_left_x = topleft_x
		self.zoom_square_upper_left_y = topleft_y
		self.zoom_square_bottom_right_x = bottomright_x
		self.zoom_square_bottom_right_y = bottomright_y
		print("Upper left: (" + str(self.zoom_square_upper_left_x) + ", " + str(self.zoom_square_upper_left_y) + ")")
		print("Lower right: (" + str(self.zoom_square_bottom_right_x) + ", " + str(self.zoom_square_bottom_right_y) + ")")

class MCBuildHelper(Frame):

	def __init__(self, root):
		super().__init__()
		self.blocks = {}
		self.block_thumbnails = {}
		self.block_tallies = {}
		self.block_names = []
		self.blocks_raw = {}
		self.block_tallies_raw = {}
		self.prev_quickselect = None
		self.quickselect_blocks = []
		self.raw_mode_checkbox_var = IntVar()
		self.raw_mode_checkbox_var.set(0)
		self.canvas_width = 640
		self.canvas_height = 640
		self.top = None
		self.root = root
		self.toplevel_replacer_block_select = None
		self.toplevel_replacee_block_select = None
		self.toplevel_replace_mode = IntVar()
		self.current_block_id = 0
		self.current_layer = 0
		self.current_project_index = None
		self.current_project_filepath = None
		self.current_project_file = None
		self.current_project_name = None
		self.project_modified = False
		self.grid_size = 40
		self.layer0 = [["*" for col in range(self.grid_size)] for row in range(self.grid_size)]
		self.layer1 = [["*" for col in range(self.grid_size)] for row in range(self.grid_size)]
		self.layer2 = [["*" for col in range(self.grid_size)] for row in range(self.grid_size)]
		self.layer3 = [["*" for col in range(self.grid_size)] for row in range(self.grid_size)]
		self.layer4 = [["*" for col in range(self.grid_size)] for row in range(self.grid_size)]
		self.layers = [self.layer0, self.layer1, self.layer2, self.layer3, self.layer4]
		self.layer_names = ["Layer 1", "Layer 2", "Layer 3", "Layer 4", "Layer 5"]
		self.prev_selected_x = None
		self.prev_selected_y = None
		self.selected_x = None
		self.selected_y = None
		self.block_orientation = 1;
		#0 = default
		#1 = rotated 90 degrees clockwise
		#2 = rotated 180 degrees clockwise
		#3 = rotated 270 degrees clockwise
		self.select_anchor_1 = None
		self.select_anchor_2 = None
		self.selected_blocks = []
		self.first_movement = True
		self.copied_blocks = []
		erase_img = Image.open("erase.png")
		self.erase_image = ImageTk.PhotoImage(erase_img)
		selected_img = Image.open("selected.png")
		self.selected_image = ImageTk.PhotoImage(selected_img)
		self.mode = 0
		#0 = place
		#1 = erase
		#2 = select
		self.submit_button_command = 0
		#0 = rename project
		#1 = new project 
		self.enter_text_area_hidden = True
		self.quick_select_block_indices = deque()
		self.selected_blocks_rotation_degrees = 0
		self.world_names = self.getMinecraftWorldNames()
		self.load_toplevel = None
		self.world_select_combobox = None
		self.project_name_text = None
		self.nw_x_coord_text = None
		self.nw_z_coord_text = None
		self.se_x_coord_text = None
		self.se_z_coord_text = None
		self.y_text = None
		self.zoom_helper = ZoomHelper()
		self.x_views_stringvar = StringVar(value=["1 to 40"])
		self.x_view = None
		self.y_views = ["40 to 40"]
		self.x_scrollbar_prev_x0 = 0
		self.y_views_stringvar = StringVar(value=["1 to 40"])
		self.y_view = None
		self.y_views = ["40 to 40"]
		self.y_scrollbar_prev_x0 = 0
		self.isScrolledX = False
		self.isScrolledY = False
		self.x_labels = []
		self.y_labels = []
		self.loadBlocks()
		self.loadRawBlockTotals()
		self.initializeUI()

	def getBlock(self, x, y, layer):
		return layer[y][x][0]

	def getBlockRotation(self, x, y, layer):
		return layer[y][x][1]

	def setBlock(self, x, y, _id, layer, rotation):
		layer[y][x] = [_id, rotation]; 

	def get_canvas_width(self):
		return self.canvas_width

	def get_canvas_height(self):
		return self.canvas_height

	def get_current_block_image(self):
		return blocks_helper.getRotatedBlockImage(self.current_block_id, 0, self.zoom_helper.getZoomLevel())

	def get_block_image(self, block_id):
		return blocks_helper.getRotatedBlockImage(block_id, 0, self.zoom_helper.getZoomLevel())

	def getRotatedBlockImage(self, block_id, rotation):
		return blocks_helper.getRotatedBlockImage(block_id, rotation, self.zoom_helper.getZoomLevel())

	def quitApplication(self, event):
		print("Quitting the application...")
		if self.project_modified:
			if messagebox.askokcancel("Quit", "Are you sure you want to quit? You have unsaved changes."):
				self.root.destroy()
		else:
			self.root.destroy()

	def loadBlocks(self):
		block_data = open("blocks_real.txt")
		loaded_blocks = block_data.readlines()
		for block in loaded_blocks:
			block = block.rstrip('\n').split("-")
			name = block[0]
			self.block_names.append(name)

	def loadRawBlockTotals(self):
		blocks_raw = open("blocks_raw.txt")
		loaded_raw_blocks = blocks_raw.readlines()
		for block in loaded_raw_blocks:
			block = block.rstrip('\n').split("-")
			block_name = block[0]
			recipe = block[1]
			craft_amount = int(block[2])
			ingredients = recipe.split("*")
			ingredients_dict = {}
			for ingredient in ingredients:
				count = int(ingredient[0:2])
				ingredient_name = ingredient[2:]
				#print(str(count) + " " + ingredient_name)
				ingredients_dict[ingredient_name] = count
			self.blocks_raw[block_name] = {
											"ingredients": ingredients_dict,
											"craftable amount": craft_amount
										}

	def toggleRawBlockTallies(self):
		mode = self.raw_mode_checkbox_var.get()
		if self.current_project_filepath is None:
			messagebox.showerror("Error", "Please select a project or create a new one")
		else:
			self.writeTallies()

	def convert_coords(self, coord):
		return ((coord - (coord % self.zoom_helper.getPixelsPerBlock())) / self.zoom_helper.getPixelsPerBlock()) + 1

	def updateTallies(self, block_id):
		block_name = self.block_names[block_id]
		raw_ingredients = self.blocks_raw[block_name]["ingredients"]
		if block_name in self.block_tallies:
			self.block_tallies[block_name] += 1
		else:
			self.block_tallies[block_name] = 1
		print(self.block_tallies)
		#ACTIVE DEVELOPMENT SITE
		self.block_tallies_raw = {}
		for block in self.block_tallies:
			print("Block: " + block)
			num_blocks = self.block_tallies[block]
			print("Num existing blocks: " + str(num_blocks))
			craft_amount = self.blocks_raw[block]["craftable amount"]
			print("Craft amount: " + str(craft_amount))
			ingredients_multiplier = num_blocks // craft_amount
			if num_blocks % craft_amount != 0:
				ingredients_multiplier += 1
			ingredients = self.blocks_raw[block]["ingredients"]
			for ingredient in ingredients:
				if ingredient in self.block_tallies_raw:
					self.block_tallies_raw[ingredient] += (ingredients_multiplier * ingredients[ingredient])
				else:
					self.block_tallies_raw[ingredient] = (ingredients_multiplier * ingredients[ingredient])
		print(self.block_tallies_raw)
		self.writeTallies()

	def drawBlockByCoords(self, real_x, real_y):
		layer = self.layers[self.current_layer]
		preexisting_block_id = self.getBlock(real_x, real_y, layer)
		if preexisting_block_id != self.current_block_id:
			self.setBlock(real_x, real_y, self.current_block_id, layer, 0)
			block_name = self.block_names[self.current_block_id]
			self.updateTallies(self.current_block_id)
			print(self.block_tallies_raw)
			if self.current_block_id not in self.quickselect_blocks:
				if len(self.quickselect_blocks) < 6:
					self.quickselect_blocks.append(self.current_block_id)
				else:
					self.quickselect_blocks = self.quickselect_blocks[1:6]
					self.quickselect_blocks.append(self.current_block_id)
				self.updateQuickSelect()
			print(self.quickselect_blocks)


	def deleteBlockByCoords(self, real_x, real_y):
		layer = self.layers[self.current_layer]
		block_name = self.block_names[self.getBlock(real_x, real_y, layer)]
		if block_name in self.block_tallies:
			self.block_tallies[block_name] -= 1
			if self.block_tallies[block_name] == 0:
				del self.block_tallies[block_name]
		self.setBlock(real_x, real_y, '*', layer, None)
		raw_ingredients = self.blocks_raw[block_name]
		for ingredient in raw_ingredients:
			self.block_tallies_raw[ingredient] -= raw_ingredients[ingredient]
			if self.block_tallies_raw[ingredient] <= 0:
				del self.block_tallies_raw[ingredient]

	def click(self, event):
		if not self.current_project_name:
			messagebox.showerror("Error", "Please select a project or create a new one")
			return
		real_x = self.zoom_helper.getZoomSquareUpperLeftX() + int(self.convert_coords(event.x)) - 1
		real_y = self.zoom_helper.getZoomSquareUpperLeftY() + int(self.convert_coords(event.y)) - 1
		#print("real x: " + str(real_x))
		#print("real y: " + str(real_y))
		converted_x = (self.convert_coords(event.x) - 1) * self.zoom_helper.getPixelsPerBlock()
		converted_y = (self.convert_coords(event.y) - 1) * self.zoom_helper.getPixelsPerBlock()
		#print("Converted x: " + str(converted_x))
		#print("Converted y: " + str(converted_y))
		layer = self.layers[self.current_layer]
		if self.mode == 0:
			self.project_modified = True
			self.toggleSaveButtonBackground()
			current_block_image = self.get_current_block_image()
			self.canvas.create_image(converted_x, converted_y, anchor=NW, image=current_block_image)
			print(self.convert_coords(event.x))
			print(self.convert_coords(event.y))
			self.drawBlockByCoords(real_x, real_y)
		elif self.mode == 1:
			self.project_modified = True
			self.toggleSaveButtonBackground()
			self.canvas.create_image(converted_x + 1, converted_y + 1, anchor=NW, image=self.erase_image)
			self.deleteBlockByCoords(real_x, real_y)
			self.writeTallies()
		elif self.mode == 2:
			self.canvas.create_image(converted_x + 1, converted_y + 1, anchor=NW, image=self.selected_image)
			if not self.prev_selected_x and not self.prev_selected_y:
				self.prev_selected_x = real_x
				self.prev_selected_y = real_y
			else:
				self.prev_selected_x = self.selected_x
				self.prev_selected_y = self.selected_y
				#print("prev selected x: " + str(self.prev_selected_x))
				#print("prev selected y: " + str(self.prev_selected_y))
				if(self.getBlock(self.prev_selected_x, self.prev_selected_y, layer) != '*'):
					prev_block_id = self.getBlock(self.prev_selected_x, self.prev_selected_y, layer)
					rotation = self.getBlockRotation(self.prev_selected_x, self.prev_selected_y, layer)
					prev_block_img = self.getRotatedBlockImage(prev_block_id, rotation)
					self.canvas.create_image((self.prev_selected_x * 16), (self.prev_selected_y * 16), anchor=NW, image=prev_block_img)
				else:
					self.canvas.create_image((self.prev_selected_x * 16) + 1, (self.prev_selected_y * 16) + 1, anchor=NW, image=self.erase_image)
			self.selected_x = real_x
			self.selected_y = real_y
			self.canvas.create_image((self.selected_x * 16) + 1, (self.selected_y * 16) + 1, anchor=NW, image=self.selected_image)

	def right_click(self, event):
		if self.mode == 2:
			real_x = self.zoom_helper.getZoomSquareUpperLeftX() + int(self.convert_coords(event.x)) - 1
			real_y = self.zoom_helper.getZoomSquareUpperLeftY() + int(self.convert_coords(event.y)) - 1
			#print("real x: " + str(real_x))
			#print("real y: " + str(real_y))
			converted_x = (self.convert_coords(event.x) - 1) * self.zoom_helper.getPixelsPerBlock()
			converted_y = (self.convert_coords(event.y) - 1) * self.zoom_helper.getPixelsPerBlock()
			#print("Converted x: " + str(converted_x))
			#print("Converted y: " + str(converted_y))
			self.canvas.create_oval(converted_x - 2, converted_y - 2, converted_x + 2, converted_y + 2, fill="red")
			if self.select_anchor_1 == None:
				self.select_anchor_1 = [real_x, real_y]
			else:
				self.select_anchor_2 = [real_x, real_y]
				self.selectBox(self.select_anchor_1[0], self.select_anchor_1[1], self.select_anchor_2[0], self.select_anchor_2[1])

	def select(self, x1, y1, x2, y2):
		self.selected_blocks = []
		layer = self.layers[self.current_layer]
		if x2 > x1 and y2 > y1:
			for i in range(y1, y2):
				for j in range(x1, x2):
					if self.getBlock(j, i, layer) != '*':
						block_info = [i, j, self.getBlock(j, i, layer), self.getBlockRotation(j, i, layer)]
						self.selected_blocks.append(block_info)
		elif x1 > x2 and y2 > y1:
			for i in range(y1, y2):
				for j in range(x2, x1):
					if self.getBlock(j, i, layer) != '*':
						block_info = [i, j, self.getBlock(j, i, layer), self.getBlockRotation(j, i, layer)]
						self.selected_blocks.append(block_info)
		elif x1 > x2 and y1 > y2:
			for i in range(y2, y1):
				for j in range(x2, x1):
					if self.getBlock(j, i, layer) != '*':
						block_info = [i, j, self.getBlock(j, i, layer), self.getBlockRotation(j, i, layer)]
						self.selected_blocks.append(block_info)
		elif x2 > x1 and y1 > y2:
			for i in range(y2, y1):
				for j in range(x1, x2):
					if self.getBlock(j, i, layer) != '*':	
						block_info = [i, j, self.getBlock(j, i, layer), self.getBlockRotation(j, i, layer)]
						self.selected_blocks.append(block_info)

	def drawSelectionBox(self, x1, y1, x2, y2):
		self.canvas.create_line(x1 * 16, y1 * 16, x2 * 16, y1 * 16, fill="red", width=3) #draw top of box
		self.canvas.create_line(x1 * 16, y1 * 16, x1 * 16, y2 * 16, fill="red", width=3) #draw left side of box
		self.canvas.create_line(x1 * 16, y2 * 16, x2 * 16, y2 * 16, fill="red", width=3) #draw bottom of box
		self.canvas.create_line(x2 * 16, y1 * 16, x2 * 16, y2 * 16, fill="red", width=3) #draw right side of box

	def selectBox(self, x1, y1, x2, y2):
		self.clearAndRedrawCanvas()
		self.drawSelectionBox(x1, y1, x2, y2)
		self.select(x1, y1, x2, y2)
		
	def undoSelectionBoxManual(self):
		layer = self.layers[self.current_layer]
		if self.first_movement == False:
			for block in self.selected_blocks:
				x = block[1]
				y = block[0]
				_id = block[2]
				rotation = block[3]
				if self.getBlock(x, y, layer) == '*':
					#print("Block at x = " + str(x) + " y = " + str(y))
					self.setBlock(x, y, _id, layer, rotation)
				else:
					self.deleteBlockByCoords(x, y)
					self.setBlock(x, y, _id, layer, rotation)
				self.writeTallies()
		if self.select_anchor_1 is not None and self.select_anchor_2 is not None:
			self.select_anchor_1 = None
			self.select_anchor_2 = None
			self.selected_blocks = []
			self.clearAndRedrawCanvas()
		self.first_movement = True

	def undoSelectionBox(self, event):
		self.undoSelectionBoxManual()

	def deleteSelection(self):
		if self.mode != 2 or len(self.selected_blocks) == 0:
			return
		else:
			layer = self.layers[self.current_layer]
			for block in self.selected_blocks:
				x = block[1]
				y = block[0]
				block_id = block[2]
				self.deleteBlockByCoords(x, y)
			self.writeTallies()
			self.undoSelectionBoxManual()

	def moveSelection(self, key):
		if self.mode != 2 or len(self.selected_blocks) == 0:
			return
		layer = self.layers[self.current_layer]
		if key == 0:
			if self.select_anchor_1[0] > 0 and self.select_anchor_2[0] > 0:
				self.select_anchor_1[0] -= 1
				self.select_anchor_2[0] -= 1
				for block in self.selected_blocks:
					if self.first_movement:
						self.setBlock(block[1], block[0], '*', layer, None)
					block[1] -= 1
				self.first_movement = False
		elif key == 1:
			if self.select_anchor_1[0] < self.grid_size and self.select_anchor_2[0] < self.grid_size:
				self.select_anchor_1[0] += 1
				self.select_anchor_2[0] += 1
				for block in self.selected_blocks:
					if self.first_movement:
						self.setBlock(block[1], block[0], '*', layer, None)
					block[1] += 1
				self.first_movement = False
		elif key == 2:
			if self.select_anchor_1[1] > 0 and self.select_anchor_2[1] > 0:
				self.select_anchor_1[1] -= 1
				self.select_anchor_2[1] -= 1
				for block in self.selected_blocks:
					if self.first_movement:
						self.setBlock(block[1], block[0], '*', layer, None)
					block[0] -= 1
				self.first_movement = False
		elif key == 3:
			if self.select_anchor_1[1] < self.grid_size and self.select_anchor_2[1] < self.grid_size:
				self.select_anchor_1[1] += 1
				self.select_anchor_2[1] += 1
				for block in self.selected_blocks:
					if self.first_movement:
						self.setBlock(block[1], block[0], '*', layer, None)
					block[0] += 1
				self.first_movement = False
		self.clearAndRedrawCanvas()
		self.drawSelectionBox(self.select_anchor_1[0], self.select_anchor_1[1], self.select_anchor_2[0], self.select_anchor_2[1])
		for block in self.selected_blocks:
			y = block[0]
			x = block[1]
			_id = block[2]
			rotation = block[3]
			image = self.getRotatedBlockImage(_id, rotation)
			self.canvas.create_image(x * 16, y * 16, anchor=NW, image=image)

	def flipSelection(self, mode):
		#mode = 0 horizontal
		#mode = 1 vertical
		if self.mode != 2 or len(self.selected_blocks) == 0:
			return
		else:
			left = min(self.select_anchor_1[0], self.select_anchor_2[0])
			right = max(self.select_anchor_1[0], self.select_anchor_2[0]) - 1
			top = min(self.select_anchor_1[1], self.select_anchor_2[1])
			bottom = max(self.select_anchor_1[1], self.select_anchor_2[1]) - 1
			for block in self.selected_blocks:
				y = block[0]
				x = block[1]
				_id = block[2]
				if mode == 0:
					dist_from_right = right - x
					flipped_x = left + dist_from_right
					if self.first_movement == True:
						self.layers[self.current_layer][y][x] = '*'
					block[1] = flipped_x
				elif mode == 1:
					dist_from_bottom = bottom - y
					flipped_y = top + dist_from_bottom
					if self.first_movement == True:
						self.layers[self.current_layer][y][x] = '*'
					block[0] = flipped_y					
			self.first_movement = False
			self.clearAndRedrawCanvas()
			self.drawSelectionBox(self.select_anchor_1[0], self.select_anchor_1[1], self.select_anchor_2[0], self.select_anchor_2[1])
			for block in self.selected_blocks:
				image = self.getRotatedBlockImage(block[2], block[3])
				self.canvas.create_image(block[1] * 16, block[0] * 16, anchor=NW, image=image)

	def placebutton_click(self, event):
		if self.mode == 2:
			self.undoSelectionBoxManual()
		self.mode = 0

	def erasebutton_click(self, event):
		if self.mode == 2:
			self.undoSelectionBoxManual()
		self.mode = 1

	def selectbutton_click(self, event):
		self.mode = 2

	def block_selected(self, event):
		selection = self.block_select.get()
		self.current_block_id = self.block_names.index(selection)
		print(self.current_block_id)

	def layer_selected(self, event):
		selection = self.layer_select.get()
		self.current_layer = self.layer_names.index(selection)
		self.zoom_helper.setZoomLevel(0)
		self.zoom_helper.setZoomSquareUpperLeftX(0)
		self.zoom_helper.setZoomSquareUpperLeftY(0)
		self.zoom_helper.setZoomSquareBottomRightX(39)
		self.zoom_helper.setZoomSquareBottomRightY(39)
		self.setXView()
		self.setYView()
		self.isScrolledX = False
		self.isScrolledY = False
		self.switchLayers()

	def clearCanvas(self):
		self.canvas.delete(ALL)
		self.canvas.create_rectangle(0, 0, self.canvas_width, self.canvas_height, fill='#FFFFFF')
		x = 0
		y = 0
		for i in range(0, self.zoom_helper.getBlocksPerSide()):
			self.canvas.create_line(x, 0, x, self.canvas_height)
			x += self.zoom_helper.getPixelsPerBlock()
		for i in range(0, self.zoom_helper.getBlocksPerSide()):
			self.canvas.create_line(0, y, self.canvas_width, y)
			y += self.zoom_helper.getPixelsPerBlock()

	def switchLayers(self):
		self.clearCanvas()
		self.drawPreviousLayerOutline()
		current_layer_arr = self.layers[self.current_layer]
		x = 0
		y = 0
		for i in range(self.zoom_helper.getZoomSquareUpperLeftY(), self.zoom_helper.getZoomSquareBottomRightY() + 1):
			for j in range(self.zoom_helper.getZoomSquareUpperLeftX(), self.zoom_helper.getZoomSquareBottomRightX() + 1):
				cell = self.getBlock(j, i, current_layer_arr)
				if cell != "*":
					rotation = self.getBlockRotation(j, i, current_layer_arr)
					block = self.getRotatedBlockImage(cell, rotation)
					self.canvas.create_image(x * self.zoom_helper.getPixelsPerBlock(), y * self.zoom_helper.getPixelsPerBlock(), anchor=NW, image=block)
				x += 1
			x = 0
			y += 1

	def drawPreviousLayerOutline(self):
		scale = self.zoom_helper.getPixelsPerBlock()
		if self.current_layer == 0:
			return
		else:
			layer = self.layers[self.current_layer - 1]
			for i in range(self.zoom_helper.getZoomSquareUpperLeftY(), self.zoom_helper.getZoomSquareBottomRightY()):
				for j in range(self.zoom_helper.getZoomSquareUpperLeftX(), self.zoom_helper.getZoomSquareBottomRightX()):
					if self.getBlock(j, i, layer) != '*':
						self.canvas.create_rectangle(j * scale, i * scale, (j * scale) + scale, (i * scale) + scale, fill="#c9d1cb")

	def clearAndRedrawCanvas(self):
		self.switchLayers()

	def doNothing(self):
		print("Doing nothing...")

	def clearText(self):
		self.enter_text.delete(1.0, END)

	def getProjectFilepath(self, name):
		return os.getcwd() + "\\projects\\" + name + ".txt"

	def openTextAreaForNewProject(self, event):
		self.toggleEnterTextArea()
		self.submit_button_command = 1

	def openTextAreaForRenaming(self, event):
		self.toggleEnterTextArea()
		self.submit_button_command = 0

	def closeTextArea(self, event):
		self.clearText()
		self.toggleEnterTextArea()

	def writeTallies(self):
		self.block_names_list.delete(1.0, END)
		self.block_tallies_list.delete(1.0, END)
		blocks = ""
		tallies = ""
		if self.raw_mode_checkbox_var.get() == 0:
			self.warning_label.grid_remove()
			for (key, value) in self.block_tallies.items():
				if len(key) > 20:
					key = key[0:17] + "..."
				blocks = blocks + key + "\n"
				tallies = tallies + str(value) + "\n"
		else:
			self.warning_label.grid(column=0, row=2, columnspan=3, sticky=W)
			for (key, value) in self.block_tallies_raw.items():
				if len(key) > 20:
					key = key[0:17] + "..."
				blocks = blocks + key + "\n"
				tallies = tallies + str(value) + "\n"
		self.block_names_list.insert(1.0, blocks)
		self.block_tallies_list.insert(1.0, tallies)

	def toggleEnterTextArea(self):
		if self.enter_text_area_hidden:
			self.enter_text_frame.grid(column = 0, row = 3)
			self.enter_text_area_hidden = False
		else:
			self.enter_text_frame.grid_remove()
			self.enter_text_area_hidden = True

	def toggleSaveButtonBackground(self):
		if self.project_modified:
			self.save_button.configure(text = "*Save")
		else:
			self.save_button.configure(text = "Save")

	def saveProject(self):
		print("Saving project...")
		if not self.current_project_filepath:
			messagebox.showerror(f"Error", "No project currently selected.")
			return False
		project_file_exists = os.path.exists(self.current_project_filepath)
		if not project_file_exists:
			messagebox.showerror(f"Error", "Could not open project {self.current_project_name}. This could be because the file was deleted or moved.")
			return False
		project_file = open(self.current_project_filepath, "w")
		num_layers = len(self.layer_names)
		project_file.write(str(num_layers) + "\n")
		for i in range(0, len(self.layers)):
			layer = self.layers[i]
			for y in range(0, len(layer)):
				row = layer[y]
				for x in range(0, len(row)):
					if row[x] != '*':
						block_id = self.getBlock(x, y, layer)
						rotation = self.getBlockRotation(x, y, layer)
						block_information = str(block_id) + "-" + str(i) + "-" + str(y) + "-" + str(x) + "-" + str(rotation) + '\n'
						project_file.write(block_information)
		project_file.close()
		self.project_modified = False
		self.toggleSaveButtonBackground()

	def submitButtonCallback(self, event):
		if self.submit_button_command == 1:
			self.newProject()
		elif self.submit_button_command == 0:
			if self.current_project_index != None:
				text = self.enter_text.get("1.0", 'end-1c')
				if self.validateNewProjectName(text, True):
					self.renameProject()
			else:
				messagebox.showerror(f"Error", "No project currently selected. Please try again.")

	def renameProject(self):
		self.project_modified = True
		self.toggleSaveButtonBackground()
		new_name = self.current_project_name
		index = self.current_project_index
		cwd = os.getcwd()
		fullpath = cwd + "\\projects\\"
		original_name = self.projects_list.get(index)
		os.rename(fullpath + original_name + ".txt", fullpath + new_name + ".txt")
		self.projects_list.delete(index)
		self.projects_list.insert(index, new_name)

	def newProject(self):
		text = self.enter_text.get("1.0", 'end-1c')
		if not self.validateNewProjectName(text, True):
			print("Invalid project")
		else:
			self.projects.append(self.current_project_name)
			self.current_project_index = len(self.projects) + 1
			self.projects_list.insert(END, self.current_project_name)
			self.current_project_file = open(self.current_project_filepath, "w")
			self.block_tallies = {}
			self.writeTallies()
			self.saveProject()

	def saveProjectEvent(self, event):
		self.saveProject()

	def loadProjectNames(self):
		cwd = os.getcwd()
		fullpath = cwd + "\\projects\\"
		projects = os.listdir(fullpath)
		return_result = []
		for project in projects:
			return_result.append(project[0:-4])
		return return_result

	def loadProject(self):
		if not self.current_project_filepath:
			messagebox.showerror(f"Error", "No project currently selected.")
			return False
		project_file_exists = os.path.exists(self.current_project_filepath)
		if not project_file_exists:
			messagebox.showerror(f"Error", "Could not open project {self.current_project_name}. This could be because the file was deleted or moved.")
			return False
		file = open(self.current_project_filepath, "r")
		num_layers = int(file.readline())
		new_layer_names = []
		for i in range(1, num_layers + 1):
			layer_name = "Layer " + str(i)
			new_layer_names.append(layer_name)
		self.layer_names = new_layer_names
		new_layers = []
		for i in range(0, num_layers):
			loaded_layer = [["*" for col in range(40)] for row in range(40)]
			new_layers.append(loaded_layer)
		self.layers = new_layers
		self.layer_select['values'] = self.layer_names
		self.delete_layer_select['values'] = self.layer_names
		blocks = file.readlines()
		self.block_tallies_raw = {}
		for line in blocks:
			line = line.rstrip('\n')
			components = line.split('-')
			block_id = int(components[0])
			layer_index = int(components[1])
			y = int(components[2])
			x = int(components[3])
			rotation = int(components[4])
			self.setBlock(x, y, block_id, self.layers[layer_index], rotation)
			name = self.block_names[block_id]
			block_image = self.getRotatedBlockImage(block_id, rotation)
			if(self.current_layer == layer_index):
				self.canvas.create_image(x * 16, y * 16, anchor=NW, image=block_image)
			if name in self.block_tallies:
				self.block_tallies[name] += 1
			else:
				self.block_tallies[name] = 1
			raw_ingredients = self.blocks_raw[name]["ingredients"]
			for ingredient in raw_ingredients:
				if ingredient in self.block_tallies_raw:
					self.block_tallies_raw[ingredient] += raw_ingredients[ingredient]
				else:
					self.block_tallies_raw[ingredient] = raw_ingredients[ingredient]
		self.writeTallies()
		file.close()

	def clearAllLayers(self):
		for layer in self.layers:
			for y in range(0, 40):
				for x in range(0, 40):
					self.setBlock(x, y, '*', layer, None)

	def addNewLayer(self, event):
		if not self.current_project_filepath:
			messagebox.showerror(f"Error", "No project currently selected.")
		else:
			self.project_modified = True
			self.toggleSaveButtonBackground()
			num_layers = len(self.layers)
			new_layer_name = "Layer " + str(num_layers + 1)
			new_layer = [["*" for col in range(40)] for row in range(40)]
			self.layer_names.append(new_layer_name)
			self.layers.append(new_layer)
			self.layer_select['values'] = self.layer_names
			self.delete_layer_select['values'] = self.layer_names
			print(self.layer_names)

	def deleteLayer(self, event):
		if not self.current_project_filepath:
			messagebox.showerror(f"Error", "No project currently selected.")
		elif len(self.layer_names) == 1:
			messagebox.showerror(f"Error", "Must have at least one layer in a project.")
		else:
			selection = self.delete_layer_select.get()
			layer_to_delete_index = self.layer_names.index(selection)			
			layer = self.layers[layer_to_delete_index]
			for i in range(0, len(layer)):
				for j in range(0, len(layer[i])):
					if self.getBlock(j, i, layer) != '*':
						block_name = self.block_names[int(self.getBlock(j, i, layer))]
						self.block_tallies[block_name] -= 1
			self.writeTallies()
			del self.layer_names[layer_to_delete_index]
			print(self.layer_names)
			del self.layers[layer_to_delete_index]
			if layer_to_delete_index == self.current_layer:
				if self.current_layer > 0:
					self.current_layer -= 1
			self.layer_select['values'] = self.layer_names
			self.delete_layer_select['values'] = self.layer_names
			self.layer_select.set(self.layer_names[self.current_layer])
			self.delete_layer_select.set(self.layer_names[self.current_layer])
			self.switchLayers()
			self.project_modified = True
			self.toggleSaveButtonBackground()


	def selectProject(self, event):
		self.selectProjectManual()

	def selectProjectManual(self):
		if self.project_modified:
			if messagebox.askyesnocancel("Switch Projects", "Current project modified. Would you like to save your changes before switching?"):
				print
				self.saveProject()
				self.project_modified = False
				self.toggleSaveButtonBackground()
			else:
				pass
		if self.current_project_file != None:
			self.current_project_file.close()
		self.clearAllLayers()
		self.clearCanvas()
		print(self.projects_list.curselection())
		self.current_project_index = self.projects_list.curselection()[0]
		self.current_project_name = self.projects[self.current_project_index]
		self.current_project_filepath = self.getProjectFilepath(self.current_project_name)
		self.block_tallies = {}
		self.loadProject()

	def validateNewProjectName(self, name, update): #if update = True, do not check if a project with that name already exists. Otherwise, check and return error if a project with that name exists
		print(name)
		if len(name) <= 0 or len(name) > 30:
			messagebox.showerror("Error", "Project name must be between 0 and 30 characters.")
			return False
		cwd = os.getcwd()
		fullpath = cwd + "\\projects\\" + name + ".txt"
		print(fullpath)
		project_exists = os.path.exists(fullpath)
		if update:
			if project_exists:
				messagebox.showerror("Error", "A project with that name already exists.")
				return False
		for char in name:
			if not char.isalpha() and not char.isdigit() and char != '_' and char != '-':
				messagebox.showerror("Error", "Please only use letters, numbers, underscores, or dashes in the project name.")
				return False
		self.current_project_filepath = fullpath
		self.current_project_name = name
		return True

	def deleteProject(self):
		selected_project_index = self.projects_list.curselection()[0]
		self.projects_list.delete(selected_project_index)
		self.clearCanvas()
		if os.path.exists(self.current_project_filepath):
			os.remove(self.current_project_filepath)
		self.clearAllLayers()
		self.current_project_filepath = None
		self.current_project_name = None
		self.current_project_index = None
		self.current_project_file = None
		self.block_tallies = {}
		self.writeTallies()

	def dialogBoxTest(self, event):
		if len(self.projects_list.curselection()) != 0:
			answer = messagebox.askyesnocancel("Question", "Delete project?")
			if answer:
				self.deleteProject()

	def motion(self, event):
		real_x = self.zoom_helper.getZoomSquareUpperLeftX() + int(self.convert_coords(event.x)) - 1
		real_y = self.zoom_helper.getZoomSquareUpperLeftY() + int(self.convert_coords(event.y)) - 1
		if real_x >= 40:
			real_x = 39
		if real_y >= 40:
			real_y = 39
		position_string = "(" + str(real_x + 1) + ", " + str(40 - real_y) + ")"
		self.mouse_grid_position.delete(0, END)
		self.mouse_grid_position.insert(0, position_string)
		layer = self.layers[self.current_layer]
		block_id = self.getBlock(real_x, real_y, layer)
		current_entry_contents = self.currently_selected_block_entry.get()
		if block_id == '*':
			if current_entry_contents != " ":
				self.currently_selected_block_entry.delete(0, END)
				self.currently_selected_block_entry.insert(0, " ")
		else:
			block_name = self.block_names[block_id]
			if(current_entry_contents != block_name):
				self.currently_selected_block_entry.delete(0, END)
				self.currently_selected_block_entry.insert(0, block_name)

	def topLevelClose(self, event):
		if self.top is not None:
			self.top.destroy()

	def replaceBlocks(self, event):
		mode = self.toplevel_replace_mode.get()
		if mode == 0:
			messagebox.showerror(f"Error", "Please select a replacement mode first.")
		else:
			replacee_block = self.toplevel_replacee_block_select.get()
			replacer_block = self.toplevel_replacer_block_select.get()
			replacee_block_index = self.block_names.index(replacee_block)
			replacer_block_index = self.block_names.index(replacer_block)
			replacer_block_image = self.get_block_image(replacer_block_index)
			num_replacements = 0
			if mode == 1:
				layer = self.layers[self.current_layer]
				for i in range(0, len(self.layers[self.current_layer])):
					for j in range(0, len(self.layers[self.current_layer][i])):
						if self.getBlock(j, i, self.layers[self.current_layer]) == replacee_block_index:
							self.setBlock(j, i, replacer_block_index, self.layers[self.current_layer], 0)
							draw_x = i * 16
							draw_y = j * 16
							num_replacements += 1
							self.canvas.create_image(draw_y, draw_x, anchor=NW, image=replacer_block_image)
				self.block_tallies[replacee_block] -= num_replacements
				if self.block_tallies[replacee_block] <= 0:
					del self.block_tallies[replacee_block]
				if replacer_block in self.block_tallies:
					self.block_tallies[replacer_block] += num_replacements
				else:
					self.block_tallies[replacer_block] = num_replacements
				self.writeTallies()
			self.project_modified = True
			self.toggleSaveButtonBackground()

	def topLevelReplaceBlocks(self):
		self.top = Toplevel(self.root)
		self.top.title("Replace Blocks")
		base_frame = Frame(self.top)
		base_frame.grid(column = 0, row = 0)
		optionlist = self.block_names
		bl1_initial_block_option = StringVar()
		bl1_initial_block_option.set("Andesite")
		replacee_block_label = Label(base_frame, text="Replace ")
		self.toplevel_replacee_block_select = Combobox(base_frame, width=20, textvariable=bl1_initial_block_option)
		print(list(self.block_tallies.keys()))
		self.toplevel_replacee_block_select['values'] = list(self.block_tallies.keys())
		bl2_initial_block_option = StringVar()
		bl2_initial_block_option.set("Andesite")
		replacer_block_label = Label(base_frame, text = " With ")
		self.toplevel_replacer_block_select = Combobox(base_frame, width=20, textvariable=bl2_initial_block_option)
		self.toplevel_replacer_block_select['values'] = optionlist
		quit_button = Button(base_frame, text="Cancel")
		quit_button.bind("<Button-1>", self.topLevelClose)
		replace_button = Button(base_frame, text="Replace")
		replace_button.bind("<Button-1>", self.replaceBlocks)
		radiobutton_layer = Radiobutton(base_frame, text="Replace in currently selected layer only", variable=self.toplevel_replace_mode, value=1)
		radiobutton_all = Radiobutton(base_frame, text="Replace throughout entire project", variable=self.toplevel_replace_mode, value=2)
		replacee_block_label.grid(column = 0, row = 0)
		self.toplevel_replacee_block_select.grid(column = 1, row = 0)
		replacer_block_label.grid(column = 2, row = 0)
		self.toplevel_replacer_block_select.grid(column = 3, row = 0)
		radiobutton_layer.grid(column = 0, row = 1, columnspan = 4, sticky=W)
		radiobutton_all.grid(column = 0, row = 2, columnspan = 4, sticky=W)
		quit_button.grid(column = 3, row = 3, sticky=W)
		replace_button.grid(column = 1, row = 3, sticky=W)
		self.top.mainloop()

	def rotateSingleBlock(self):
		if self.mode != 2 or not self.selected_x or not self.selected_y:
			return
		else:
			layer = self.layers[self.current_layer]
			block_id = self.getBlock(self.selected_x, self.selected_y, layer)
			rotation = self.getBlockRotation(self.selected_x, self.selected_y, layer)
			if rotation == 3:
				rotation = 0
			else:
				rotation += 1
			self.setBlock(self.selected_x, self.selected_y, block_id, layer, rotation)
			image = self.getRotatedBlockImage(block_id, rotation)
			self.canvas.create_image(self.selected_x * 16, self.selected_y * 16, anchor=NW, image=image)

	def rotateSelection(self):
		selection_width = abs(self.select_anchor_1[0] - self.select_anchor_2[0])
		selection_height = abs(self.select_anchor_1[1] - self.select_anchor_2[1])
		layer = self.layers[self.current_layer]
		topleft_x = min(self.select_anchor_1[0], self.select_anchor_2[0])
		topleft_y = min(self.select_anchor_1[1], self.select_anchor_2[1])
		middle_x = 0
		middle_y = 0
		if selection_width % 2 == 0:
			middle_x = topleft_x + (selection_width / 2) - 1
		else:
			middle_x = topleft_x + (selection_width - 1) / 2

		if selection_height % 2 == 0:
			middle_y = topleft_y + (selection_height / 2) - 1
		else:
			middle_y = topleft_y + (selection_height - 1) / 2
		current_bottom_left_ycoord = max(self.select_anchor_1[1], self.select_anchor_2[1]) - 1
		current_bottom_left_xcoord = min(self.select_anchor_1[0], self.select_anchor_2[0])
		current_top_right_ycoord = min(self.select_anchor_1[1], self.select_anchor_2[1])
		current_top_right_xcoord = max(self.select_anchor_1[0], self.select_anchor_2[0]) - 1
		new_topleft_x = middle_x - (current_bottom_left_ycoord - middle_y)
		new_topleft_y = middle_y - (middle_x - current_bottom_left_xcoord)
		new_bottomright_x = middle_x + (middle_y - current_top_right_ycoord) + 1
		new_bottomright_y = middle_y + (current_top_right_xcoord - middle_x) + 1
		if self.selected_blocks_rotation_degrees < 270:
			self.selected_blocks_rotation_degrees += 90
		else:
			self.selected_blocks_rotation_degrees = 0
		for i in range(0, len(self.selected_blocks)):
			block = self.selected_blocks[i]
			original_x = block[1]
			original_y = block[0]
			new_x = new_topleft_x + (current_bottom_left_ycoord - original_y)
			new_y = new_topleft_y + (original_x - current_bottom_left_xcoord)
			if self.first_movement:
				print(block[0])
				print(block[1])
				self.setBlock(block[1], block[0], '*', layer, None)
			self.selected_blocks[i][1] = int(new_x)
			self.selected_blocks[i][0] = int(new_y)
		self.first_movement = False
		self.clearAndRedrawCanvas()
		for block in self.selected_blocks:
			img = self.getRotatedBlockImage(block[2], block[3]) #block[2] = id, block[3] = rotation
			self.canvas.create_image(block[1] * 16, block[0] * 16, anchor=NW, image=img)
		self.select_anchor_1 = [new_topleft_x, new_topleft_y]
		self.select_anchor_2 = [new_bottomright_x, new_bottomright_y]
		self.drawSelectionBox(new_topleft_x, new_topleft_y, new_bottomright_x, new_bottomright_y)
		

	def copySelection(self):
		topleft_selection_x = min(self.select_anchor_1[0], self.select_anchor_2[0])
		topleft_selection_y = min(self.select_anchor_1[1], self.select_anchor_2[1])
		bottomright_selection_x = max(self.select_anchor_1[0], self.select_anchor_2[0])
		bottomright_selection_y = max(self.select_anchor_1[1], self.select_anchor_2[1])
		layer = self.layers[self.current_layer]
		for y in range(topleft_selection_y, bottomright_selection_y):
			for x in range(topleft_selection_x, bottomright_selection_x):
				if layer[y][x] != '*':
					block_id = self.getBlock(x, y, layer)
					block_info = [y, x, self.getBlock(x, y, layer), self.getBlockRotation(x, y, layer)]
					self.copied_blocks.append(block_info)

	def pasteSelection(self):		
		if len(self.copied_blocks) == 0:
			return
		topleft_x = 41
		topleft_y = 41
		bottomright_x = 0
		bottomright_y = 0
		xcoords = []
		ycoords = []
		for block in self.copied_blocks:
			y = block[0]
			x = block[1]
			block_id = block[2]
			self.updateTallies(block_id)
			xcoords.append(x)
			ycoords.append(y)
		self.undoSelectionBoxManual()
		self.first_movement = False
		topleft_x = min(xcoords)
		topleft_y = min(ycoords)
		bottomright_x = max(xcoords) + 1
		bottomright_y = max(ycoords) + 1
		self.select_anchor_1 = [topleft_x, topleft_y]
		self.select_anchor_2 = [bottomright_x, bottomright_y]
		self.select(topleft_x, topleft_y, bottomright_x, bottomright_y)
		self.drawSelectionBox(topleft_x, topleft_y, bottomright_x, bottomright_y)

	def getMinecraftWorldNames(self):
		filepath = "C:\\Users\\benja\\AppData\\Roaming\\.minecraft\\saves\\"
		list_directory_contents = os.listdir(filepath)
		return list_directory_contents

	def loadBuildButtonCallback(self, event):
		print("Load button clicked...")
		selected_world = self.world_select_combobox.get()
		new_project_name = self.project_name_text.get("1.0", 'end-1c')
		nw_x = self.nw_x_coord_text.get("1.0", 'end-1c')
		nw_z = self.nw_z_coord_text.get("1.0", 'end-1c')
		se_x = self.se_x_coord_text.get("1.0", 'end-1c')
		se_z = self.se_z_coord_text.get("1.0", 'end-1c')
		y = self.y_text.get("1.0", 'end-1c')
		num_pattern = re.compile("[-]?[0-9]{1,7}")
		y_pattern = re.compile("[0-9]{1,3}")
		match_nw_x = num_pattern.fullmatch(nw_x)
		match_nw_z = num_pattern.fullmatch(nw_z)
		match_se_x = num_pattern.fullmatch(se_x)
		match_se_z = num_pattern.fullmatch(se_z)
		match_y = y_pattern.fullmatch(y)
		if not match_nw_x or not match_nw_z or not match_se_x or not match_se_z or not match_y:
			messagebox.showerror("Error", "Invalid coordinate(s) entered. Please enter numbers in integer (not decimal) form. Y coordinate cannot be less than 0.")
		else:
			selected_nw_x = int(nw_x)
			selected_nw_z = int(nw_z)
			selected_se_x = int(se_x)
			selected_se_z = int(se_z)
			if selected_nw_x >= selected_se_x or selected_nw_z >= selected_se_z:
				messagebox.showerror("Error", "Northwest x coordinate should be less than southeast x coordinate, and northwest z coordinate should be less than southeast z coordinate.")
			elif abs(selected_se_x - selected_nw_x) > 40 or abs(selected_se_z - selected_nw_z) > 40:
				messagebox.showerror("Error", "Selection should not greater than 40 blocks by 40 blocks in XZ area.")
			elif not self.validateNewProjectName(new_project_name, False):
				print("Invalid project name.")
			else:
				lowest_y = int(y)
				load_return = load_main(selected_nw_x, selected_nw_z, selected_se_x, selected_se_z, lowest_y, selected_world, new_project_name)
				if load_return.getStatus() == "SUCCESS":
					if new_project_name not in self.projects:
						self.projects_list.insert(END, new_project_name)
						self.projects.append(new_project_name)
					new_project_index = self.projects.index(new_project_name)
					self.projects_list.select_set(new_project_index)
					self.top.destroy()
					self.top = None
					self.selectProjectManual()
				else:
					error_message = load_return.getErrorMessage()
					error_code = load_return.getErrorCode()
					compiled_error_message = "ERROR CODE " + str(error_code) + ": " + error_message
					messagebox.showerror("Error", compiled_error_message)

	def cancelLoadButtonCallback(self, event):
		self.top.destroy()
		self.top = None


	def loadBuildCallback(self, event):
		self.top = Toplevel(self.root)		
		self.top.title("Load a Build from a Minecraft World")
		base_frame = Frame(self.top)
		part1 = "The purpose of this feature is to allow you to view a build in a Minecraft world from a top-down perspective.\n"
		part2 = "This can be useful when trying to replicate a build done in one particular world elsewhere.\n"
		part3 = "Your build will be saved in a project file, and you can update it in the Minecraft Build Helper by\nsimply loading it again.\n"
		part4 = "To begin:\n"
		part5 = "	1. Find the most NORTHWEST and SOUTHEAST coordinate points and lowest Y-level that encompasses your build.\n	The north-south and east-west distance should not exceed 40 blocks.\n"
		part6 = "	2. Enter the coordinate values, as well as the name of the build (to be used in the project file) and the\n 	name of the Minecraft world in the fields below.\n"
		part7 = "	3. Press the Load button below.\n"
		directions_text = part1 + part2 + part3 + part4 + part5 + part6 + part7
		base_frame.grid(column = 0, row = 0)
		header = Label(base_frame, font=("Arial", 12), text="IMPORTANT! Read all of the following directions to properly use this feature.\n")
		directions = Label(base_frame, text=directions_text)
		input_frame = Frame(base_frame)
		world_select_stringvar = StringVar()
		world_select_stringvar.set(self.world_names[0])
		world_select_label = Label(input_frame, text="Select a World: ")
		self.world_select_combobox = Combobox(input_frame, state="readonly", width=20, textvariable=world_select_stringvar)
		self.world_select_combobox['values'] = self.world_names
		project_name_label = Label(input_frame, text="New Project Name: ")
		self.project_name_text = Text(input_frame, height=1, width=30)
		nw_x_coord_label = Label(input_frame, text="Northwest Block Coordinate X: ")
		self.nw_x_coord_text = Text(input_frame, height=1, width=6)
		nw_z_coord_label = Label(input_frame, text="Northwest Block Coordinate Z: ")
		self.nw_z_coord_text = Text(input_frame, height=1, width=6)
		se_x_coord_label = Label(input_frame, text="Southeast Block Coordinate X: ")
		self.se_x_coord_text = Text(input_frame, height=1, width=6)
		se_z_coord_label = Label(input_frame, text="Southeast Block Coordinate Z: ")
		self.se_z_coord_text = Text(input_frame, height=1, width=6)
		y_label = Label(input_frame, text="Lowest Y coordinate of your project: ")
		self.y_text = Text(input_frame, height=1, width=6)
		button_frame = Frame(base_frame)
		load_button = Button(button_frame, text="Load")
		load_button.bind("<Button-1>", self.loadBuildButtonCallback)
		cancel_button = Button(button_frame, text="Cancel")
		cancel_button.bind("<Button-1>", self.cancelLoadButtonCallback)
		world_select_label.grid(column=0, row=0)
		self.world_select_combobox.grid(column=1, row = 0, columnspan=2)
		project_name_label.grid(column=0, row=2, pady=(10, 0))
		self.project_name_text.grid(column=1, row=2, columnspan=2, pady=(10, 0))
		nw_x_coord_label.grid(column=0, row=3, pady=(10, 10))
		self.nw_x_coord_text.grid(column=1, row=3, pady=(10, 10))
		nw_z_coord_label.grid(column=2, row=3, pady=(10, 10))
		self.nw_z_coord_text.grid(column=3, row=3)
		se_x_coord_label.grid(column=0, row=4, pady=(0, 10))
		self.se_x_coord_text.grid(column=1, row=4, pady=(0, 10))
		se_z_coord_label.grid(column=2, row=4, pady=(0, 10))
		self.se_z_coord_text.grid(column=3, row=4, pady=(0, 10))
		y_label.grid(column=0, row=5)
		self.y_text.grid(column=1, row=5)
		header.grid(column=0, row=0)
		directions.grid(column=0, row=1)
		input_frame.grid(column=0, row=2, sticky=(W))
		load_button.grid(column=0, row=0, padx=(10, 10))
		cancel_button.grid(column=1, row=0, padx=(10, 10))
		button_frame.grid(column=0, row=3, pady=(20,20))
		self.top.mainloop()

	def optionMenuHandler(self, value):
		print(value)
		self.edit_dropdown_stringvar.set("Advanced Editing")
		if value == "Replace Blocks":
			if self.current_project_filepath is None:
				messagebox.showerror("Error", "Please select a project or create a new one first.")
			else:
				self.topLevelReplaceBlocks()
		elif value == "Delete Selected":
			self.deleteSelection()
		elif value == "Flip Horizontally":
			self.flipSelection(0)
		elif value == "Flip Vertically":
			self.flipSelection(1)
		elif value == "Copy":
			if len(self.selected_blocks) > 0:
				self.copySelection()
		elif value == "Paste":
			if len(self.copied_blocks) > 0:
				self.pasteSelection()
		elif value == "Rotate 90 deg. CW":
			if len(self.selected_blocks) > 0:
				self.rotateSelection()

	def clearQuickSelect(self):
		self.quick_select_slot1.create_rectangle(0, 0, 18, 18, fill='white')
		self.quick_select_slot2.create_rectangle(0, 0, 18, 18, fill='white')
		self.quick_select_slot3.create_rectangle(0, 0, 18, 18, fill='white')
		self.quick_select_slot4.create_rectangle(0, 0, 18, 18, fill='white')
		self.quick_select_slot5.create_rectangle(0, 0, 18, 18, fill='white')
		self.quick_select_slot6.create_rectangle(0, 0, 18, 18, fill='white')		

	def updateQuickSelect(self):
		print("Updating quick select bar...")
		self.clearQuickSelect()
		for i in range(0, len(self.quickselect_blocks)):
			image = self.get_block_image(self.quickselect_blocks[i])
			if i == 0:
				self.quick_select_slot1.create_image(2, 2, anchor=NW, image=image)
			elif i == 1:
				self.quick_select_slot2.create_image(2, 2, anchor=NW, image=image)
			elif i == 2:
				self.quick_select_slot3.create_image(2, 2, anchor=NW, image=image)
			elif i == 3:
				self.quick_select_slot4.create_image(2, 2, anchor=NW, image=image)
			elif i == 4:
				self.quick_select_slot5.create_image(2, 2, anchor=NW, image=image)
			elif i == 5:
				self.quick_select_slot6.create_image(2, 2, anchor=NW, image=image)

	def manageQuickSelect(self, key):
		if key > len(self.quickselect_blocks):
			return
		if self.prev_quickselect is not None:
			image = self.get_block_image(self.quickselect_blocks[self.prev_quickselect - 1])
			if self.prev_quickselect == 1:
				self.quick_select_slot1.create_image(2, 2, anchor=NW, image=image)
			elif self.prev_quickselect == 2:
				self.quick_select_slot2.create_image(2, 2, anchor=NW, image=image)
			elif self.prev_quickselect == 3:
				self.quick_select_slot3.create_image(2, 2, anchor=NW, image=image)
			elif self.prev_quickselect == 4:
				self.quick_select_slot4.create_image(2, 2, anchor=NW, image=image)
			elif self.prev_quickselect == 5:
				self.quick_select_slot5.create_image(2, 2, anchor=NW, image=image)
			elif self.prev_quickselect == 6:
				self.quick_select_slot6.create_image(2, 2, anchor=NW, image=image)
		if key == 1:
			self.quick_select_slot1.create_image(2, 2, anchor=NW, image=self.selected_image)
			self.prev_quickselect = 1
		elif key == 2:
			self.quick_select_slot2.create_image(2, 2, anchor=NW, image=self.selected_image)
			self.prev_quickselect = 2
		elif key == 3:
			self.quick_select_slot3.create_image(2, 2, anchor=NW, image=self.selected_image)
			self.prev_quickselect = 3
		elif key == 4:
			self.quick_select_slot4.create_image(2, 2, anchor=NW, image=self.selected_image)
			self.prev_quickselect = 4
		elif key == 5:
			self.quick_select_slot5.create_image(2, 2, anchor=NW, image=self.selected_image)
			self.prev_quickselect = 5
		elif key == 6:
			self.quick_select_slot6.create_image(2, 2, anchor=NW, image=self.selected_image)
			self.prev_quickselect = 6
		block_index = self.quickselect_blocks[key - 1]
		self.block_select.current(block_index)
		self.current_block_id = block_index


	def handleKeyPresses(self, event):
		key = event.char
		if key in ["1", "2", "3", "4", "5", "6"]:
			if(int(key) > len(self.quickselect_blocks)):
				return
			self.manageQuickSelect(int(key))
		elif key == "d":
			self.deleteSelection()
		elif key == "h":
			self.flipSelection(0)
		elif key == "v":
			self.flipSelection(1)
		elif key == "r":
			if len(self.selected_blocks) > 0:
				self.rotateSelection()
			else:
				self.rotateSingleBlock()
		elif key == "c":
			if len(self.selected_blocks) > 0:
				self.copySelection()
		elif key == "p":
			self.pasteSelection()
		else:
			print("Key: --" + key + "--")

	def leftArrowKey(self, event):
		self.moveSelection(0)

	def rightArrowKey(self, event):
		self.moveSelection(1)

	def upArrowKey(self, event):
		self.moveSelection(2)

	def downArrowKey(self, event):
		self.moveSelection(3)

	def quickSelect1(self, event):
		self.manageQuickSelect(1)
		
	def quickSelect2(self, event):
		self.manageQuickSelect(2)
		
	def quickSelect3(self, event):
		self.manageQuickSelect(3)

	def quickSelect4(self, event):
		self.manageQuickSelect(4)

	def quickSelect5(self, event):
		self.manageQuickSelect(5)

	def quickSelect6(self, event):
		self.manageQuickSelect(6)	

	def zoomScaleTextOut(self):
		for i in range(0, 40):
			self.x_labels[i].config(text=str(i + 1))
			self.y_labels[i].config(text=str(40 - i))

	def zoomScaleTextIn(self):
		x_start = self.zoom_helper.getZoomSquareUpperLeftX() + 1
		y_start = self.zoom_helper.getZoomSquareUpperLeftY() + 1
		for i in range(0, len(self.x_labels)):
			if i % 2 == 0:
				if x_start < 10:
					new_label_text = "  " + str(x_start)
				else:
					new_label_text = str(x_start)
				if i < 9:
					self.x_labels[i].config(text=new_label_text)
				else:
					new_label_text = new_label_text + " "
					self.x_labels[i].config(text=new_label_text)
				x_start += 1
				self.y_labels[i].config(text=str(41-y_start))
				y_start += 1
			else:
				if i < 9:
					self.x_labels[i].config(text="")
				else:
					self.x_labels[i].config(text="   ")
				self.y_labels[i].config(text="")

	def setXView(self):
		interval = self.zoom_helper.getBlocksPerSide()
		start = 1
		end = interval
		iterations = (40 - interval) + 1
		views = []
		for i in range(0, iterations):
			view_string = str(start) + " to " + str(end)
			start += 1
			end += 1
			views.append(view_string)
		self.x_views_stringvar.set(views)	
		upper_left_x = self.zoom_helper.getZoomSquareUpperLeftX()
		self.x_view.yview_scroll(upper_left_x, PAGES)

	def setYView(self):
		interval = self.zoom_helper.getBlocksPerSide()
		start = 1
		end = interval
		iterations = (40 - interval) + 1
		views = []
		for i in range(0, iterations):
			view_string = str(start) + " to " + str(end)
			start += 1
			end += 1
			views.append(view_string)
		self.y_views_stringvar.set(views)	
		upper_left_y = self.zoom_helper.getZoomSquareUpperLeftY()
		self.y_view.yview_scroll(upper_left_y, PAGES)
		
	def setXScrollbarTest(self):
		self.canvas_x_scrollbar.set(0.19047619047619047, 0.23809523809523808)

	def canvasMouseWheelCallback(self, event):
		real_x = self.zoom_helper.getZoomSquareUpperLeftX() + int(self.convert_coords(event.x)) - 1
		real_y = self.zoom_helper.getZoomSquareUpperLeftY() + int(self.convert_coords(event.y)) - 1
		if real_x >= 40:
			real_x = 39
		if real_y >= 40:
			real_y = 39
		if event.delta < 0:
			if self.zoom_helper.zoom_level > 0:
				self.isScrolledX = False
				self.isScrolledY = False
				self.zoom_helper.getZoomOutCoordinates(real_x, real_y)
				self.zoomScaleTextOut()
				self.clearAndRedrawCanvas()
				self.setXView()
				self.setYView()
		else:
			if self.zoom_helper.zoom_level < 1:
				self.isScrolledX = False
				self.isScrolledY = False
				self.zoom_helper.getZoomInCoordinates(real_x, real_y)
				self.zoomScaleTextIn()
				self.clearAndRedrawCanvas()
				self.setXView()
				self.setYView()
		
	def canvasXScrollCommandHandler(self, x0, x1):
		if self.isScrolledX:
			if x0 > self.x_scrollbar_prev_x0:
				self.zoom_helper.shiftZoomWindowRight()
				self.clearAndRedrawCanvas()
			elif x0 < self.x_scrollbar_prev_x0:
				self.zoom_helper.shiftZoomWindowLeft()
				self.clearAndRedrawCanvas()
			else:
				print("Equal???")
			self.x_scrollbar_prev_x0 = x0
			self.zoomScaleTextIn()
		else:
			self.x_scrollbar_prev_x0 = x0
		self.canvas_x_scrollbar.set(x0, x1)
		self.isScrolledX = True

	def canvasYScrollCommandHandler(self, y0, y1):
		if self.isScrolledY:
			if y0 > self.y_scrollbar_prev_x0:
				self.zoom_helper.shiftZoomWindowDown()
				self.clearAndRedrawCanvas()
			elif y0 < self.y_scrollbar_prev_x0:
				self.zoom_helper.shiftZoomWindowUp()
				self.clearAndRedrawCanvas()
			else:
				print("Equal???")
			self.y_scrollbar_prev_x0 = y0
			self.zoomScaleTextIn()
		else:
			self.y_scrollbar_prev_x0 = y0
		self.canvas_y_scrollbar.set(y0, y1)
		self.isScrolledY = True

	def initializeUI(self):
		print("Yay")
		self.master.title("Minecraft Build Helper")
		base_frame = Frame(self)
		self.root.bind("<Left>", self.leftArrowKey)
		self.root.bind("<Down>", self.downArrowKey)
		self.root.bind("<Right>", self.rightArrowKey)
		self.root.bind("<Up>", self.upArrowKey)
		self.root.bind("<KeyPress>", self.handleKeyPresses)
		self.root.bind("<Escape>", self.undoSelectionBox)
		base_frame.grid(column = 0, row = 0)
		self.canvas = Canvas(base_frame, width = self.canvas_width, height = self.canvas_height, background="white")
		self.canvas.bind("<MouseWheel>", self.canvasMouseWheelCallback)
		self.x_scale_frame = Frame(base_frame)
		self.y_scale_frame = Frame(base_frame)	
		for i in range(0, 40):
			new_x_label = Label(self.x_scale_frame, text=str(i + 1))
			if i < 9:
				new_x_label.grid(column=i, row=0, sticky=(W, E), padx=3)
			else:
				new_x_label.grid(column=i, row=0, sticky=(W, E))
			self.x_labels.append(new_x_label)
		for i in range(0, 40):
			new_y_label = Label(self.y_scale_frame, font=("Arial", 7), text=str((40-i)))
			if i < 9:
				new_y_label.grid(column=0, row=i, sticky=(W, E))
			else:
				new_y_label.grid(column=0, row=i, sticky=(W, E))
			self.y_labels.append(new_y_label)
		self.x_view = Listbox(base_frame, height=1, listvariable=self.x_views_stringvar, exportselection=False)
		x_view_label = Label(base_frame, text="X span: ")
		self.canvas_x_scrollbar = Scrollbar(base_frame, orient=HORIZONTAL, command=self.x_view.yview)
		self.x_view['yscrollcommand'] = self.canvasXScrollCommandHandler
		y_view_label = Label(base_frame, text="Y span: ")
		self.y_view = Listbox(base_frame, height=1, listvariable=self.y_views_stringvar, exportselection=False)
		self.canvas_y_scrollbar = Scrollbar(base_frame, orient=VERTICAL, command=self.y_view.yview)
		self.y_view['yscrollcommand'] = self.canvasYScrollCommandHandler
		self.canvas.bind("<Button-1>", self.click)
		self.canvas.bind("<Motion>", self.motion)
		self.canvas.bind("<Button-3>", self.right_click)
		x = 0
		y = 0
		for i in range(0, 40):
			self.canvas.create_line(x, 0, x, 640)
			x += 16
		for i in range(0, 40):
			self.canvas.create_line(0, y, 640, y)
			y += 16
		self.toolbar = LabelFrame(base_frame, text='Toolbar')
		self.place_button = Button(self.toolbar, text="Place Blocks")
		self.place_button.bind("<Button-1>", self.placebutton_click)
		self.erase_button = Button(self.toolbar, text="Erase Blocks")
		self.erase_button.bind("<Button-1>", self.erasebutton_click)
		self.select_button = Button(self.toolbar, text="Select Block")
		self.select_button.bind("<Button-1>", self.selectbutton_click)
		optionlist = self.block_names
		self.initial_block_option = StringVar()
		self.initial_block_option.set("Andesite")
		block_label = Label(self.toolbar, text="Block: ")
		self.block_select = Combobox(self.toolbar, width=30, textvariable=self.initial_block_option, state="readonly")
		self.block_select['values'] = optionlist
		self.block_select.bind("<<ComboboxSelected>>", self.block_selected)
		self.initial_layer_option = StringVar()
		self.initial_layer_option.set("Layer 1")
		self.layer_select = Combobox(self.toolbar, width=10, textvariable=self.initial_layer_option)
		self.layer_select['values'] = self.layer_names
		self.layer_select.bind("<<ComboboxSelected>>", self.layer_selected)
		layer_label = Label(self.toolbar, text="Layer: ")
		self.save_button = Button(self.toolbar, text="Save")
		self.save_button.bind("<Button-1>", self.saveProjectEvent)
		self.new_layer_button = Button(self.toolbar, text="New Layer")
		self.new_layer_button.bind("<Button-1>", self.addNewLayer)
		self.clear_layer_button = Button(self.toolbar, text="Load Build")
		self.clear_layer_button.bind("<Button-1>", self.loadBuildCallback)
		delete_layer_label = Label(self.toolbar, text="Delete Layer: ")
		self.delete_layer_initial_layer_option = StringVar()
		self.delete_layer_initial_layer_option.set("Layer 1")
		self.delete_layer_select = Combobox(self.toolbar, width=10, textvariable=self.delete_layer_initial_layer_option, state="readonly")
		self.delete_layer_select['values'] = self.layer_names
		self.delete_layer_select.bind("<<ComboboxSelected>>", self.deleteLayer)
		dropdown_options = ["Advanced Editing", "Copy", "Paste", "Replace Blocks", "Delete Selected", "Flip Horizontally", "Flip Vertically", "Rotate 90 deg. CW"]
		self.edit_dropdown_stringvar = StringVar()
		self.edit_dropdown_stringvar.set(dropdown_options[0])
		self.edit_dropdown = OptionMenu(self.toolbar, self.edit_dropdown_stringvar, *dropdown_options, command=self.optionMenuHandler)
		self.quit_application_button = Button(self.toolbar, text="Quit")
		self.quit_application_button.bind("<Button-1>", self.quitApplication)
		self.quick_select_frame = LabelFrame(base_frame, text='Quick Select')
		self.quick_select_slot1 = Canvas(self.quick_select_frame, width=16, height=16, background='white')
		self.quick_select_slot1.bind("<Button-1>", self.quickSelect1)
		self.quick_select_slot2 = Canvas(self.quick_select_frame, width=16, height=16, background='white')
		self.quick_select_slot2.bind("<Button-1>", self.quickSelect2)
		self.quick_select_slot3 = Canvas(self.quick_select_frame, width=16, height=16, background='white')
		self.quick_select_slot3.bind("<Button-1>", self.quickSelect3)
		self.quick_select_slot4 = Canvas(self.quick_select_frame, width=16, height=16, background='white')
		self.quick_select_slot4.bind("<Button-1>", self.quickSelect4)
		self.quick_select_slot5 = Canvas(self.quick_select_frame, width=16, height=16, background='white')
		self.quick_select_slot5.bind("<Button-1>", self.quickSelect5)
		self.quick_select_slot6 = Canvas(self.quick_select_frame, width=16, height=16, background='white')
		self.quick_select_slot6.bind("<Button-1>", self.quickSelect6)
		self.currently_selected_block_frame = Frame(self.quick_select_frame)
		self.currently_selected_block_label = Label(self.currently_selected_block_frame, text="Looking at: ")
		self.currently_selected_block_stringvar = StringVar()
		self.currently_selected_block_stringvar.set(" ")
		self.currently_selected_block_entry = Entry(self.currently_selected_block_frame, textvariable=self.currently_selected_block_stringvar)
		self.mouse_grid_position_label = Label(self.currently_selected_block_frame, text="Mouse position: ")
		self.mouse_grid_position_stringvar = StringVar()
		self.mouse_grid_position_stringvar.set(" ")
		self.mouse_grid_position = Entry(self.currently_selected_block_frame, textvariable = self.mouse_grid_position_stringvar)
		self.sidebar = LabelFrame(base_frame)
		self.select_projects_label = Label(self.sidebar, text="Select a project")
		self.projects = self.loadProjectNames()
		self.projects_list_frame = Frame(self.sidebar)
		self.projects_list = Listbox(self.projects_list_frame, height=10, listvariable=StringVar(value=self.projects), exportselection=False)
		self.projects_list.bind("<<ListboxSelect>>", self.selectProject)
		self.projects_list_scrollbar = Scrollbar(self.projects_list_frame, orient=VERTICAL, command=self.projects_list.yview)
		self.projects_list['yscrollcommand'] = self.projects_list_scrollbar.set
		self.project_buttons = Frame(self.sidebar)
		self.new_project_button = Button(self.project_buttons, text="New")
		self.new_project_button.bind("<Button-1>", self.openTextAreaForNewProject)
		self.rename_project_button = Button(self.project_buttons, text="Rename")
		self.rename_project_button.bind("<Button-1>", self.openTextAreaForRenaming)
		self.delete_project_button = Button(self.project_buttons, text="Delete")
		self.delete_project_button.bind("<Button-1>", self.dialogBoxTest)
		self.enter_text_frame = Frame(self.sidebar)
		self.enter_text_label = Label(self.enter_text_frame, text="Enter a name:")
		self.enter_text = Text(self.enter_text_frame, height=1, width=30)
		self.submit_button = Button(self.enter_text_frame, text="Submit")
		self.block_tallies_frame = LabelFrame(base_frame, text="Block tallies")
		self.block_names_list = Text(self.block_tallies_frame, height=20, width=20, wrap=None)
		self.block_tallies_separator = Separator(self.block_tallies_frame, orient='vertical')
		self.block_tallies_list = Text(self.block_tallies_frame, height=20, width=5)
		self.block_names_list.insert(1.0, "block1\nblock2\nblock3\nblock4\nblock5\nblock6\nblock7\nblock8\nblock9\nblock10\nblock11")
		self.block_tallies_list.insert(1.0, "1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n11\n")
		self.block_tallies_scrollbar = Scrollbar(self.block_tallies_frame, orient=VERTICAL, command=self.block_tallies_list.yview)
		self.block_tallies_list['yscrollcommand'] = self.block_tallies_scrollbar.set
		self.submit_button.bind("<Button-1>", self.submitButtonCallback)
		self.quit_button = Button(self.enter_text_frame, text="Quit")
		self.quit_button.bind("<Button-1>", self.closeTextArea)
		self.raw_mode_checkbox = Checkbutton(self.block_tallies_frame, text="Toggle raw block tallies", variable=self.raw_mode_checkbox_var, onvalue=1, offvalue=0, command=self.toggleRawBlockTallies)
		self.warning_label = Label(self.block_tallies_frame, text="Note: All raw tallies assume\n stonecutters are used \nfor cutting/polishing.")
		self.place_button.grid(column = 0, row = 0)
		self.erase_button.grid(column = 1, row = 0)
		self.select_button.grid(column = 2, row = 0)
		block_label.grid(column=3, row=0)
		self.block_select.grid(column = 4, row = 0, columnspan = 2)
		layer_label.grid(column=6, row = 0)
		self.layer_select.grid(column=7, row = 0)
		self.save_button.grid(column = 0, row = 1)
		self.new_layer_button.grid(column = 1, row = 1)
		self.clear_layer_button.grid(column = 2, row = 1)
		delete_layer_label.grid(column = 3, row = 1)
		self.delete_layer_select.grid(column = 4, row = 1)
		self.edit_dropdown.grid(column = 5, row = 1, columnspan = 2, sticky=(W))
		self.quit_application_button.grid(column = 7, row = 1)
		self.toolbar.grid(column = 1, row = 0)
		self.y_scale_frame.grid(column=0, row=1, sticky=(N,W,E,S), rowspan=5, columnspan=1)
		self.canvas.grid(column=1, row=1, sticky=(N, W, E, S), rowspan = 5, columnspan=3)
		self.x_scale_frame.grid(column=1, row=6, sticky=(N,W,E,S), rowspan=1, columnspan=5)
		self.canvas_x_scrollbar.grid(column=1, row=7, sticky=(N,W,E,S), rowspan=1, columnspan=4)
		self.canvas_y_scrollbar.grid(column=4, row=1, sticky=(N,W,E,S), rowspan=5, columnspan=1)
		x_view_label.grid(column=6, row=3)
		y_view_label.grid(column=6, row=4)
		self.x_view.grid(column=7, row=3)
		self.y_view.grid(column=7, row=4)
		self.quick_select_frame.grid(column=3, row = 0, sticky=(N,W,E,S), rowspan=1, columnspan=6) ####
		self.quick_select_slot1.grid(column=0, row=0)
		self.quick_select_slot2.grid(column=1, row=0)
		self.quick_select_slot3.grid(column=2, row=0)
		self.quick_select_slot4.grid(column=3, row=0)
		self.quick_select_slot5.grid(column=4, row=0)
		self.quick_select_slot6.grid(column=5, row=0)
		self.currently_selected_block_label.grid(column=0, row=0)
		self.currently_selected_block_entry.grid(column=1, row=0)
		self.mouse_grid_position_label.grid(column=0, row=1)
		self.mouse_grid_position.grid(column=1, row=1)
		self.currently_selected_block_frame.grid(column=0, row=1, columnspan=6)
		self.select_projects_label.grid(column = 0, row = 0)
		self.projects_list.grid(column = 0, row = 0)
		self.projects_list_scrollbar.grid(column = 1, row = 0, sticky=(N,W,E,S))
		self.projects_list_frame.grid(column = 0, row = 1, columnspan=6) 
		self.new_project_button.grid(column = 0, row = 0)
		self.rename_project_button.grid(column = 1, row = 0)
		self.delete_project_button.grid(column = 2, row = 0 )
		self.project_buttons.grid(column = 0, row = 2)
		self.enter_text_label.grid(column = 0, row = 0)
		self.enter_text.grid(column = 0, row = 1, columnspan = 2)
		self.submit_button.grid(column = 0, row = 2)
		self.quit_button.grid(column = 1, row = 2)
		self.block_names_list.grid(column=0, row=0)
		self.block_tallies_separator.grid(column=1, row=0)
		self.block_tallies_list.grid(column=2, row=0)
		self.block_tallies_scrollbar.grid(column=3, row=0, sticky=(N, W, E, S))
		self.raw_mode_checkbox.grid(column=0, row=1, columnspan=3, sticky=W)
		self.sidebar.grid(column=6, row=1, columnspan=6)
		self.block_tallies_frame.grid(column=6, row=2, sticky=W, columnspan=6) ####
		self.grid(column = 0, row = 0)
		#self.pack()

blocks_helper = BlocksHelper()


def main():
	root = Tk()
	root.geometry("1000x800")
	global blocks_helper
	blocks_helper.loadBlocks()
	app = MCBuildHelper(root)
	print(mystuff)
	root.mainloop()

if __name__ == "__main__":
	main()


