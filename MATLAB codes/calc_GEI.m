% close all windows
close all;

% rows and columns of matrix
% change as per required
row = 240;
col = 352;

% navigate to the directory containing processed silhouettes
base_file_name = 'img_proc_';
subject = 'subject1';
ext = '.png';

% initialize an empty matrix to store GEI
gait_energy_mat = zeros (row, col);

% count total images in the directory
file_list = dir ('*.png');
img_count = length (file_list);

for count = 1: img_count
  img_name = strcat (base_file_name, subject, '_', int2str (count), ext);
  img = imread (img_name);
  
  % summation of each frame in the gait cycle
  gait_energy_mat = gait_energy_mat + img;
end

multiply_factor = 1 / total_files;

% multiply the factor 1/N to get the gait energy image
gait_energy_mat = multiply_factor .* gait_energy_mat;

% write image to the same directory
file_name = strcat('extracted_gei', subject);
imwrite(gait_energy_mat, file_name, 'PNG');
