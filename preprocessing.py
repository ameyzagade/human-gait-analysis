# apply erosion, dilation, opening and closing operations

import numpy as np
import cv2
import os
import shutil


def erosion(frame):

	# kernel size
	kernel_height = 5
	kernel_width = 5

	# number of iterations
	iterations = 1
	
	# set kernel
	kernel = np.ones((kernel_height, kernel_width), np.uint8)

	# perform erosion
	frame  = cv2.erode(frame, kernel, iterations)

	return frame


def dilation(frame):

	# kernel size
	kernel_height = 5
	kernel_width = 5

	# number of iterations
	iterations = 1
	
	# set kernel
	kernel = np.ones((kernel_height, kernel_width), np.uint8)

	# perform dilation
	frame  = cv2.dilate(frame, kernel, iterations)

	return frame


def opening(frame):

	# kernel size
	kernel_height = 3
	kernel_width = 3

	# set kernel
	kernel = np.ones((kernel_height, kernel_width), np.uint8)

	# perform opening operation
	frame = cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel)

	return frame


def closing(frame):

	# kernel size
	kernel_height = 5
	kernel_width = 5

	# set kernel
	kernel = np.ones((kernel_height, kernel_width), np.uint8)

	# perform opening operation
	frame = cv2.morphologyEx(frame, cv2.MORPH_CLOSE, kernel)

	return frame


def main():
	# input directory
    input_dir = 'silhouettes'

    if not input_dir:
    	raise Exception('No such input directory!')

    # get the names of jpeg files
    files = [x for x in os.listdir(input_dir) if x.endswith('.jpeg')]
    files.sort()

    # output directory
    output_dir = 'processed'
    
    if os.path.exists(output_dir):
    	print(output_dir, 'directory exists!\nReplacing the contents!')
    	shutil.rmtree(output_dir)

    # create output directory
    os.mkdir(output_dir)

    # get the names of jpeg files
    files = [x for x in os.listdir(input_dir) if x.endswith('.jpeg')]
    files.sort()

    for i in files:

    	# path to the image
        image_path = os.path.join(input_dir, i)

        image = cv2.imread(image_path)
		
		# opening
        image = opening(image)

        # closing
        image = closing(image)

        output_path = os.path.join(output_dir, i)
        cv2.imwrite(output_path, image)

if __name__ == "__main__":
	main()