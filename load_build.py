import math
import gzip
import zlib
import re
import os


class StatusCode(object):
	def __init__(self, status, error_code, error_message, payload):
		self.status = status #is "SUCCESS" for success or "ERROR" for error
		self.error_code = error_code #number that uniquely describes each error
		self.error_message = error_message #info text that describes the error if there is one
		self.payload = payload #data that gets returned by the function if there is data to return. If there is an error, this is None

		'''
		error codes:
		0 = OK
		1 = World not found
		2 = File not found
		'''

	def getStatus(self):
		return self.status

	def getErrorCode(self):
		return self.error_code

	def getErrorMessage(self):
		return self.error_message

	def getPayload(self):
		return self.payload

	def setStatus(self, new_status):
		self.status = new_status

	def setErrorCode(self, new_error_code):
		self.error_code = new_error_code

	def setErrorMessage(self, new_error_message):
		self.error_message = new_error_message

	def setPayload(self, payload):
		self.payload = payload


def playerCoordsToFilename(x, y):
	chunk_x = x // 16
	chunk_y = y // 16
	file_x = math.floor(chunk_x / 32)
	file_y = math.floor(chunk_y / 32)
	return [file_x, file_y]

def getFileNameFromChunkCoords(chunk_x, chunk_z):
	file_x = math.floor(chunk_x / 32)
	file_z = math.floor(chunk_z / 32)
	return [file_x, file_z]

def getOffsetFromNums(digit1, digit2, digit3):
	digit1_shifted = digit1 << 16
	digit2_shifted = digit2 << 8
	digit3_shifted = digit3

	total = ((digit1_shifted | digit2_shifted) | digit3_shifted)
	#print("Total: " + str(total))
	return total * 4096

def playerCoordsToChunkCoords(x, y):
	chunk_x = math.floor(x / 16)
	chunk_y = math.floor(y / 16)
	return [chunk_x, chunk_y]

output = playerCoordsToFilename(-3755, 788)
print(output)

chunk_x = -235
chunk_z = 49

def findGCD(num1, num2): #find greatest common divisor
	if num1 == 0:
		return num2
	return findGCD(num2 % num1, num1)

def findLCM(num1, num2):
	lcm = (num1 / findGCD(num1, num2)) * num2
	return int(lcm)

def byteStringToInt(mybytestring):
	bytestring_list = list(mybytestring)
	shift = 0
	total = 0x00
	for i in reversed(range(0, len(bytestring_list))):
		print(bytestring_list[i])
		total = total | (bytestring_list[i] << total)
		shift += 8
	return total

print(findLCM(5, 8))
print(findLCM(8, 6))

num_properties = {
	"anvil": 1,
	"bamboo": 3,
	"banner": 1,
	"barrel": 2,
	"bed": 3,
	"beehive": 2,
	"beetroot": 2,
	"bell": 3,
	"blast_furnace": 2,
	"bone_block": 2,
	"brewing_stand": 3,
	"bubble_column": 1,
	"button": 3,
	"cactus": 1,
	"campfire": 4,
	"cake": 1,
	"carrots": 1,
	"carved_pumpkin": 1,
	"cauldron": 1,
	"chain": 2,
	"chest": 3,
	"ender_chest": 2,
	"chorus_flower": 1,
	"chorus_plant": 6,
	"cocoa": 2,
	"command_block": 2,
	"composter": 1,
	"conduit": 1,
	"daylight_detector": 2,
	"dispenser": 2,
	"dropper": 2,
	"door": 5,
	"end_portal_frame": 2,
	"end_rod": 1,
	"farmland": 1,
	"fence": 5,
	"fence_gate": 4,
	"fire": 6,
	"frosted_ice": 1,
	"furnace": 2,
	"glass_pane": 5,
	"glazed_terracotta": 1,
	"grass_block": 1,
	"mycelium": 1,
	"podzol": 1,
	"grindstone": 2,
	"hay_bale": 1,
	"hopper": 2,
	"iron_bars": 5,
	"jigsaw_block": 1,
	"jack_o_lantern": 1,
	"jukebox": 1,
	"kelp": 1,
	"ladder": 2,
	"lantern": 1,
	"sunflower": 1,
	"lilac": 1,
	"rose_bush": 1,
	"peony": 1,
	"lava": 1,
	"leaves": 2,
	"lectern": 3,
	"lever": 3,
	"logs": 1,
	"loom": 1,
	"melon_stem": 1,
	"mob_head": 1,
	"mushroom_block": 6,
	"nether_wart": 1,
	"nether_portal": 1,
	"note_block": 3,
	"observer": 2,
	"piston": 2,
	"moving_piston": 2,
	"piston_head": 3,
	"potatoes": 1,
	"weighted_pressure_plate": 1,
	"pressure_plate": 1,
	"growing_pumpkin_stem": 1,
	"attached_pumpkin_stem": 1,
	"purpur_pillar": 1,
	"quartz_pillar": 1,
	"detector_rail": 3,
	"powered_rail": 3,
	"activator_rail": 3,
	"rail": 2,
	"redstone_comparator": 3,
	"redstone_dust": 5,
	"redstone_lamp": 1,
	"redstone_ore": 1,
	"redstone_repeater": 4,
	"floor_redstone_torch": 1,
	"wall_redstone_torch": 2,
	"respawn_anchor": 1,
	"sapling": 1,
	"scaffolding": 3,
	"sea_pickle": 2,
	"shulker_box": 1,
	"sign": 3,
	"slab": 2,
	"smoker": 2,
	"snow": 1,
	"stairs": 4,
	"stonecutter": 1,
	"structure_block": 1,
	"sugar_cane": 1,
	"sweet_berry_bush": 1,
	"tall_grass": 1,
	"large_fern": 1,
	"tall_seagrass": 1,
	"tnt": 1,
	"trapdoor": 5,
	"tripwire": 7,
	"tripwire_hook": 3,
	"turtle_egg": 2,
	"vine": 5,
	"wall_torch": 1,
	"wall": 6,
	"water": 1,
	"wheat": 1,
	"wood": 1
}

#true = property is a number
#false = property is a string

property_types = {
	"facing": False,
	"age": True,
	"leaves": False,
	"stage": True,
	"rotation": True,
	"open": False,
	"occupied": False,
	"part": False,
	"honey_level": True,
	"attachment": False,
	"powered": False,
	"lit": False,
	"has_bottle_0": False,
	"has_bottle_1": False,
	"has_bottle_2": False,
	"drag": False,
	"face": False,
	"signal_fire": False,
	"waterlogged": False,
	"bites": True,
	"level": True,
	"axis": False,
	"type": False,
	"down": False,
	"east": False,
	"north": False,
	"south": False,
	"up": False,
	"west": False,
	"conditional": False,
	"inverted": False,
	"power": True,
	"triggered": False,
	"half": False,
	"hinge": False,
	"eye": False,
	"moisture": True,
	"in_wall": False,
	"snowy": False,
	"enabled": False,
	"orientation": False,
	"has_record": False,
	"hanging": False,
	"distance": True,
	"persistent": False,
	"has_book": False,
	"instrument": False,
	"note": True,
	"extended": False,
	"short": False,
	"shape": False,
	"mode": False,
	"locked": False,
	"delay": True,
	"charges": True,
	"bottom": False,
	"pickles": True,
	"unstable": False,
	"disarmed": False,
	"attached": False,
	"eggs": True,
	"hatch": True,
	"layers": True
}

def getChunkData(chunk_x, chunk_z, world_name):
	chunk_header_offset = 4 * ((chunk_x % 32) + (chunk_z % 32) * 32)
	file_coords = getFileNameFromChunkCoords(chunk_x, chunk_z)
	file_x = file_coords[0]
	file_z = file_coords[1]
	available_worlds = os.listdir("C:\\Users\\benja\\AppData\\Roaming\\.minecraft\\saves\\")
	if world_name not in available_worlds:
		world_not_found = StatusCode("ERROR", 1, "The requested world was not found.", None)
		return world_not_found

	available_chunk_files = os.listdir("C:\\Users\\benja\\AppData\\Roaming\\.minecraft\\saves\\" + world_name + "\\region\\")
	filename = "r." + str(file_x) + "." + str(file_z) + ".mca"
	if filename not in available_chunk_files:
		file_not_found = StatusCode("ERROR", 2, "The file containing the requested chunk was not found.", None)
		return file_not_found

	filepath = "C:\\Users\\benja\\AppData\\Roaming\\.minecraft\\saves\\" + world_name + "\\region\\" + filename
	file = open(filepath, mode="rb")
	file.seek(chunk_header_offset, 0)
	chars = file.read(50)
	list_chars = list(chars)	
	chunk_data_offset_digit1 = list_chars[0]
	chunk_data_offset_digit2 = list_chars[1]
	chunk_data_offset_digit3 = list_chars[2]
	chunk_data_size = list_chars[3]
	chunk_data_offset = getOffsetFromNums(chunk_data_offset_digit1, chunk_data_offset_digit2, chunk_data_offset_digit3)
	file.seek(chunk_data_offset, 0)
	chunk_data_header = file.read(5)
	list_chunk_data_header = list(chunk_data_header)
	chunk_data_size_digit1 = list_chunk_data_header[0]
	chunk_data_size_digit2 = list_chunk_data_header[1]
	chunk_data_size_digit3 = list_chunk_data_header[2]
	chunk_data_size_digit4 = list_chunk_data_header[3]
	chunk_data_size_digit1_shifted = chunk_data_size_digit1 << 24
	chunk_data_size_digit2_shifted = chunk_data_size_digit2 << 16
	chunk_data_size_digit3_shifted = chunk_data_size_digit3 << 8
	chunk_data_size_digit4_shifted = chunk_data_size_digit4
	chunk_data_size_total = (((chunk_data_size_digit1_shifted | chunk_data_size_digit2_shifted) | chunk_data_size_digit3_shifted) | chunk_data_size_digit4_shifted)
	compressed_chunk_data = file.read(chunk_data_size_total)
	decompressed_chunk_data = zlib.decompress(compressed_chunk_data)
	decompressed_chunk_data_list = list(decompressed_chunk_data)
	file.close()
	success = StatusCode("SUCCESS", 0, "Success", decompressed_chunk_data)
	return success
	#return decompressed_chunk_data

def parseCompoundTag(data, start_index):
	#print("Parsing a compound tag...")
	compound_tag_payload = []
	compound_tag_start = start_index
	while True:
		#print("Parsing tags within a compound tag ===================")
		#print(compound_tag_start)
		subtag_data = parseTags(data, compound_tag_start)
		#print("Finished parsing tags within a compound tag ==========")
		#print("Subtag data:")
		#print(subtag_data)
		compound_tag_start = subtag_data[0]
		#compound_tag_payload.append(subtag_data[1])
		subtag_contents = subtag_data[1]
		#print("Subtag data: ")
		#print(subtag_data)
		if isinstance(subtag_contents, list):
			#print("This is a compound tag...")
			compound_tag_payload.append(subtag_contents)
			continue
		compound_tag_payload.append(subtag_contents)
		subtag_type = subtag_contents["Tag type"]
		if subtag_type == "TAG_End":
			#print("Found a TAG_End, breaking...")
			break
	#print("Final compound tag payload:")
	#print(compound_tag_payload)
	return [compound_tag_start, compound_tag_payload]
		 



def parseTags(data, start_index):
	#print("Parsing tags...")
	tag_data = {}
	new_index = start_index
	
	tag_id_start = start_index
	tag_id_end = tag_id_start + 1
	tag_id = data[tag_id_start:tag_id_end]
	#print(tag_id)
	tag_id_int = int.from_bytes(tag_id, byteorder="big")
	#print(tag_id_int)

	tag_data = {"Tag type": None, "Name": None, "Payload": None}
	if tag_id_int == 0:
		#print("Found a TAG_End")
		tag_data["Tag type"] = "TAG_End"
		tag_data["Name"] = "TAG_End"
		tag_data["Payload"] = tag_id_int
		return [tag_id_end, tag_data]
	else:
		tag_name_len_start = tag_id_end
		tag_name_len_end = tag_name_len_start + 2
		tag_name_len = data[tag_name_len_start:tag_name_len_end]
		#print(tag_name_len)
		tag_name_len_int = int.from_bytes(tag_name_len, byteorder="big")

		tag_name_start = tag_name_len_end
		tag_name_end = tag_name_start + tag_name_len_int
		tag_name = data[tag_name_start:tag_name_end]
		#print(tag_name)	
		if tag_id_int == 1:
			#print("Found a TAG_Byte")
			#for TAG_byte, the payload consists of a single byte
			tag_byte_payload_start = tag_name_end
			tag_byte_payload_end = tag_byte_payload_start + 1
			tag_byte_payload = data[tag_byte_payload_start:tag_byte_payload_end]
			tag_data["Tag type"] = "TAG_Byte"
			tag_data["Name"] = tag_name
			tag_data["Payload"] = tag_byte_payload

			return [tag_byte_payload_end, tag_data]
		elif tag_id_int == 2:
			#print("Found a TAG_Short")
			#For a TAG_short, we need to read in 2 bytes, since a short is 2 bytes
			tag_short_start = tag_name_end
			tag_short_end = tag_short_start + 2
			tag_short_payload = data[tag_short_start:tag_short_end]
			tag_short_value = int.from_bytes(tag_short_payload, byteorder="big")

			tag_data["Tag type"] = "TAG_Short"
			tag_data["Name"] = tag_name
			tag_data["Payload"] = tag_short_value
			return [tag_short_end, tag_data]
		elif tag_id_int == 3:
			#print("Found a TAG_Int")
			#For a TAG_int, we need to read in 4 bytes, since an integer is 4 bytes
			tag_int_start = tag_name_end
			tag_int_end = tag_int_start + 4
			tag_int_payload = data[tag_int_start:tag_int_end]
			tag_int_value = int.from_bytes(tag_int_payload, byteorder="big", signed=True)
			#print("Int value: " + str(tag_int_value))

			tag_data["Tag type"] = "TAG_Int"
			tag_data["Name"] = tag_name
			tag_data["Payload"] = tag_int_value
			return [tag_int_end, tag_data]
		elif tag_id_int == 4:
			#print("Found a TAG_Long")
			#For a TAG_Long, we need to read in 8 bytes, since a long is 8 bytes.
			tag_long_start = tag_name_end
			tag_long_end = tag_long_start + 8

			tag_long = data[tag_long_start:tag_long_end]
			tag_long_int = int.from_bytes(tag_long, byteorder="big")

			tag_data["Tag type"] = "TAG_Long"
			tag_data["Name"] = tag_name
			#print(tag_name)
			#print("Tag name: " + tag_name)
			tag_data["Payload"] = tag_long
			#print(tag_long)
			#print("Tag payload: " + tag_long)
			return [tag_long_end, tag_data]

		elif tag_id_int == 5:
			#print("Found a TAG_Float")
			tag_float_start = tag_name_end
			tag_float_end = tag_float_start + 4

			tag_float = data[tag_float_start:tag_float_end]
			tag_data["Tag type"] = "TAG_Float"
			tag_data["Name"] = tag_name
			tag_data["Payload"] = tag_float
			return [tag_float_end, tag_data]
		elif tag_id_int == 6:
			#print("Found a TAG_Double")
			#read in 8 bytes for a double
			tag_double_start = tag_name_end
			tag_double_end = tag_double_start + 8
			tag_double = data[tag_double_start:tag_double_end]
			tag_data["Tag type"] = "TAG_Float"
			tag_data["Name"] = tag_name
			tag_data["Payload"] = tag_double
			return [tag_double_end, tag_data]
		elif tag_id_int == 7:
			#print("Found a TAG_Byte_Array")
			byte_array_length_start = tag_name_end
			byte_array_length_end = byte_array_length_start + 4
			byte_array_length = data[byte_array_length_start:byte_array_length_end]
			byte_array_length_int = int.from_bytes(byte_array_length, byteorder="big")
			byte_array_contents_start = byte_array_length_end
			byte_array_contents_end = byte_array_contents_start + byte_array_length_int

			byte_array = data[byte_array_contents_start:byte_array_contents_end]
			tag_data["Tag type"] = "TAG_Byte_Array"
			tag_data["Name"] = tag_name
			tag_data["Payload"] = byte_array

			return [byte_array_contents_end, tag_data]

		elif tag_id_int == 8:
			#print("Found a TAG_String")
			#For a TAG_string, we need to read in 2 bytes for the length of the string, and then the string itself. 
			tag_string_length_start = tag_name_end
			tag_string_length_end = tag_string_length_start + 2
			tag_string_length = data[tag_string_length_start:tag_string_length_end]
			tag_string_length_int = int.from_bytes(tag_string_length, byteorder="big")

			tag_string_start = tag_string_length_end
			tag_string_end = tag_string_start + tag_string_length_int

			tag_string = data[tag_string_start:tag_string_end]

			tag_data["Tag type"] = "TAG_String"
			tag_data["Name"] = tag_name
			tag_data["Payload"] = tag_string

			return [tag_string_end, tag_data]
		elif tag_id_int == 9:

			#print("Found a TAG_List")
			tag_list_contents_type_start = tag_name_end
			tag_list_contents_type_end = tag_list_contents_type_start + 1
			tag_list_contents_type = data[tag_list_contents_type_start:tag_list_contents_type_end]
			tag_list_contents_type_int = int.from_bytes(tag_list_contents_type, byteorder="big")
			#print("TAG_List contents type:")
			#print(tag_list_contents_type)

			tag_list_length_start = tag_list_contents_type_end
			tag_list_length_end = tag_list_length_start + 4
			tag_list_length = data[tag_list_length_start:tag_list_length_end]
			tag_list_length_int = int.from_bytes(tag_list_length, byteorder="big")
			#print("TAG_List length:")
			#print(tag_list_length_int)
			#print("TAG_List name:")
			#print(tag_name)
			tag_data["Tag type"] = "TAG_List"
			tag_data["Name"] = tag_name
			tag_list_data = []

			list_start = tag_list_length_end
			
			#for i in range(0, tag_list_length_int):
			for i in range(0, tag_list_length_int):
				if tag_list_contents_type_int == 10:
					#print("==================NEW COMPOUND TAG======================")
					compound_tag_data = parseCompoundTag(data, list_start)
					list_start = compound_tag_data[0]
					tag_list_data.append(compound_tag_data[1])
				else:
					#array_item = parseTags(data, list_start)
					#list_start = array_item[0]
					#tag_list_data.append(array_item[1])
					if tag_list_contents_type == b'\x03':
						single_int = data[list_start:list_start+4]
						tag_list_data.append(single_int)
						list_start = list_start + 4
					elif tag_list_contents_type == b'\x08':
						string_length_start = list_start
						string_length_end = list_start + 2
						string_length = data[string_length_start:string_length_end]
						string_length_int = int.from_bytes(string_length, byteorder="big")
						string_start = string_length_end
						string_end = string_start + string_length_int
						string = data[string_start:string_end]
						list_start = string_end
						tag_list_data.append(string)
					elif tag_list_contents_type == b'\x06':
						single_double = data[list_start:list_start+8]
						tag_list_data.append(single_double)
						list_start = list_start + 8
					elif tag_list_contents_type == b'\x05':
						single_float = data[list_start:list_start+4]
						tag_list_data.append(single_float)
						list_start = list_start + 4
					#print("wat")

			#print("TAG_List data:")
			#print(tag_list_data)
			return [list_start, tag_list_data]
		elif tag_id_int == 10:
			#print("Found a TAG_Compound")
			#print(tag_name)
			compound_tag_data = parseCompoundTag(data, tag_name_end)
			compound_tag_data_end = compound_tag_data[0]
			compound_tag_data_payload = compound_tag_data[1]
			return [compound_tag_data_end, compound_tag_data_payload]
		elif tag_id_int == 11:
			#print("Found a TAG_Int_Array")
			int_array_length_start = tag_name_end
			int_array_length_end = int_array_length_start + 4
			int_array_length = data[int_array_length_start:int_array_length_end]
			int_array_length_int = int.from_bytes(int_array_length, byteorder="big") * 4 #multiply by 4, since each integer is 4 bytes long

			int_array_start = int_array_length_end
			int_array_end = int_array_start + int_array_length_int
			int_array = data[int_array_start:int_array_end]

			tag_data["Tag type"] = "TAG_Int_Array"
			tag_data["Name"] = tag_name
			tag_data["Payload"] = int_array

			return [int_array_end, tag_data] 

		elif tag_id_int == 12:
			#print("Found a TAG_Long_Array")
			long_array_length_start = tag_name_end
			long_array_length_end = long_array_length_start + 4
			long_array_length = data[long_array_length_start:long_array_length_end]
			long_array_length_int = int.from_bytes(long_array_length, byteorder="big") * 8 #multiply by 8, since each long is 8 bytes 

			long_array_start = long_array_length_end
			long_array_end = long_array_start + long_array_length_int
			long_array = data[long_array_start:long_array_end]

			tag_data["Tag type"] = "TAG_Int_Array"
			tag_data["Name"] = tag_name
			tag_data["Payload"] = long_array

			return [long_array_end, tag_data]
		else:
			print("TAG ID: " + str(tag_id_int))

def parseTileEntities(chunk_x, chunk_z):
	#decompressed_chunk_data = getChunkData(chunk_x, chunk_z)
	#if decompressed_chunk_data.getStatus() == "SUCCESS":
	chunk_data = getChunkData(chunk_x, chunk_z)
	decompressed_chunk_data = chunk_data.getPayload()

	tile_entities_start = decompressed_chunk_data.find(b'TileEntities')

	tile_entities_tag_start = tile_entities_start - 3
	#print(decompressed_chunk_data[tile_entities_tag_start:tile_entities_tag_start + 3])
	
	final_output = parseTags(decompressed_chunk_data, tile_entities_tag_start)
	print("==================FINAL OUTPUT======================")
	print(final_output)
	tile_entities_data = final_output[1]
	for tile_entity in tile_entities_data:
		print("Found a tile entity.**************")
		for data_tag in tile_entity:
			if isinstance(data_tag, list):
				continue
			if data_tag['Name'] == b'id':
				print("Name: ")
				print(data_tag['Payload'])
			elif data_tag['Name'] == b'x':
				print("X: ")
				print(data_tag['Payload'])
			elif data_tag['Name'] == b'y':
				print("Y: ")
				print(data_tag['Payload'])
			elif data_tag['Name'] == b'z':
				print("Z: ")
				print(data_tag['Payload'])
	'''
	block_entities_end = block_entities_start + 12
	print(decompressed_chunk_data[block_entities_start:block_entities_end])
	data_type_start = block_entities_end
	data_type_end = block_entities_end + 1
	print(decompressed_chunk_data[data_type_start:data_type_end])
	num_items_start = data_type_end
	num_items_end = num_items_start + 4
	num_items = decompressed_chunk_data[num_items_start:num_items_end]
	num_items_int = int.from_bytes(num_items, byteorder="big")

	tag_start = num_items_end
	for i in range(0, num_items_int):
		parseTags(decompressed_chunk_data, tag_start)
	'''
def loadNameToIndexMappings():
	block_data = open("blocks_real.txt")
	loaded_blocks = block_data.readlines()
	index = 0
	blocks = {}
	for block in loaded_blocks:
		block = block.rstrip('\n').split("-")
		block_name = block[0]
		blocks[block_name] = index
		index += 1
	#print(blocks)
	return blocks

#loadNameToIndexMappings()

def loadNamespacedIDMappings():
	mappings = {}
	mapping_file = open("namespaced_ids_to_ingame_names.txt", "r")
	lines = mapping_file.readlines()
	for line in lines:
		line = line.rstrip("\n")
		line_split = line.split("-")
		#print(line_split)
		namespaced_ID = line_split[1]
		ingame_name = line_split[0]
		mappings[namespaced_ID] = ingame_name
	#print(mappings)
	return mappings

name_mappings = loadNamespacedIDMappings()

def printPaletteData(chunk_x, chunk_z, requested_y, world_name):
	chunk_data = getChunkData(chunk_x, chunk_z, world_name)
	if chunk_data.getStatus() == "ERROR":
		return chunk_data
	decompressed_chunk_data = chunk_data.getPayload()
	find_start = 0
	palette_indices = []
	while True:
		position = decompressed_chunk_data.find(b'Palette', find_start)
		if position == -1:
			break
		palette_indices.append(position)
		find_start = position + 20
	palette_start = palette_indices[requested_y]
	palette_end = palette_start + 8
	palette_word = decompressed_chunk_data[palette_start:palette_end]
	palette_tag_type = decompressed_chunk_data[palette_end - 1:palette_end]
	num_blocks = decompressed_chunk_data[palette_end:palette_end+4]
	num_blocks_int = byteStringToInt(num_blocks)
	block_index = 0
	start = palette_end + 4
	blocks = []
	current_block_name = None
	current_properties = None
	while True:
		tag_type = decompressed_chunk_data[start:start + 1]
		if tag_type == b'\x08':
			name_size_start = start + 1
			name_size_end = name_size_start + 2
			name_size = decompressed_chunk_data[name_size_start:name_size_end]
			name_start = name_size_end
			name_end = name_start + int.from_bytes(name_size, byteorder="big")
			name_word = decompressed_chunk_data[name_start:name_end]
			block_name_size_start = name_end
			block_name_size_end = block_name_size_start + 2
			block_name_size = int.from_bytes(decompressed_chunk_data[block_name_size_start:block_name_size_end], byteorder="big")
			block_name_start = block_name_size_end
			block_name_end = block_name_start + block_name_size
			block_name = decompressed_chunk_data[block_name_start:block_name_end]
			terminator_tag_start = block_name_end
			terminator_tag_end = terminator_tag_start + 1
			terminator_tag = decompressed_chunk_data[terminator_tag_start:terminator_tag_end]
			start = terminator_tag_end
			block_name_string = block_name.decode("utf-8")[10:]
			ingame_name = name_mappings[block_name_string]
			current_block_name = ingame_name
			block_info_dict = {"name": ingame_name, "index": block_index, "properties": None}
			if current_properties is not None:
				block_info_dict["properties"] = current_properties
				current_properties = None
			blocks.append(block_info_dict)
			block_index += 1
		elif tag_type == b'\n':
			name_size_start = start + 1
			name_size_end = name_size_start + 2
			name_size = decompressed_chunk_data[name_size_start:name_size_end]
			name_start = name_size_end
			name_end = name_start + int.from_bytes(name_size, byteorder="big")
			name_word = decompressed_chunk_data[name_start:name_end]
			name_word_string = name_word.decode("utf-8")
			properties_start = name_end
			properties = {}
			while True:
				property_key_type_start = properties_start
				property_key_type_end = property_key_type_start + 1
				property_key_type = decompressed_chunk_data[property_key_type_start:property_key_type_end]
				if property_key_type == b'\x00':
					print(decompressed_chunk_data[property_key_type_end:property_key_type_end+30])
				property_key_length_start = property_key_type_end
				property_key_length_end = property_key_length_start + 2
				property_key_length = int.from_bytes(decompressed_chunk_data[property_key_length_start:property_key_length_end], byteorder="big")
				property_key_start = property_key_length_end
				property_key_end = property_key_start + property_key_length
				property_key = decompressed_chunk_data[property_key_start:property_key_end];
				property_key_string = property_key.decode("utf-8")
				if property_key_string == "Name":
					start = properties_start
					break
				is_numeric = property_types[property_key_string]
				property_value_end = 0
				property_value_length_start = property_key_end
				property_value_length_end = property_value_length_start + 2
				property_value_length = int.from_bytes(decompressed_chunk_data[property_value_length_start:property_value_length_end], byteorder="big")
				property_value_start = property_value_length_end
				property_value_end = property_value_start + property_value_length
				property_value = None
				if is_numeric:
					property_value = int.from_bytes(decompressed_chunk_data[property_value_start:property_value_end], byteorder="big")
				else:
					property_value_bytestring = decompressed_chunk_data[property_value_start:property_value_end]
					property_value = property_value_bytestring.decode("utf-8")
				terminator_tag_start = property_value_end
				terminator_tag_end = terminator_tag_start + 1
				terminator_tag = decompressed_chunk_data[terminator_tag_start:terminator_tag_end]
				properties[property_key_string] = property_value
				current_properties = properties
				if terminator_tag == b'\x00':
					start = terminator_tag_end
					break
				properties_start = terminator_tag_start
		else:
			break
	print("Palette:")
	print(blocks)
	success = StatusCode("SUCCESS", 0, "Success", blocks)
	return success


def get_bitmask_of_specified_length(length):
	if length == 0:
		return 0x00
	start = 0x01
	for i in range(0, length - 1):
		start = start << 1
		start = start | 0x01
	return start


def getVersion(world_name):
	level_dat_filepath = "C:\\Users\\benja\\AppData\\Roaming\\.minecraft\\saves\\" + world_name + "\\level.dat"
	#level_dat_file = open(level_dat_filepath, "rb")

	with gzip.open(level_dat_filepath, "rb") as file:
		level_dat_file_data = file.read()
		#print(level_dat_file_data)
		ret = parseTags(level_dat_file_data, 3)
		print("FINAL RET")
		#print(ret)
		for tag in ret[1]:
			'''
			print("TAG===============================================================")
			print(tag)
			print("==================================================================")
			'''
			if isinstance(tag, dict):
				#print("Hello")
				#print(tag)
				if tag["Name"] == b'DataVersion':
					print(tag["Payload"])
					return tag["Payload"]
	return -1 
	'''
	level_dat_file_data = level_dat_file.read()
	decompressed_dat_file_data = zlib.decompress(level_dat_file_data)
	print(decompressed_dat_file_data)
	'''


def printChunkData(chunk_x, chunk_z, requested_y, world_name):


	
	chunk_data = getChunkData(chunk_x, chunk_z, world_name)
	if chunk_data.getStatus() == "ERROR":
		chunk_read_error = StatusCode("ERROR", chunk_data.getErrorCode(), chunk_data.getErrorMessage(), None)
		return chunk_read_error
	decompressed_chunk_data = chunk_data.getPayload()
	

	decompressed_chunk_data_list = list(decompressed_chunk_data)

	find_start = 0

	block_states_indices = []

	while True:
		position = decompressed_chunk_data.find(b'BlockStates', find_start)
		if position == -1:
			break
		#print(position)
		block_states_indices.append(position)
		#print(decompressed_chunk_data[position:(position + 20)])
		find_start = position + 20
		#decompressed_chunk_data = decompressed_chunk_data[(position + 15):]

	
	#block_states_start = decompressed_chunk_data.find(b'BlockStates')
	if requested_y < len(block_states_indices):
		block_states_start = block_states_indices[requested_y]
	else:
		return -1

	#print(block_states_start)



	block_states_size_start = block_states_start + 11
	block_states_size_end = block_states_size_start + 4

	block_states_size = decompressed_chunk_data[block_states_size_start:block_states_size_end]
	#print(block_states_size)
	block_states_size_int = int.from_bytes(block_states_size, byteorder="big")

	real_size = block_states_size_int * 8
	#print("Block size: " + str(block_states_size_int))

	block_states = decompressed_chunk_data[block_states_size_end:block_states_size_end+real_size]
	#print(block_states)
	block_states_list = list(block_states)
	#print(len(block_states_list))

	bits_per_block = int((len(block_states_list) * 8) / 4096)
	print("Bits per block: " + str(bits_per_block))
	#print(block_states_list)

	block_ids = []

	block_counts = {
		"0": 0,
		"1": 0,
		"2": 0,
		"3": 0,
		"4": 0,
		"5": 0,
		"6": 0,
		"7": 0,
		"8": 0,
		"9": 0,
		"10": 0,
		"11": 0,
		"12": 0,
		"13": 0,
		"14": 0,
		"15": 0,
		"16": 0,
		"17": 0,
		"18": 0,
		"19": 0,
		"20": 0,
		"21": 0,
		"22": 0,
		"23": 0,
		"24": 0,
		"25": 0,
		"26": 0
	}

	world_version = getVersion(world_name)

	if world_version < 2566:
		original_leftover_bits_bitmask = 0xFF >> (8 - int(64 % bits_per_block)) #at 64 bits per long, and 5 bits per block, that equals 4 bits leftover, or a bitmask of 0x0F
		# - If there are 4 bits per block, this should be 0, since 64 % 4 = 0
		total_leftover_bits = int(64 % bits_per_block) #also 4. 

		bits_per_block_remainder = bits_per_block - total_leftover_bits
		#For 4 bits per block, this is 4. For 5 bits per block, this is 1. For 6 bits per block, this is 2. For 7 bits per block, this is 6

		'''
		4 bits per block = 16 blocks per long, 0 bits left over. 4 - 0 = 4
		5 bits per block = 12 blocks per long, 4 bits left over. 5 - 4 = 1
		6 bits per block = 10 blocks per long, 4 bits left over. 6 - 4 = 2
		7 bits per block = 9 blocks per long, 1 bit left over. 7 - 1 = 6
		'''


		blocks_per_long = int(64 // bits_per_block) #at 64 bits per long, and 5 bits per block, that equals 12 blocks
		block_bitmask = 0xFF >> (8 - int(bits_per_block)) #this bitmask is to get the bits that make up a block from a long. 0xFF >> (8 - 5) = 0x1F
		original_next_long_high_bits = int(bits_per_block - total_leftover_bits)
		#1 if 5 bits per block, 2 if 6 bits per block
		original_next_long_high_bits_shift = block_bitmask >> total_leftover_bits
		#0x01 if 5 bits per block, 0x03 (0000 0011) if 6 bits per block since 0x3F >> 4 = 0x03
		print("Original leftover bits bitmask: " + str(original_leftover_bits_bitmask))
		print("Total leftover bits: " + str(total_leftover_bits))
		print("Blocks per long: " + str(blocks_per_long))
		print("Block bitmask: " + str(block_bitmask))
		print("Original next long high bits: " + str(original_next_long_high_bits))
		print("Original next long high bits shift: " + str(original_next_long_high_bits_shift))

		#step = 8 * bits_per_block
		step = findLCM(8, bits_per_block)
		if(step == 8):
			step = 8 * bits_per_block
		print("Step: " + str(step))

		for i in range(0, len(block_states_list), step):
			#print("New group of 40 bytes")
			leftover_bits_bitmask = original_leftover_bits_bitmask
			next_long_high_bits = original_next_long_high_bits
			leftover_bits = total_leftover_bits
			next_long_high_bits_shift = original_next_long_high_bits_shift
			longs = []
			start = 0

			for j in range(i, i + step, 8):
				#print("j: " + str(j))
				byte1 = block_states_list[j] << 56
				byte2 = block_states_list[j + 1] << 48
				byte3 = block_states_list[j + 2] << 40
				byte4 = block_states_list[j + 3] << 32
				byte5 = block_states_list[j + 4] << 24
				byte6 = block_states_list[j + 5] << 16
				byte7 = block_states_list[j + 6] << 8		
				byte8 = block_states_list[j + 7]
				new_long = (((((((byte1 | byte2) | byte3) | byte4) | byte5) | byte6) | byte7) | byte8)
				#print("Long: " + str(new_long))
				longs.append(new_long)
			start = 0
			
			num_iterations_per_long = blocks_per_long

			
			for i in range(0, len(longs)):
				for j in range(0, num_iterations_per_long):
					extracted_bytes = longs[i] & block_bitmask
					block_ids.append(extracted_bytes)
					longs[i] = longs[i] >> bits_per_block
				if i != len(longs) - 1:
					leftover_bits_bitmask = get_bitmask_of_specified_length(leftover_bits)
					current_leftover_bits = longs[i] & leftover_bits_bitmask

					next_long_num_bits = bits_per_block - leftover_bits
					next_long_bits_bitmask = get_bitmask_of_specified_length(next_long_num_bits)
					next_long_bits = longs[i + 1] & next_long_bits_bitmask
					next_long_bits = next_long_bits << leftover_bits

					longs[i + 1] = longs[i + 1] >> next_long_num_bits
					additional_block = current_leftover_bits | next_long_bits
					block_ids.append(additional_block)


					num_iterations_per_long = (64 - next_long_num_bits) // bits_per_block

					block_bits_in_next_long = num_iterations_per_long * bits_per_block
					leftover_bits = 64 - next_long_num_bits - block_bits_in_next_long
	else:
		#longs = []
		#start = 0

		blocks_per_long = 64 // bits_per_block
		block_bitmask = get_bitmask_of_specified_length(bits_per_block)

		for i in range(0, len(block_states_list), 8):
			#print("New group of 40 bytes")
			

			
			#print("j: " + str(j))
			byte1 = block_states_list[i] << 56
			byte2 = block_states_list[i + 1] << 48
			byte3 = block_states_list[i + 2] << 40
			byte4 = block_states_list[i + 3] << 32
			byte5 = block_states_list[i + 4] << 24
			byte6 = block_states_list[i + 5] << 16
			byte7 = block_states_list[i + 6] << 8		
			byte8 = block_states_list[i + 7]
			new_long = (((((((byte1 | byte2) | byte3) | byte4) | byte5) | byte6) | byte7) | byte8)
			#print("Long: " + str(new_long))
			for i in range(0, blocks_per_long):
				block = new_long & block_bitmask
				block_ids.append(block)
				new_long = new_long >> bits_per_block

			#longs.append(new_long)
		#start = 0	
		
	
	'''	
	row = ""
	for i in range(0, len(block_ids)):
		if block_ids[i] < 10:
			row = row + str(block_ids[i]) + "- "
		else:
			row = row + str(block_ids[i]) + "-"
		if i % 16 == 0:
			print(row)
			row = ""
		if i % 256 == 0:
			print("\n")

	print(len(block_ids))
	'''
	
	
	chunk_section_data = []
	for i in range(0, 4096, 256):
		#print("Y value: " + str(i))
		y_block = []
		for j in range(i, i + 256, 16):
			#print(block_ids[j:j+16])
			x_row = block_ids[j:j+16]
			y_block.append(x_row)
		chunk_section_data.append(y_block)
	

	total_blocks = 0
	for y in chunk_section_data:
		for x_row in y:
			total_blocks += len(x_row)
	#print("Total number of blocks: " + str(total_blocks))

	#print(block_counts)		
	#myfile.close()

	success = StatusCode("SUCCESS", 0, "Success", chunk_section_data)
	#return chunk_section_data
	return success
	
def getChunksAndOffsets(NW_x, NW_z, SE_x, SE_z):
	NE_x = SE_x
	NE_z = NW_z

	SW_x = NW_x
	SW_z = SE_z

	NW_chunk_coords = playerCoordsToChunkCoords(NW_x, NW_z)
	SE_chunk_coords = playerCoordsToChunkCoords(SE_x, SE_z)

	#print("NW chunk coords:")
	#print(NW_chunk_coords)
	#print("SE chunk coords:")
	#print(SE_chunk_coords)

	NW_chunk_x = NW_chunk_coords[0]
	NW_chunk_z = NW_chunk_coords[1]
	SE_chunk_x = SE_chunk_coords[0]
	SE_chunk_z = SE_chunk_coords[1]

	selected_width = SE_x - NW_x + 1
	selected_height = SE_z - NW_z + 1
	#print("Selected width: " + str(selected_width))
	#print("Selected height: " + str(selected_height))


	x_dist_to_border = 16 - (NW_x % 16)
	#print("X dist to border: " + str(x_dist_to_border))
	#print(selected_width - x_dist_to_border)
	num_full_x_chunks = (selected_width - x_dist_to_border) // 16
	#print("Number of full x chunks: " + str(num_full_x_chunks))

	#incomplete_x = selected_width % 16
	incomplete_x = x_dist_to_border + (selected_width - x_dist_to_border - (num_full_x_chunks * 16))
	#print("Incomplete x: " + str(incomplete_x))
	left_incomplete_chunk_x_start = NW_x % 16
	#print("Left incomplete x: " + str(left_incomplete_chunk_x_start))
	right_incomplete_chunk_x_end = incomplete_x - (16 - left_incomplete_chunk_x_start)
	#print("Right incomplete x: " + str(right_incomplete_chunk_x_end))

	if right_incomplete_chunk_x_end == 0:
		right_incomplete_chunk_x_end = 16


	z_dist_to_border = 16 - (NW_z % 16)
	#print("Z dist to border: " + str(z_dist_to_border))
	#num_full_z_chunks = selected_height // 16
	#print(selected_height - z_dist_to_border)
	num_full_z_chunks = (selected_height - z_dist_to_border) // 16
	#print("Number of full z chunks: " + str(num_full_z_chunks))
	
	#incomplete_z = selected_height % 16
	incomplete_z = z_dist_to_border + (selected_height - z_dist_to_border - (num_full_z_chunks * 16))

	#print("incomplete z: " + str(incomplete_z))
	top_incomplete_z_start = NW_z % 16
	#print("Top incomplete z: " + str(top_incomplete_z_start))
	bottom_incomplete_z_end = incomplete_z - (16 - top_incomplete_z_start)
	#bottom_incomplete_z_end = selected_height - (16 - top_incomplete_z_start) + (16 * num_full_z_chunks)
	#print("Bottom incomplete z: " + str(bottom_incomplete_z_end))

	if bottom_incomplete_z_end == 0:
		bottom_incomplete_z_end = 16


	'''
	oooooooooooooooooooooooooooooooooooooooooooooo
	o              o              o              o
	o              o              o              o
	o              o              o              o
	o              o              o              o
	o              o              o              o
	o              o              o              o
	o         s    o              o   p          o
	o              o              o              o
	o         iiiiio              oiiii           o
	o              o              o              o
	o    v n  rrrrrhxxxxxxxxxxxxxxoxxxz          o
	o      n  z    h              o   z          o
	o      n  z    h              o   z          o
	o      n  z    h              o   z          o  h = selection height
	oooooooooowwwwwwwwwwwwwwwwwwwwwwwwwooooooooooo  w = selection width
	o         z    h              o   z          o  r = x_dist_to_border
	o         z    h              o   z          o  i = incomplete_x
	o         z    h              o   z          o  s = left_incomplete_x_start
	o         z    h              o   z          o  p = right_incomplete_x_end
	o         z    h              o   z          o  v = top_incomplete_z_start
	o         z    h              o   z          o  d = bottom_incomplete_z_end
	o         z    h              o   z          o  n = incomplete_z
	o         z    h              o   z          o
	o         z    h              o   z          o
	o         z    h              o   z          o
	o         z    h              o   z          o
	o         z    h              o   z          o
	o         z    h              o   z          o
	o         z    h              o   z          o
	oooooooooozoooohoooooooooooooooooozooooooooooo
	o      n  z    h              o   z          o
	o      n  z    h              o   z          o
	o      n  z    h              o   z          o
	o      n  z    h             o    z          o
	o    d n  zxxxxhxxxxxxxxxxxxxxxxxxz          o
	o              o              o              o
	o              o              o              o
	o              o              o              o
	o              o              o              o
	o              o              o              o
	o              o              o              o
	o              o              o              o
	o              o              o              o
	o              o              o              o
	oooooooooooooooooooooooooooooooooooooooooooooo
	'''


	chunks_data = []
	for i in range(NW_chunk_z, SE_chunk_z + 1):
		#x_pos_in_chunk = NW_x % 16
		#z_pos_in_chunk = NW_z % 16
		z_level = []
		x_start = 0
		z_start = 0

		x_end = 16
		z_end = 16

		if NW_chunk_z == SE_chunk_z:
			#special case: only one chunk is selected
			z_start = top_incomplete_z_start
			z_end = top_incomplete_z_start + selected_height
		else:
			#generic case: multiple chunks selected, i.e. NW_chunk_z != SE_chunk_z, or selection spans at least 2 chunks
			if i == NW_chunk_z:
				z_start = top_incomplete_z_start
			elif i == SE_chunk_z:
				z_start = 0
				z_end = bottom_incomplete_z_end
			else:
				z_start = 0
		for j in range(NW_chunk_x, SE_chunk_x + 1):

			chunk_data = {}
			chunk_data["x"] = j
			chunk_data["z"] = i

			#print("Chunk at x = " + str(j) + ", z = " + str(i))
			if NW_chunk_x == SE_chunk_x:
				x_start = left_incomplete_chunk_x_start
				x_end = left_incomplete_chunk_x_start + selected_width
			else:	
				if j == NW_chunk_x:
					x_start = left_incomplete_chunk_x_start
				elif j == SE_chunk_x:
					x_start = 0
					x_end = right_incomplete_chunk_x_end 
				else:
					x_start = 0
			chunk_data["x_start"] = x_start
			chunk_data["x_end"] = x_end
			chunk_data["z_start"] = z_start
			chunk_data["z_end"] = z_end

			#print("Chunk x start: " + str(x_start))
			#print("Chunk z start: " + str(z_start))
			#print("Chunk x end: " + str(x_end))
			#print("Chunk z end: " + str(z_end))
			z_level.append(chunk_data)
		chunks_data.append(z_level)
	print("Chunks and offsets data: ")
	print(chunks_data)
	return chunks_data	

#printPaletteData(chunk_x, chunk_z, 3)

#parseTileEntities(chunk_x, chunk_z)

#loadNamespacedIDMappings()

def handleSpecialMappingCases(block_name, properties, original_index): #returns a tuple containing the index and the rotation
	if block_name == "Redstone":
		#print("Found redstone")
		north = (properties["north"] == "side" or properties["north"] == "up") and properties["north"] != "none"
		east = (properties["east"] == "side" or properties["east"] == "up") and properties["east"] != "none"
		south = (properties["south"] == "side" or properties["south"] == "side") and properties["south"] != "none"
		west = (properties["west"] == "side" or properties["west"] == "side") and properties["west"] != "none"
		#print("North = " + str(north) + " east = " + str(east) + " west = " + str(west) + " south = " + str(south))
		if west and not east and not north and not south:
			return (original_index + 1, 0)
		elif south and not east and not north and not west:
			return (original_index + 2, 0)
		elif south and west and not north and not east:
			return (original_index + 3, 0)
		elif north and not east and not south and not west:
			return (original_index + 2, 0)
		elif north and west and not east and not south:
			return (original_index + 4, 0)
		elif north and south and west and not east:
			return (original_index + 7, 0)
		elif east and not north and not south and not west:
			return (original_index + 1, 0)
		elif east and south and not north and not west:
			return (original_index + 5, 0)
		elif east and south and west and not north:
			return (original_index + 8, 0)
		elif east and north and not south and not west:
			return (original_index + 6, 0)
		elif east and north and west and not south:
			return (original_index + 9, 0)
		elif east and north and south and not west:
			return (original_index + 10, 0)
		elif east and north and south and west:
			return (original_index + 11, 0)
		elif north and south and not east and not west:
			return (original_index + 2, 0)
		elif east and west and not north and not south:
			return (original_index + 1, 0)
		else:
			return (original_index, 0)
	elif " Bed" in block_name:
		#print("Found a bed with name " + str(block_name))
		bed_facing = properties["facing"]
		part = properties["part"]
		rotation = 0
		if bed_facing == "north":
			#print("Facing north...")
			rotation = 1
		elif bed_facing == "west":
			#print("Facing west...")
			rotation = 2
		elif bed_facing == "south":
			#print("Facing south...")
			rotation = 3
		if part == "foot":
			return (original_index + 1, rotation)
		else:
			return (original_index, rotation)
	elif " Log" in block_name or " Stem" in block_name:
		#print("Found a log")
		axis = properties["axis"]
		if axis == "x" or axis == "z":
			if axis == "z":
				return (original_index + 1, 0)
			else:
				return (original_index + 1, 1)
		else:
			return (original_index, 0)
	elif " Door" in block_name:
		door_index = original_index
		if properties["half"] == "lower":
			door_index += 1
		door_rotation = 0
		if properties["facing"] == "west":
			door_rotation = 1
		elif properties["facing"] == "north":
			door_rotation = 2
		elif properties["facing"] == "east":
			door_rotation = 3
		return (door_index, door_rotation)
	elif " Stairs" in block_name:
		stairs_rotation = 0
		if properties["half"] == "bottom":
			if properties["facing"] == "north" or properties["facing"] == "east":
				stairs_rotation = 1
		else:
			if properties["facing"] == "north" or properties["facing"] == "east":
				stairs_rotation = 2
			else:
				stairs_rotation = 3
		return (original_index, stairs_rotation)
	elif block_name == "Piston" or block_name == "Sticky Piston":
		piston_index = original_index
		if properties["facing"] == "north":
			piston_index += 1
		elif properties["facing"] == "south":
			piston_index += 2
		elif properties["facing"] == "west":
			piston_index += 3
		elif properties["facing"] == "east":
			piston_index += 4
		elif properties["facing"] == "down":
			piston_index += 5
		return (piston_index, 0)
	elif block_name == "Tall Seagrass":
		half_index = original_index
		if properties["half"] == "upper":
			half_index += 1
		return (half_index, 0)
	else:
		return (original_index, 0)




def load_main(NW_x, NW_z, SE_x, SE_z, lowest_y, world_name, file_name):
	print("Running main...")
	print("Northwest X: " + str(NW_x))
	print("Northwest Z: " + str(NW_z))
	print("Southeast X: " + str(SE_x))
	print("Southeast Z: " + str(SE_z))
	print("Lowest Y point: " + str(lowest_y))
	#NW_chunk_coords = playerCoordsToChunkCoords(NW_x, NW_z)
	#SE_chunk_coords = playerCoordsToChunkCoords(SE_x, SE_z)
	#print(NW_chunk_coords)
	#print(SE_chunk_coords)
	#NW_chunk_x = NW_chunk_coords[0]
	#NW_chunk_z = NW_chunk_coords[1]
	#SE_chunk_x = SE_chunk_coords[0]
	#SE_chunk_z = SE_chunk_coords[1]
	#print("NW chunk x: " + str(NW_chunk_x))
	#print("NW chunk z: " + str(NW_chunk_z))
	#print("SE chunk x: " + str(SE_chunk_x))
	#print("SE chunk z: " + str(SE_chunk_z))
	chunk_y_index = lowest_y // 16
	original_chunk_y_index = lowest_y // 16
	print("Chunk y index: " + str(chunk_y_index))
	namespaced_id_mappings = loadNamespacedIDMappings()
	name_to_index_mappings = loadNameToIndexMappings()
	#print(name_to_index_mappings)
	chunks = getChunksAndOffsets(NW_x, NW_z, SE_x, SE_z)
	#print("Successfully got chunk data")
	real_x = 0
	real_z = 0 #where in the selection (not the chunk) are we right now

	all_chunk_data = []
	highest_y = 0

	for z_level in chunks:

		chunk_selected_height = z_level[0]["z_end"] - z_level[0]["z_start"] #for all chunks in this z level, the chunk_selected_height will be the same

		for chunk in z_level:
			chunk_x = chunk["x"]
			chunk_z = chunk["z"]

			chunk_selected_NW_x = chunk["x_start"]
			chunk_selected_NW_z = chunk["z_start"]
			chunk_selected_SE_x = chunk["x_end"]
			chunk_selected_SE_z = chunk["z_end"]

			chunk_selected_width = chunk_selected_SE_x - chunk_selected_NW_x
			#chunk_selected_height = chunk_selected_SE_z - chunk_selected_NW_z

			first_time = True
			real_y = 0
			data_to_write = []
			while True:
				#chunk_section_data = printChunkData(chunk_x, chunk_z, chunk_y_index, world_name)
				
				
				chunk_section = printChunkData(chunk_x, chunk_z, chunk_y_index, world_name)
				#print(chunk_section)
				
				if chunk_section == -1:
					print("Chunk y index is out of bounds")
					break

				if chunk_section.getStatus() == "ERROR":
					chunk_section_error = StatusCode("ERROR", chunk_section.getErrorCode(), chunk_section.getErrorMessage(), None)
					return chunk_section_error
				chunk_section_data = chunk_section.getPayload()
				
				#print(chunk_section_data)
				if first_time:
					section_y = lowest_y % 16
					first_time = False #for this 16x16x16 chunk section, we load from the selected y index upwards. But on subsequent chunk sections, we load all the y's
				else:
					section_y = 0
				

				print("chunk selected NW x: " + str(chunk_selected_NW_x))
				print("chunk selected NW z: " + str(chunk_selected_NW_z))
				print("chunk selected SE x: " + str(chunk_selected_SE_x))
				print("chunk selected SE z: " + str(chunk_selected_SE_z))
				selected = []
				for y_level in range(section_y, len(chunk_section_data)):
					level = chunk_section_data[y_level]
					level_data = []
					for i in range(chunk_selected_NW_z, chunk_selected_SE_z):
						x_section = level[i][chunk_selected_NW_x:chunk_selected_SE_x]
						level_data.append(x_section)
					selected.append(level_data)

				'''
				print("Selected: ==================================")
				for y in range(0, len(selected)):
					for z in range(0, len(selected[y])):
						print(selected[y][z])
					print("New Y: ")
				print("============================================")
				'''
				print("Attempting to retrieve palette data:")
				#section_palette = printPaletteData(chunk_x, chunk_z, chunk_y_index, world_name)
				palette_data = printPaletteData(chunk_x, chunk_z, chunk_y_index, world_name)
				if palette_data.getStatus() == "ERROR":
					palette_error = StatusCode("ERROR", palette_data.getStatus(), palette_data.getErrorMessage(), None)
					return palette_error
				section_palette = palette_data.getPayload()

				print("Successfully retrieved palette data...")
				#print(loadNameToIndexMappings())
				#new_project_file = open("giant_leap.txt", "a")
				#new_project_file.write(str(len(selected)) + "\n")
				for y in range(0, len(selected)):
					for z in range(0, len(selected[y])):
						for x in range(0, len(selected[y][z])):
							block_chunk_id = selected[y][z][x]
							name = section_palette[block_chunk_id]['name']
							properties = section_palette[block_chunk_id]['properties']
							if name != 'Air' and name != 'Cave Air':
								#mchelper_id = name_to_index_mappings[name]
								#print(mchelper_id)
								mchelper_id = name_to_index_mappings[name]
								id_and_rotation = handleSpecialMappingCases(name, properties, mchelper_id)
								final_id = id_and_rotation[0]
								final_rotation = id_and_rotation[1]

								block_info = str(final_id) + "-" + str(real_y) +"-" + str(real_z + z) + "-" + str(real_x + x) + "-" + str(final_rotation) + "\n"
								#new_project_file.write(block_info)
								
								all_chunk_data.append(block_info)
								#data_to_write.append(block_info)
					real_y += 1
					if real_y > highest_y:
						highest_y = real_y
				#new_project_file.close()
				chunk_y_index += 1

			chunk_y_index = original_chunk_y_index
			real_x += chunk_selected_width

			'''
			new_project_file = open("giant_leap.txt", "a")
			new_project_file.write(str(real_y) + "\n")		
			for block in data_to_write:
				new_project_file.write(block)
			new_project_file.close()
			'''
		real_z += chunk_selected_height
		real_x = 0

	print("Highest y: " + str(highest_y))

	project_file_path = "projects\\"

	new_project_file = open(project_file_path + file_name + ".txt", "w")
	new_project_file.write(str(highest_y) + "\n")		
	for block in all_chunk_data:
		new_project_file.write(block)
	new_project_file.close()
	success_code = StatusCode("SUCCESS", 0, "Success", None)
	return success_code



#main(-3760, 784, -3749, 794, 61)

#main(-3776, 848, -3761, 863, 63)


#main2(-3776, 848, -3761, 863, 62)

#print(int(64 // 7))


#big house:
#load_main(-3794, 920, -3778, 944, 61, "World 1 copy for special testing", "giant_leap")


#superflat testing 1:
#load_main(-142, -109, -134, -99, 3, "superflat world 1", "superflat")

#superflat village:
#load_main(-222, -295, -188, -260, 3, "superflat world 1", "superflat_village")

def say_hello():
	print("Hello World")

filepath = "projects\\"
files = os.listdir(filepath)
print(files)

mypattern = re.compile("[-]?[0-9]{0,7}")
ret = mypattern.fullmatch("benjamin")
if ret:
	print("Matches")
else:
	print("Doesn't match")

#getVersion("Testing")

#print(b'\x03' == b'\x03')

#directory_contents = os.listdir("C:\\Users\\benja\\AppData\\Roaming\\.minecraft\\saves\\")
#print(directory_contents)

#available_chunk_files = os.listdir("C:\\Users\\benja\\AppData\\Roaming\\.minecraft\\saves\\superflat world 1\\region\\")
#print(available_chunk_files)

#var = "none"
#if var:
#	print("What")

#getChunksAndOffsets(43, -244, 67, -220)

#res = getChunksAndOffsets(76, -244, 83, -237)

#print(res)

#for i in range(351, 352):
#	print("Hello!")


#printPaletteData(chunk_x, chunk_z, 3)

#mynum = -3761 / 16
#print(mynum)

#print(math.floor(mynum))

'''
bm1 = get_bitmask_of_specified_length(1)
bm2 = get_bitmask_of_specified_length(2)
bm3 = get_bitmask_of_specified_length(3)
bm7 = get_bitmask_of_specified_length(7)
print(bm1)
print(bm2)
print(bm3)
print(bm7)
'''

#ret = printChunkData(-26, 13, 4, "post-116 world test")
#palette = printPaletteData(-26, 13, 4, "post-116 world test")

'''
block_name = "Redstone dust (east/west)"

if "(" in block_name:
	index = block_name.find("(")
	block_name = block_name[:index - 1]
	print("---" + block_name + "---")
else:
	print(block_name)
'''