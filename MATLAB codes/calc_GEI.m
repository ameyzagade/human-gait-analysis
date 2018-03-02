close all;

% change as per required
rows = 240;
columns = 352;

% navigate to the directory containing processed silhouettes
% edit the base file name as per your requirements 
base_file_name = '';
extension = '.png';

% initialize an empty matrix to store GEI
gait_energy_mat = zeros(rows, columns);

% count total images in the directory
[files, err, msg] = readdir (pwd);
total_files = length (files) - 2;

factor = 1 / total_files;

for file_no = 1: total_files
  image_name = strcat (base_file_name, int2str (file_no), extension);
  image = imread(image_name);
  
  % summation of each frame in the gait cycle
  gait_energy_mat = gait_energy_mat + image;
end

% multiply the factor 1/N to get the gait energy image
gait_energy_mat = times(factor, gait_energy_mat);

% write image to the same directory
file_name = strcat(base_file_name, '_', 'extracted_gei');
imwrite(gait_energy_mat, file_name, 'PNG');
