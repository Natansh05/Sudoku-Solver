import cv2 as cv # type: ignore
import numpy as np
import os
from status_codes import StatusCode

BASE_DIR = os.path.dirname(__file__)
images_path = os.path.join(BASE_DIR, "images")

def thresholding(image_np):
    gray = cv.cvtColor(image_np, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(gray, (5, 5), 1)
    thresh = cv.adaptiveThreshold(
        blurred, 255,
        cv.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv.THRESH_BINARY_INV,
        13, 2
    )
    return gray, blurred, thresh

def find_largest_contour(thresh_img):
    contours, _ = cv.findContours(thresh_img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    
    # Initialize
    largest_area = 0
    largest_contour = None
    
    # Loop through contours and find the largest one by area
    for contour in contours:
        area = cv.contourArea(contour)
        if area > largest_area:
            largest_area = area
            largest_contour = contour
            
    return largest_contour

def get_corners_from_contour(contour):
    peri = cv.arcLength(contour, True)
    approx = cv.approxPolyDP(contour, 0.02 * peri, True)
    
    if len(approx) == 4:
        corners = approx.reshape(4, 2)
        return corners
    else:
        return None 

def order_corners(corners):
    rect = np.zeros((4, 2), dtype="float32")
    
    s = corners.sum(axis=1)
    diff = np.diff(corners, axis=1)
    
    rect[0] = corners[np.argmin(s)]      # Top-left
    rect[2] = corners[np.argmax(s)]      # Bottom-right
    rect[1] = corners[np.argmin(diff)]   # Top-right
    rect[3] = corners[np.argmax(diff)]   # Bottom-left
    
    return rect

def pre_process(id):
    image_path = os.path.join(images_path, f"sudoku_input_{id}.png")
    img = cv.imread(image_path)
    if img is None:
        return StatusCode.IMAGE_NOT_FOUND
    img = cv.resize(img, (450, 450))
    gray, blurred, thresh = thresholding(img)
    largest_contour = find_largest_contour(thresh)
    
    if largest_contour is not None:
        corners = get_corners_from_contour(largest_contour)
        if corners is not None:
            pass
        else:
            return StatusCode.NOT_A_SUDOKU
    else:
        return StatusCode.NOT_A_SUDOKU

    rect = order_corners(corners)

    if rect is not None:
        # Perspective transformation
        width = 450
        height = 450
        dst = np.array([
            [0, 0],
            [width - 1, 0],
            [width - 1, height - 1],
            [0, height - 1]
        ], dtype="float32")
        M = cv.getPerspectiveTransform(rect, dst)
        warped = cv.warpPerspective(thresh, M, (width, height))
        warped_path = os.path.join(images_path,f"sudoku_warped_{id}.png")
        cv.imwrite(warped_path, warped)
        return StatusCode.SUCCESS
    else:
        return StatusCode.CORNER_ORDERING_FAILED

if __name__ == "__main__":
    pre_process()