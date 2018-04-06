import numpy as np
import cv2
import os
import shutil



def main():

	# input directory
	input_dir = 'GEI'

	# check if input directory exists
	if not os.path.exists(input_dir):
		raise Exception('No such input directory!')


	# output directory
	output_dir = 'DCT'

	# check if output directory exists
	if os.path.exists(output_dir):
		print(output_dir, 'directory exists!\nReplacing the contents!')
		shutil.rmtree(output_dir)

	# create output directory
	os.mkdir(output_dir)


	# list all the files
	files = [x for x in os.listdir(input_dir) if x.endswith('.png')]
	files.sort()


	# set max resolution of output image
	max_height = 256
	max_width = 256

	
	for im in files:
		# create a destination matrix
		output = np.zeros(shape=(max_height, max_width), dtype=np.float32)


		# path to the image
		src = os.path.join(input_dir, im)

		# read image
		image = cv2.imread(src, 0)

		# convert image to 32-bit floating-point
		image = np.float32(image)


		# resize image to maximum dimension
		image_new = cv2.resize(image, (max_height, max_width), interpolation=cv2.INTER_CUBIC)

		# apply DCT
		output = cv2.dct(image_new, output)

		# convert output to 64-bit integer
		output = np.int0(output)


		# image name
		name = 'DCT_' + im

		# destination path
		destination = os.path.join(output_dir, name)

		# write image
		cv2.imwrite(destination, output)

	
	print('Done!')


if __name__ == "__main__":
	main()