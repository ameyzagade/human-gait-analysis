import numpy as np
import cv2
import os
import shutil



# return largest contour from the list
def largest_contour(contours):
	
	# maximum contours in the list
	max_of_list = 0

	# list iterator
	list_no = 0

	# corresponding list number containing maximum contours
	ret_list = list_no


	# iterate through list of contours
	for i in contours:
		count = 0

		# count total coordinates in each contour
		for j in i:
			count += 1

		# store the position of largest contour
		if count > max_of_list:
			max_of_list = count
			ret_list = list_no
		list_no += 1

	# return the entire contour
	select_cnt = contours[ret_list]


	return select_cnt


# get largest contour for an image
def get_contour(image):

	# get contours
	im, contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	# return largest contour
	cnt = largest_contour(contours)


	return cnt


# output dimension of each image
def set_res(files, path):

	# initialize max width and height parameters
	set_width = 0
	set_height = 0


	for im in files:
		image_path = os.path.join(path, im)
		#read image
		image = cv2.imread(image_path, 0)

		# get largest contour for the image
		cnt = get_contour(image)

		# get bounding rectangle
		axis1, axis2, width, height = cv2.boundingRect(cnt)
		
		# set max width and height
		if width > set_width:
			set_width = width
		if height > set_height:
			set_height = height


	set_width +=  5
	set_height += 5


	return (set_height, set_width)


# normalized centred processing
def normalize(image, max_dim):
	
	# get largest contour for the image
	cnt = get_contour(image)

	# get bounding box
	x, y, width, height = cv2.boundingRect(cnt)


	# convert start coordinates to uint16
	# x = np.uint16(x)
	# y = np.uint16(y)

	# convert individual image dimensions to float
	width = np.float16(width)
	height = np.float16(height)

	# convert maximum output image dimension to float
	max_height, max_width = np.float16(max_dim)


	# check if the difference in width is an even number
	if not ((max_width - width) % 2):
		# if false then add 1
		width += 1
		
	# check if the difference in height is an even number
	if not ((max_height - height) % 2):
		# if false then add 1
		height += 1


	# calculate difference between maximum dimensions and current image dimensions along each axis 
	# take their halves, since the difference considers height and width on both sides of the image
	diff_x = (max_width - width) / 2
	diff_y = (max_height - height) / 2


	# coordinates for clipping
	x_new = x - diff_x
	y_new = y - diff_y

	if  (x_new < 1) or (y_new < 1):
		return None
	else:
		# end coordinates for trimming input image
		x_end = x + width + 1
		x_end = np.uint16(x_end)

		y_end = y + height + 1
		y_end = np.uint16(y_end)


		# start coordinates for output image
		x1 = np.uint16(diff_x)
		y1 = np.uint16(diff_y)

		# end coordinates for output image
		x2 = x1 + width + 1
		x2 = np.uint16(x2)

		y2 = y1 + height + 1
		y2 = np.uint16(y2)

		# initialize output image
		output_image = np.zeros(max_dim, dtype=np.uint8)


		# copy old image to new image
		output_image[y1:y2, x1:x2] = image[y:y_end, x:x_end]


		return output_image


def main():

	# input directory
	input_dir = 'processed'

	# check if input directory exists
	if not os.path.exists(input_dir):
		raise Exception('No such input directory!')
	

	# get all the subdirectories from the input directory
	list_dirs = [x for x in os.listdir(input_dir) if not os.path.isfile(x)]


	# output directory
	output_dir = 'aligned'

	# check if output directory exists
	if os.path.exists(output_dir):
		print(output_dir, 'directory exists!\nReplacing the contents!')
		shutil.rmtree(output_dir)

	# create output directory
	os.mkdir(output_dir)



	for d in list_dirs:
		# set the path of input subdirectory
		input_sub_dir = os.path.join(input_dir, d)


		# set the path of output subdirectory
		output_sub_dir = os.path.join(output_dir, d)

		# create output subdirectory
		os.mkdir(output_sub_dir)


		# get all the images with .png extension from sub-directory
		files = [x for x in os.listdir(input_sub_dir) if x.endswith('.png')]
		files.sort()

		# set max dimensions
		max_height, max_width = set_res(files, input_sub_dir)


		image_no = 1

		for im in files: 
			# path to image
			image_path = os.path.join(input_sub_dir, im)

			# read an image
			image = cv2.imread(image_path, 0)

			# apply normalized centred processing
			output_image = normalize(image, (max_height, max_width))

			if output_image is None:
				image_no += 1
				continue

			name = str(image_no) + '.png'
			destination_path = os.path.join(output_sub_dir, name)

			# write image
			cv2.imwrite(destination_path, output_image)

			image_no += 1


	print('Done!')

	
if __name__ == "__main__":
	main()