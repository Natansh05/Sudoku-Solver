# status_codes.py
from enum import Enum

class StatusCode(Enum):
    SUCCESS = 0
    IMAGE_NOT_FOUND = 1
    GRID_EXTRACTION_FAILED = 2
    SUDOKU_UNSOLVABLE = 3
    INVALID_INPUT = 4
    MODEL_LOAD_FAILED = 5
    NOT_A_SUDOKU = 6
    GRID_CONTOUR_NOT_FOUND = 7
    GRID_CORNER_DETECTION_FAILED = 8
    CORNER_ORDERING_FAILED = 9


status_messages = {
    StatusCode.SUCCESS: "Sudoku solved successfully!",
    StatusCode.IMAGE_NOT_FOUND: "Input image not found. Please upload a valid image.",
    StatusCode.GRID_EXTRACTION_FAILED: "Sudoku Grid could not be extracted from the image.",
    StatusCode.SUDOKU_UNSOLVABLE: "Sudoku could not be solved. Please check the input grid.",
    StatusCode.INVALID_INPUT: "Invalid input grid. Sudoku rules are violated.",
    StatusCode.MODEL_LOAD_FAILED: "Digit recognition model could not be loaded.",
    StatusCode.NOT_A_SUDOKU: "The image does not appear to contain a Sudoku puzzle.",
    StatusCode.GRID_CONTOUR_NOT_FOUND: "Could not find the grid contour in the image.",
    StatusCode.GRID_CORNER_DETECTION_FAILED: "Failed to detect the four corners of the Sudoku grid.",
    StatusCode.CORNER_ORDERING_FAILED: "Could not properly order the detected corners. Please try again.",
}