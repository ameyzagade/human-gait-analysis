#
#
#

import numpy as np
import cv2
import shutil
import os


# perform some filtering before processing the image
def denoise(frame):

	# kernel size
	# should be an odd positive integer
	median_kernel_size = 5

	# apply median blur
	frame = cv2.medianBlur(frame, median_kernel_size)

	# height and width of the gaussian kernel
	# should be an odd positive integer
	gauss_blur_height = 5
	gauss_blur_width = 5

	# standard deviation in X and Y direction
	sigma_x = 0
	sigma_y = 0

	# apply gaussian blur
	frame = cv2.GaussianBlur(frame, (gauss_blur_height, gauss_blur_width), sigma_x, sigma_y)

	return frame


def main():

    # input directory
    input_dir = 'frames'
    if not input_dir:
    	raise Exception('No such input directory!')

    # get the names of jpeg files
    files = [x for x in os.listdir(input_dir) if x.endswith('.jpeg')]
    files.sort()

    # output directory
    output_dir = 'silhouettes'
    if os.path.exists(output_dir):
    	print(output_dir, 'directory exists!\nReplacing the contents!')
    	shutil.rmtree(output_dir)

    # create output directory
    os.mkdir(output_dir)

    # rate at which the algorithm is going to learn
    # value should be between 0 and 1
    # increase value if the environment is moving quickly
    ALPHA = 0.009

    # path to the first image
    image_path = os.path.join(input_dir, files[0])

    # read image
    image = cv2.imread(image_path)

    # check if image exists
    if image is None:
    	raise Exception("Could not load initial image")

    # create a background model
    # fetch the first image and convert it to grayscale 
    # and then apply denoise function
    bg_model = denoise(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))    

    for i in files:

        # path to the image
        image_path = os.path.join(input_dir, i)

        image = cv2.imread(image_path)
        
        # create a foreground model of the current image
        # fetch each image and convert it to grayscale 
        fg_model = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # create new background model for each image
        bg_model = fg_model * ALPHA + bg_model * (1 - ALPHA)

        # calculate mask
        mask = cv2.absdiff(fg_model.astype(np.uint8), bg_model.astype(np.uint8))

        # select any value between min and max
        min_val = 50
        max_val = 255

        # apply thresholding on the background
        ret_val, mask = cv2.threshold(mask.astype(np.uint8), min_val, max_val, cv2.THRESH_BINARY)

        output_path = os.path.join(output_dir, i)
        cv2.imwrite(output_path, mask)

if __name__ == "__main__":
	main()