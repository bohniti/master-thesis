import cv2 as cv
import numpy as np

def laplace(img):
    """
    @file laplace_demo.py
    @brief Sample code showing how to detect edges using the Laplace operator
    @author: cv2 tutorial https://docs.opencv.org/3.4/d5/db5/tutorial_laplace_operator.html
    """
    # [variables]
    # Declare the variables we are going to use
    ddepth = cv.CV_16S
    kernel_size = 3
    window_name = "Laplace Demo"



    # Check if image is loaded fine
    if img is None:
        print('Error opening image')
        print('Program Arguments: [image_name -- default lena.jpg]')
        return -1
    # [load]
    # [reduce_noise]
    # Remove noise by blurring with a Gaussian filter
    print(type(img))
    src = cv.GaussianBlur(img, (3, 3), 0)
    # [reduce_noise]
    # [convert_to_gray]
    # Convert the image to grayscale
    src_gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    # [convert_to_gray]
    # Create Window
    cv.namedWindow(window_name, cv.WINDOW_AUTOSIZE)
    # [laplacian]
    # Apply Laplace function
    dst = cv.Laplacian(src_gray, ddepth, ksize=kernel_size)
    # [laplacian]
    # [convert]
    # converting back to uint8
    abs_dst = cv.convertScaleAbs(dst)

    return abs_dst
