import os, time
from PIL import Image

from opimg import op_dir, op_img

def optimize(img_path:str, is_simple:bool)-> None:
	img_size:int = 0
	comp_size:int = 0

	#if dir
	if os.path.isdir(img_path):
		op_dir(img_path, is_simple)
	#if file
	elif os.path.isfile(img_path):
		op_img(img_path, is_simple)
	else:
		print("Input is invalid...")

def simple_reduction(simple:str) -> bool:
	if simple == "y":
		return True
	else:
		return False

if __name__ == "__main__":
	img_dir:str = input("enter image dir or image path: ")
	start = time.time()
	simple:str = input("Simple reduction(y/n)? ")
	is_simple:bool = simple_reduction(simple)
	optimize(img_dir, is_simple)
	end = time.time()
	final = end - start
	print("time elapsed: ",final, "second(s)") if final < 60 else print("time elapsed: ",final / 60, "minute(s)")
