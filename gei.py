import numpy as np
import cv2
import os
import shutil


def main():

	# input directory
	input_dir = 'gaitcyle'

	# check if input directory exists
	if not os.path.exists(input_dir):
		raise Exception('No such input directory!')
	

	# get all the subdirectories from the input directory
	list_dirs = [x for x in os.listdir(input_dir) if not os.path.isfile(x)]


	# output directory
	output_dir = 'GEI'

	# check if output directory exists
	if os.path.exists(output_dir):
		print(output_dir, 'directory exists!\nReplacing the contents!')
		shutil.rmtree(output_dir)

	# create output directory
	os.mkdir(output_dir)

	# subject count
	subject_no = 1

	for d in list_dirs:
		# set the path of input subdirectory
		input_sub_dir = os.path.join(input_dir, d)


		# # set the path of output subdirectory
		# output_sub_dir = os.path.join(output_dir, d)

		# # create output subdirectory
		# os.mkdir(output_sub_dir)

		# get all the images with .png extension from sub-directory
		files = [x for x in os.listdir(input_sub_dir) if x.endswith('.png')]
		files.sort()

		
		# get input path for sample image
		input_path = os.path.join(input_sub_dir, files[0])

		im = cv2.imread(input_path, 0)

		# get shape of sample image for reference height and width
		height, width = im.shape
		
		# initialize numpy array of zeros for gait energy image
		gait_energy = np.zeros((height, width), np.float32)
		
		total_images = 0

		for im in files:
			# path to image
			image_path = os.path.join(input_sub_dir, im)

			# read an image
			image = cv2.imread(image_path, 0)

			# add each image to overall gait energy image
			gait_energy += np.float32(image)

			total_images += 1


		factor = np.float16(1 / total_images)

		# multiply final gait energy image for each subject with factor
		gait_energy *= factor

		gait_energy = np.int0(gait_energy)

		name = 'GEI' + str(subject_no) + '.png'

		# output path of image
		destination_path = os.path.join(output_dir, name)

		# write image
		cv2.imwrite(destination_path, gait_energy)


		# since the GEi contains salt-and-pepper noise
		# use median filter

		gait_energy = cv2.imread(destination_path, 0)

		# kernel size of median blur filter
		kernel_size = 9

		# apply median blur
		gait_energy = cv2.medianBlur(gait_energy, kernel_size)

		# write modified image
		gait_energy = cv2.imwrite(destination_path, gait_energy)


		subject_no += 1


	print('Done!')

if __name__ == "__main__":
	main()