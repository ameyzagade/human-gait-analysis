# Extract frames from video file

def main():
    import numpy as num
    import cv2
    import os
    import shutil


    # input directory
    input_dir = 'videos'

    # get the names of mp4 files
    files = [x for x in os.listdir(input_dir) if x.endswith('.mp4')]


    # output directory
    output_dir = 'frames'
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    # create output directory
    os.mkdir(output_dir)


    # iterate through all the video files
    for vid_file in files:
        # path to the video file
        vid_path = os.path.join(input_dir, vid_file)
      

        # get video
        video = cv2.VideoCapture(vid_path)

        # get basename of the video file without file extension
        vid_name = os.path.splitext(vid_file)[0]


        basename = vid_name
        ext = '.png'

        # set output directory for each video
        output_dir_vid = os.path.join(output_dir, basename)
        os.mkdir(output_dir_vid)

        image_no = 1
        print(video.isOpened())
        while (video.isOpened()):
            # grab frame in the video
            # and the return value if grabbed
            ret_val, frame = video.read()
            print('#')
            print(ret_val)
            # check whether end of video is reached or not
            # and if reached, break out of the loop
            if (ret_val):
                # set output file name
                filename = ''.join ([basename, '_', str(image_no), ext])

                # set output file path
                output_path = os.path.join(output_dir_vid, filename)
            
                # write it to the output location
                cv2.imwrite (output_path, frame)

                image_no += 1
            else:
                break
    

            # close video file and release memory
            video.release()

if __name__ == "__main__":
    main()
