import cv2 as cv  # type: ignore
import numpy as np
import os
from status_codes import StatusCode
from tensorflow.keras.models import load_model # type: ignore

# Paths setup
BASE_DIR = os.path.dirname(__file__)
model_path = os.path.join(BASE_DIR, "model", "mnist_model.h5")
images_path = os.path.join(BASE_DIR, "images")

# Load model once
model = load_model(model_path)

def preprocess_cell(image):
    """
    Preprocess the cell image:
    - Crop 4 pixels from each border to avoid grid lines
    - Resize to 28x28 (MNIST input size)
    - Normalize pixels to [0,1]
    - Reshape for model input (28x28x1)
    """
    img = np.asarray(image)

    img = img[4:img.shape[0] - 4, 4:img.shape[1] - 4]
    
    img = cv.resize(img, (28, 28))
    img = img.astype('float32') / 255.0
    img = img.reshape(28, 28, 1)  # note: no batch dim here yet
    return img

def split_into_cells_batch(warped_img, model, threshold=0.7):
    """
    Split the sudoku image into 81 cells, preprocess each,
    and run batch prediction for digit recognition.
    Returns a 9x9 grid of detected digits (0 if empty or uncertain).
    """
    height, width = warped_img.shape[:2]
    cell_width = width // 9
    cell_height = height // 9

    cells = []
    for row in range(9):
        for col in range(9):
            x_start = col * cell_width
            y_start = row * cell_height
            cell_img = warped_img[y_start:y_start + cell_height, x_start:x_start + cell_width]
            preprocessed = preprocess_cell(cell_img)  # shape (28,28,1)
            cells.append(preprocessed)

    batch = np.array(cells)
    predictions = model.predict(batch)

    # Decode predictions
    results = []
    for pred in predictions:
        prob = np.max(pred)
        digit = np.argmax(pred)
        results.append(digit if prob > threshold else 0)

    # Convert flat list to 9x9 grid
    grid = [results[i*9:(i+1)*9] for i in range(9)]
    return grid

def warpedToGrid(id):
    """
    Read the sudoku image, recognize digits, and print the grid.
    """
    warped_path = os.path.join(images_path, f"sudoku_warped_{id}.png")
    warped = cv.imread(warped_path, cv.IMREAD_GRAYSCALE)

    grid = split_into_cells_batch(warped, model)
    if(os.path.exists(warped_path)):
        os.remove(warped_path)
    if grid is None:
        return None
    return grid

if __name__ == "__main__":
    os.system('clear')  # Clear terminal output (works on Mac/Linux)
    warpedToGrid()
