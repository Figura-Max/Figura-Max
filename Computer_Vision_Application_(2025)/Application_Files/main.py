# main.py
# Created by Ariana Beeby, Max Figura, and Jason Jopp for CSC443
# Initial main driver for Computer Vision project

import detect
import gen_mask
import read_write_image
import user_interface
import plot
import contours
import read_video

def main():
    """ Main driver - Creates GUI object and specifies how functionalities should be linked
    """
    
    # Create user interface instance
    app, gui = user_interface.create_gui()
    # Connect functionalities with UI actions
    gui.connectAnalyse(main_processing)
    gui.connectVideoAnalyse(video_processing)
    gui.connectSave(save_file)
    gui.connectGetCPRangeFile(plot.hsv_color_range)
    gui.connectGetVideoFrame(read_video.first_frame)
    # Begin event-driven loop - no main() code after this line will be run!
    user_interface.start_gui(app, gui)
    
    print("An unexpected error occurred. The event-driven loop ended without the program terminating.")

def main_processing(image_path, color=None, second_color=None, detect_mode=1, kernel_size=0, contour_point=(0.0,0.0)):
    """ Calls the functional parts of the program from GUI
    
    Parameters
    ----------
    image_path : str
        The location of the input image file
    color : tuple (int)
        A tuple representing the color to detect as HSVA, 0-255 (0-359 for hue)
    second_color : tuple (int)
        A tuple representing the second color defining a range, or None if range selection is not used
    detect_mode : int
        The detection mode in use (1 = blobs, 2 = contours)
    kernel_size : int
        The radius of the processing kernel
    contour_point : tuple (float)
        An ordered pair representing the location the user wishes to look for contours as a fraction of the width and height of the image
    
    Returns
    -------
    path_to_result : str
        The location of the output image file
    marked_image : np.array
        The raw processed image
    """

    image = read_write_image.bgr_from_path(image_path)
    color = gen_mask.hsv_color_standardizer(color)
    if (second_color):
        second_color = gen_mask.hsv_color_standardizer(second_color)
    mask = gen_mask.using_hsv_ranges(image, color, kernel_size, second_color)
    marked_image = None
    if detect_mode == 2:
        marked_image = contours.using_contours(image, mask)
    else:
        marked_image = detect.using_blobs(image, mask)
    path_to_result = read_write_image.write_image(marked_image)

    return path_to_result, marked_image

def video_processing(video_path, color=None, second_color=None, detect_mode=1, kernel_size=0):
    """ Calls the video-processing functionalities from GUI
    
    Parameters
    ----------
    video_path : str
        The location of the input image file
    color : tuple (int)
        A tuple representing the color to detect as HSVA, 0-255 (0-359 for hue)
    second_color : tuple (int)
        A tuple representing the second color defining a range, or None if range selection is not used
    detect_mode : int
        The detection mode in use (1 = blobs, 2 = contours)
    kernel_size : int
        The radius of the processing kernel
    
    Returns
    -------
    path_to_result : str
        The location of the output image file
    """

    video = read_video.read_video_from_file(video_path)
    path_to_result, marked_cap = read_video.process_video(video, color, second_color, kernel_size)
    read_video.save_written_video(marked_cap)

    return path_to_result

def save_file(raw_image, save_path, save_dims):
    """ Saves a raw cached output image into the desired location
    
    Parameters
    ----------
    raw_image : np.array
        The raw processed image
    save_path : str
        The location to save the final image to
    save_dims : (int, int)
        The width and height (in pixels) of the saved image
    """
    
    #print(raw_image, save_path, save_dims)
    read_write_image.save_image(raw_image, save_path, save_dims)

    return

if __name__ == "__main__":
    main()
