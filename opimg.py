import os, time
from PIL import Image

from bi import bicubic_resize
from simple import reduce_image_by_factor

def optimize(img_path:str)-> None:
	simple:str = input("Simple reduction(y/n)? ")
	is_simple:bool = simple_reduction(simple)
	img_size:int = 0
	comp_size:int = 0
	
	#dir
	if os.path.isdir(img_path):
		f_list = os.listdir(img_path)
		
		if len(f_list) == 0:
			return "directory was empty..."
		print("files in directory: ", f_list)
		
		for f in f_list:
			path:str = img_path + "/" + f
			og_size:int = Image.open(path).size[0]
			print("file:",f)
			img_size:str = str(os.path.getsize(path) / 1024) + "KB"
			
			if is_simple:
				factor = int(input("Enter reduction factor: "))
				reduce_image_by_factor(path, path, factor)
			else:
				reduce_image_by_factor(path, path, 10)
				curr_size:int = Image.open(path).size[0]
				p = curr_size / og_size
				f = p * 100			
				ratio = f // 2
				print("ratio",ratio)
				bicubic_resize(path,ratio)
			
			comp_size:str = str(os.path.getsize(path) / 1024) + "KB"
			print("Original size: ", img_size,"\nCompressed Size", comp_size)
	#file
	else:
		if is_simple:
			factor = int(input("Enter reduction factor: "))
			reduce_image_by_factor(img_path, img_path, factor)
		else:
			reduce_image_by_factor(img_path, img_path, 10)
			curr_size = Image.open(img_path).size[0]
			p = curr_size / og_size
			f = p * 100			
			ratio = f // 2
			print("ratio:",ratio)
			bicubic_resize(img_path,ratio)

def simple_reduction(simple:str) -> bool:
	if simple == "y":
		return True
	else:
		return False

if __name__ == "__main__":
	img_dir:str = input("enter image dir: ")
	start = time.time()
	optimize(img_dir)
	end = time.time()
	final = end - start
	print("time elapsed: ",final, "second(s)") if final > 60 else print("time elapsed: ",final / 60, "minute(s)")
