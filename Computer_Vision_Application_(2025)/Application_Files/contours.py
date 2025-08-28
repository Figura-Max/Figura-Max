# contours.py
# Created by Ariana Beeby, Max Figura, and Jason Jopp for CSC443
# Performs operations with contours on provided images

import cv2 as cv
import numpy as np
import gen_mask
import read_write_image

def using_contours(img: np.array, mask: np.array):
    """
    Given an image and a mask of the image, draw contours
    around the colors and return that image 

    Parameters
    ----------
    img : np.array
        The original image
    m_img : np.array
        The mask of the image

    Return
    ----------
    contoured_image: np.array

    """

    c = contours(img, mask)
    cv.drawContours(img, c, -1, (255, 105, 180), 3) # contours drawn in hot pink
    return img

def contours(img: np.array, m_img: np.array):
    """
    Given an image and a mask of the image, finds contours of the mask 

    Parameters
    ----------
    img : np.array
        The original image
    m_img : np.array
        The mask of the image

    Return
    ----------
    contours: np.array

    """
    # need to invert images
    m_img = cv.bitwise_not(m_img)

    rect,thresh = cv.threshold(m_img, 127,255,0)

    # Note, findContours alters the image
    contours, hierarcy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    return contours

def convex_hull(contours: np.array):
    # temp
    return

def centroid(contours: np.array):
    """
    Given the contours of an image, calculates and returns the centroids of each contour
    The centroids are stored in a list as tuple (x,y) coordinates

    Parameters
    ----------
    contours : np.array
        The contours of the image
    
    Return
    ----------
    centroids: list
    """
    centroids = []
    for c in contours:
        M = cv.moments(c)
        if M['m00'] != 0:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00']) 
            centroids.append((cx,cy))
    return centroids

def draw_centroids(centroids: list, img: np.array, color: tuple):
    """
    Given a list of centroid coordinates, draw them onto the image
    The centroids are drawn as circles of radius 5 with the given color
    Changes the passed image

    Parameters
    ----------
    centroids : list
        The centroid locations for the desired image
    img : np.array
        The image 
    color: tuple
        The color for drawing the centroids in RGB
    """

    for pair in centroids:
        cv.circle(img, pair, 5, color, -1)

def grab_shape(coord: tuple, contours: np.array):
    """
    Given a coordinate and a list of centroids, 
    return the contour that the point is contained in
    or null if none

    Parameters
    ---------- 
    coord: tuple
        The coordinate selected
    contours: np.array
        The array of all contours of the image
    
    Return
    ----------
    cont: list
        the shape containing the given coordinate
    """

    '''
    The format of a contour for a single shape is in np.array format
    array([[[859, 635]], [[859, 661]], [[883, 661]], [[883, 635]]], dtype=int32)
    '''
    

if __name__ == "__main__":
    img = read_write_image.bgr_from_path("images/pink_ball.jpg")
    ## Note, with this mask creates outline of total image becuase will outline solid white shapes
    mask = gen_mask.using_hsv_ranges(img, [162, 30, 10],  0, [172, 255, 255])
    cv.imshow("mask", mask)
    contoured_img = using_contours(img, mask)
    cv.imshow("contoured", contoured_img)
    c = contours(img, mask)
    grab_shape((100,100), c)
    print(centroid(c))
    draw_centroids(centroid(c), img, (0,0,0))
    cv.imshow("Centroids", img)
    cv.waitKey(0)
