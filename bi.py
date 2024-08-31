import cv2
import numpy as np
import math
import sys, time, os

#interpolation kernel
def u(s, a):
	if (abs(s) >= 0) and (abs(s) <= 1):
		return (a + 2) * (abs(s)**3) - (a + 3) * (abs(s)**2) + 1
	elif (abs(s) > 1 ) and (abs(s) <= 2):
		return a * (abs(s)**3) - (5 * a) * (abs(s)**2) + (8 * a) * (abs(s)) - 4 * a
	return 0

#padding - compute values of all pixels that lie within the boundary of the img.
def padding(img, h, w, c):
	zimg = np.zeros((h + 4, w+4, c))
	zimg[2:h+2, 2:w+2, :c] = img

	#pad the first/last two col and row
	zimg[2:h+2, 0:2, :c] = img[:, 0:1, :c]
	zimg[h+2:h+4, 2:w+2, :] = img[h-1:h, :, :]
	zimg[2:h+2, w+2:w+4, :] = img[:, w-1:w, :]
	zimg[0:2, 2:w+2, :c] = img[0:1, :, :c]

	#pad 8 missing points
	zimg[0:2, 0:2, :c] = img[0, 0, :c]
	zimg[h+2:h+4, 0:2, :c] = img[h-1, 0, :c]
	zimg[h+2:h+4, w+2:w+4, :c] = img[h-1, w-1, :c]
	zimg[0:2, w+2:w+4, :c] = img[0, w-1, :c]

	return zimg

#bicubic operation
def bicubic(img, ratio, a):
	#get image size
	h,w,c = img.shape
	
	#h= height, w=width
	#c = channels if img has color
	img = padding(img, h, w, c)

	#create new image
	dH = math.floor(h*ratio)
	dW = math.floor(w*ratio)

	#convert into matrix of zeros
	dst = np.zeros((dH, dW, 3))

	h = 1/ratio

	print('Starting bicubic interpolation. \nThis will take awhile...')
	inc = 0
	
	for k in range(c):
		for j in range(dH):
			for i in range(dW):

				#get the coordinates of nearby values
				x, y = i * h + 2, j * h + 2

				x1 = 1 + x - math.floor(x)
				x2 = x - math.floor(x)
				x3 = math.floor(x) + 1 - x
				x4 = math.floor(x) + 2 - x

				y1 = 1 + y - math.floor(y)
				y2 = y - math.floor(y)
				y3 = math.floor(y) + 1 - y
				y4 = math.floor(y) + 2 - y

				#consider all nearby 16 values
				mat_l = np.matrix([[u(x1,a), u(x2,a), u(x3,a), u(x4,a)]])				
				mat_m = np.matrix([[img[int(y-y1), int(x-x1), k], 
                                    img[int(y-y2), int(x-x1), k], 
                                    img[int(y+y3), int(x-x1), k], 
                                    img[int(y+y4), int(x-x1), k]], 
                                   [img[int(y-y1), int(x-x2), k], 
                                    img[int(y-y2), int(x-x2), k], 
                                    img[int(y+y3), int(x-x2), k], 
                                    img[int(y+y4), int(x-x2), k]], 
                                   [img[int(y-y1), int(x+x3), k], 
                                    img[int(y-y2), int(x+x3), k], 
                                    img[int(y+y3), int(x+x3), k], 
                                    img[int(y+y4), int(x+x3), k]], 
                                   [img[int(y-y1), int(x+x4), k], 
                                    img[int(y-y2), int(x+x4), k], 
                                    img[int(y+y3), int(x+x4), k], 
                                    img[int(y+y4), int(x+x4), k]]])
				mat_r = np.matrix(
					[[u(y1, a)], [u(y2, a)], [u(y3, a)], [u(y4, a)]]
				)

				#get dot product of 2 matrices
				dst[j, i ,k] = np.dot(np.dot(mat_l, mat_m), mat_r)
	
	#handle errors
	sys.stderr.write('\n')

	#flush buffer
	sys.stderr.flush()
	return dst

def bicubic_resize(img_file:str, ratio:int):
	img = cv2.imread(img_file)

	dst = bicubic(img, ratio, -1/2)
	print('done.')

	cv2.imwrite(img_file, dst)