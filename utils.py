import global_vars
#from global_vars import max_building_size, min_building_size, max_building_colour, min_building_colour

def building_colour(size:int):
	

	building_size_range = global_vars.max_building_size-global_vars.min_building_size
	building_size_percent = 1-((size-global_vars.min_building_size)/building_size_range)
	print("___")
	print("size", size)
	print("sizerange", building_size_range)
	print("size%",building_size_percent)
	colour_range=global_vars.max_building_colour-global_vars.min_building_colour
	print("c_range",colour_range)
	colour = global_vars.min_building_colour + colour_range*building_size_percent

	print(colour)
	return(colour)
	pass