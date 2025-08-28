# detect.py
# Created by Ariana Beeby, Max Figura, and Jason Jopp for CSC443
# Performs detection operations on provided images

import cv2
import numpy as np

def using_blobs(image: np.array, mask: np.array):
    """
    Given an image and a mask, uses basic blob detection to find objects.
    This function uses no blurring or other image transformations.

    Parameters
    ----------
    image : np.array
        The image which will be marked to show where detected objects are 
    mask : np.array
        The mask which blob detection will use to detect objects
        
    Returns
    -------
    marked_image : np.array
        An image which has been marked with ellipses to mark detected objects
    """

    # Initializes detector parameters, creates detector object
    params = cv2.SimpleBlobDetector_Params()
    params.filterByArea = False
    params.filterByCircularity = False
    params.filterByConvexity = False
    params.filterByInertia = False
    detector = cv2.SimpleBlobDetector_create(params)

    # Detector finds keypoints in the image, given it's current parameters
    keypoints = detector.detect(mask)

    marked_image = image

    for keypoint in keypoints:
        x, y = int(keypoint.pt[0]), int(keypoint.pt[1])
        radius = int(keypoint.size / 2)
        thickness = 20
        cv2.circle(marked_image, (x, y), radius, (0, 255, 0), thickness)

    # For troubleshooting, uncomment to view marked_image
    #cv2.imshow("Marked Image", marked_image)
    #cv2.waitKey(0)

    return marked_image