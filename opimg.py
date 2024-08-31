import os, time
from PIL import Image

from bi import bicubic_resize
from reduce_img import reduce_image_by_factor

def op_dir(img_dir:str, is_simple:bool) -> None:
    og_size:int = Image.open(img_dir).size[0]
    curr_size:int = 0
    f_list = os.listdir(img_dir)
		
    if len(f_list) == 0:
        print("directory was empty...")
        return
    
    print("files in directory: ", f_list)

    for f in f_list:
        path:str = img_dir + "/" + f
        print("file:",f)
        img_size:str = str(os.path.getsize(path) / 1024) + "KB"
        
        if is_simple:
            factor = int(input("Enter reduction factor: "))
            reduce_image_by_factor(path, path, factor)
        else:
            reduce_image_by_factor(path, path, 10)
            curr_size = Image.open(img_dir).size[0]
            p = curr_size / og_size
            f = p * 100			
            ratio = f // 2
            print("ratio",ratio)
            bicubic_resize(path,ratio)
			
        comp_size:str = str(os.path.getsize(path) / 1024) + "KB"
        print("Original size: ", img_size,"\nCompressed Size", comp_size)

def op_img(img_path:str, is_simple) -> None:
    og_size:int = Image.open(img_path).size[0]
    factor:int = 0
    if is_simple:
        factor = int(input("Enter reduction factor: "))
        reduce_image_by_factor(img_path, img_path, factor)
    else:
        factor = calc_factor(og_size)
        if factor == 0:
            print("could not determine factor...")
            return
        reduce_image_by_factor(img_path, img_path, factor)			
        ratio = factor // 2
        print("ratio:",ratio)
        bicubic_resize(img_path,ratio)

def calc_factor(size:int) -> int:
    if size > 5000 and size < 10000:
        return 10
    if size < 3000:
        return 2
    if size < 4000:
        return 3
    if size < 5000:
        return 4
    