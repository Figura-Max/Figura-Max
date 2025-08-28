# gen_mask.py
# Created by Ariana Beeby, Max Figura, and Jason Jopp for CSC443
# Performs masking operations on provided images

import cv2
import numpy as np

def hsv_color_standardizer(color: tuple):
    """
    Given a tuple in HSV color model from GUI, standardizes values to match OpenCV standards
    
    Parameters
    ----------
    color : tuple
        The orignial tuple representing the color in GUI based HSV color model

    Returns
    ----------
    color : list
        The same color now represented in the HSV color model with hue scaled to OpenCV (1/2)
    """
    # This will need to be moved to it's own file, just converting HSV scale to OpenCV's
    color = [*color][0:3] # Unpacks tuple into list, takes first three entries

    # I saw an issue where a dimension of the color returned -1
    for dim in color:
        if dim < 0:
            dim = 0

    # Converting hue value to OpenCV scale
    color[0] = round(color[0]/2)
    return color

def using_hsv_ranges(image: np.array, color: list, kernel_size: int, second_color=None):
    """
    Given an RGB image, and HSV color model bounds, returns a mask which
    masks all pixels which do not fall within the provded bounds.

    Given a non-zero kernel_size, will apply a gaussian blur to the image.

    Parameters
    ----------
    image : np.array
        The image which will be masked by the hsv range
    color : list
        Either a 3-dim color in HSV color model, or a 6-dim HSV color range
    kernel_size : int
        The size of the kernel used for image transformations like blurring
        
    Returns
    -------
    mask : np.array
        The mask representing the portions of the image which were not filtered
        by the HSV lower and upper bounds.
    """

    # Applied Gaussian Blurring to image if kernel_size is > 0 (present)
    if (kernel_size > 0):
        # Prevents even number kernel by subtracting 1 from provided even ints
        kernel_size = (lambda kernel_size : kernel_size if (kernel_size % 2 != 0) else kernel_size - 1)(kernel_size)
        image = cv2.GaussianBlur(image,(kernel_size,kernel_size),0)


    # Converts the image to the HSV color model
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Uses the second color as the upper bound if it's available
    if (second_color != None):
    # Creates lower and upper bounds for mask creation, creates the mask
        lower_bound = np.array([color[0], color[1], color[2]])
        upper_bound = np.array([second_color[0], second_color[1], second_color[2]])
    
    else:
        # Looks like color was passed as specific value, can apply a range to color
        hsv_color_ranges = []
        
        # Sets lower bounds of HSV -10, or zero if it were to go negative
        for dimension in color:
            hsv_color_ranges.append((lambda dimension: dimension - 10 if dimension > 10 else 0)(dimension))

        # Sets upper hue value to hue + 10, or 179 if hue + 10 > 179
        hsv_color_ranges.append((lambda hue: hue + 10 if hue <= 169 else 179)(color[0]))

        # Sets value, saturation value to +10, unless it would be > 255, then 255
        for dimension in color[1:3]:
            hsv_color_ranges.append((lambda dim: dim + 10 if dim <= 245 else 255)(dimension))

        lower_bound = np.array([hsv_color_ranges[0], hsv_color_ranges[1], hsv_color_ranges[2]])
        upper_bound = np.array([hsv_color_ranges[3], hsv_color_ranges[4], hsv_color_ranges[5]])

    # Generates a mask using the HSV ranges and image provided
    mask = cv2.inRange(hsv_image, lower_bound, upper_bound)

    if (kernel_size > 0):
        # Applies additional transformations
        kernel = np.ones((kernel_size,kernel_size), np.uint8)
        #mask = cv2.erode(mask, kernel, iterations=1)
        mask = cv2.dilate(mask, kernel, iterations=1)

    # Places a small border around the image so blobs can be detected on image edge
    mask = cv2.copyMakeBorder(mask, 2, 2, 2, 2, cv2.BORDER_CONSTANT, value=[0, 0, 0]) 

    # For some reason, need to flip mask for detector to work properly
    mask = cv2.bitwise_not(mask)

    return mask