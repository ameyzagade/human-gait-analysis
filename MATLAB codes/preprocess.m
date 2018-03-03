% input image format: img_extract_subjectsubjectno_imageno.png
% output image format: img_proc_subjectsubjectno_imageno.png
% input image dimension: 352 x 240
% output image dimension: variable sizes for each image


close all;
pkg load image;


% width and height of the image
img_size_X = 240;
img_size_Y = 352;



% navigate to the directory containing extracted silhouettes
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
  	base_name = 'img_extract_';
  	subject = strcat ('subject', int2str (counter));
  	ext = '.png';
  
  	% count total images in the directory
  	img_list = dir ('*.png');
	img_count = length (img_list);
  
  	for count = 1 : img_count
  		img_name = strcat (base_name, subject, '_', int2str (count), ext);
    	img = imread (img_name);
  
    	% perform erosion operation
  
    	% perform dilation operation
  
    	% perform normalized-centred processing  
    	img_stats = regionprops (img, "FilledImage");
    	img_centred = img_stats.FilledImage;
  
	    % save the processed image
    	file_name = strcat ('img_proc_', subject, '_', int2str (count), ext);
    	imwrite (img_centred, file_name, 'PNG');
    	
  	end
  
  	% exit directory
  	cd ../;
  
end


clear;
