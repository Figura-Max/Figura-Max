# read_write_image.py
# Created by Ariana Beeby, Max Figura, and Jason Jopp for CSC443
# Reads in images with different color models

import cv2
import os


def bgr_from_path(image_path: str):
    """
    Given a image path to a BGR image, returns a np.array of an BGR image.

    Parameters
    ----------
    image_path : str
        The path the image to be read in
        
    Returns
    -------
    bgr_image : np.array
        The image which was read in, represented in the BGR colormodel
    """

    # Reads in an image as BGR color model
    bgr_image = cv2.imread(image_path, cv2.IMREAD_COLOR_BGR)

    return bgr_image

def write_image(image):
    """
    Given an image, writes the image to the images file as result.png
    
    Parameters
    ----------
    image : np.array
        The image that will be written to images/result.png

    Returns
    -------

    """
    path = "images/result.png" # Could change in future
    cv2.imwrite(path, image)

    return path

def cache_working_image(image_path : str, image):
    """
    Given an image a user is currently working on, save the image to the
    .cache folder.

    Parameter
    ----------
    image : np.array
        The image the user is currently working on, will be saved as
        "[filename]-temp.png" in the .cache directory.
    """
    image_name = os.path.basename(image_path)
    cv2.imwrite(f".cache/{image_name}-temp.png", image)

def save_image(raw_image, save_path, save_dims):
    """ Writes a raw processed image as desired by the user
    
    Parameters
    ----------
    raw_image : np.array
        The raw processed image
    save_path : str
        The location to save the final image to
    save_dims : (int, int)
        The width and height (in pixels) of the saved image
    """
    
    #TODO - resizing?
    
    cv2.imwrite(save_path, raw_image)
    
    return