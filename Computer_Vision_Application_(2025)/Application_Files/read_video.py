# read_video.py
# Created by Ariana Beeby, Max Figura, and Jason Jopp for CSC443
# reads video to perform object detection on 

import cv2 as cv
import detect
import gen_mask
import read_write_image
import contours

def read_video_from_file(file_path: str):
    """
    Reads in a video from a given file path
    Code largely following tutorial on openCv

    Parameters
    ----------
    file_path : str
        - The file location of the video 

    Return
    ----------
    cap: VideoCapture
        - The Video capture object, that can be read frame by frame
    """

    # Open the video file
    cap = cv.VideoCapture(file_path)
    
    # Check if the video was opened successfully
    if not cap.isOpened():
        print("Error: Could not open video file.")
    else:
        print("Video file opened successfully!")
    
    return cap

def process_video(cap: cv.VideoCapture, color, second_color=None, kernel_size=0):
    '''
    Takes a video and desired color range and detects that image 
    throughout the given video. Writing to new video file

    Parameters:
    cap : VideoCapture
        The video to process
     color : tuple (int)
        A tuple representing the color to detect as HSVA, 0-255 (0-359 for hue)
    second_color : tuple (int)
        A tuple representing the second color defining a range, or None if range selection is not used
    kernel_size : int
        The radius of the processing kernel
   
    Returns
    -------
    path_to_result : str
        The location and name of the processed video
    marked_cap : VideoWriter
        The processed video as VideoWriter Object
    '''
    # Modified from tutorial on opencv blog for reading and writing videos
    # Get video properties (e.g., frame count and frame width)
    frame_count = int(cap.get(cv.CAP_PROP_FRAME_COUNT))  # Get total number of frames in the video
    fps = float(cap.get(cv.CAP_PROP_FPS))  # Get frames per second (FPS)

    # Get frame width and height
    frame_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    
    # Define the codec and create VideoWriter object
    path_to_result = "output.avi"
    fourcc = cv.VideoWriter_fourcc(*"XVID")
    marked_cap = cv.VideoWriter(path_to_result, fourcc, fps, (frame_width, frame_height))

    # Read and display each frame of the video
    while True:
        ret, frame = cap.read()
        if not ret:
            print("End of video or error occurred.")
            break
    
        # PROCESS THE FRAME USING BLOB DETECTION
        color = gen_mask.hsv_color_standardizer(color)
        if (second_color):
            second_color = gen_mask.hsv_color_standardizer(second_color)
        mask = gen_mask.using_hsv_ranges(frame, color, kernel_size, second_color)
        marked_frame = detect.using_blobs(frame, mask)

        # Add marked frame to marked capture
        marked_cap.write(marked_frame)

    # Close capture
    cap.release()
    return path_to_result, marked_cap

def save_written_video(marked_cap: cv.VideoWriter):
    '''
    Releases the written video

    Parameters
    ----------
    marked_cap : VideoWriter
        The written video
    '''

    marked_cap.release()

# TODO Please fix this up! (functionality and organisation/documentation)
def first_frame(file_path: str):
    cap = read_video_from_file(file_path)
    ret, frame = cap.read()
    read_write_image.cache_working_image("first_frame", frame)
    return ".cache/first_frame-temp.png"

if __name__ == "__main__":
    print("Running read_video.py")
    cap = read_video_from_file("images/video_simple.mp4")
    color1 = [67, 1, 255]
    color2 = [172, 10, 255]
    path_to_result, marked_cap = process_video(cap,color1, color2 )
    save_written_video(marked_cap)
