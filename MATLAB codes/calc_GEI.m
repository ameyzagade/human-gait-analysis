% input image format: img_proc_subjectsubjectno_imageno.png
% output image format: extracted_gei_subjectno.png
% input image dimension: variable sizes for each image
% output image dimension: unknown

close all;
pkg load image;


% width and height of the image
img_size_X = ;
img_size_Y = ;



% navigate to the directory containing processed silhouettes
files = dir (pwd);

% identify a directory using logical vector
dirFlag = [files.isdir];

% fetch only directories
subDirs = files (dirFlag);

% remove . and ..
subDirs (ismember ( {subDirs.name}, {'.', '..'} )) = [];

len_subdirs = length (subDirs);



% visit all the directories containing silhouettes
for counter = 1 : len_subdirs
 
	% enter directory
  	cd (subDirs(counter).name);

  
  	% image path
  	base_name = 'img_proc_';
  	subject = strcat ('subject', int2str(counter));
  	ext = '.png';

  
  	% initialize an empty matrix to store GEI
  	gait_energy_mat = zeros (img_size_X, img_size_Y);
	
  
  	% count total images in the directory
  	img_list = dir ('*.png');
  	img_count = length (img_list);

  
  	% calculate GEI
  	for count = 1 : img_count
    	img_name = strcat (base_name, subject, '_', int2str (count), ext);
    	img = imread (img_name);
  
  
    	% summation of each frame in the gait cycle
    	gait_energy_mat = gait_energy_mat + img;
    
  	end

  
  	multiply_factor = 1 / img_count;

  
  	% multiply the factor 1/N to get the gait energy image
  	gait_energy_mat = multiply_factor .* gait_energy_mat;

  
  	% write image to the same directory
  	file_name = strcat ('extracted_gei_', subject);
  	imwrite (gait_energy_mat, file_name, 'PNG');
  
  
  	% exit directory
  	cd ../;
  
end


clear;
