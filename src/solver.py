from pre_process import pre_process
from exctraction import warpedToGrid
from status_codes import StatusCode
import copy
import os
import cv2 as cv # type: ignore
import pandas as pd # type: ignore

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # directory of current script
csv_path = os.path.join(BASE_DIR, "outputs")
images_path = os.path.join(BASE_DIR, "images")

def save_grid_to_csv(original_grid, solved_grid,id):
    marked_grid = []
    for i in range(9):
        row = []
        for j in range(9):
            if original_grid[i][j] == 0:
                row.append(-solved_grid[i][j])
            else:
                row.append(solved_grid[i][j])
        marked_grid.append(row)
    filename = os.path.join(csv_path, f"sudoku_solution_{id}.csv")
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    df = pd.DataFrame(marked_grid)
    df.to_csv(filename, index=False, header=False)


def is_valid(board, row, col, num):
    for i in range(9):
        if board[i][col] == num:
            return False
        if board[row][i] == num:
            return False
        if board[3 * (row // 3) + i // 3][3 * (col // 3) + i % 3] == num:
            return False
    return True

def solve(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                for num in range(1, 10):
                    if is_valid(board, i, j, num):
                        board[i][j] = num
                        if solve(board):
                            return True
                        board[i][j] = 0
                return False
    return True

def is_valid_initial_grid(grid):
    # Check rows
    for row in grid:
        nums = [num for num in row if num != 0]
        if len(nums) != len(set(nums)):
            return False

    # Check columns
    for col in range(9):
        nums = [grid[row][col] for row in range(9) if grid[row][col] != 0]
        if len(nums) != len(set(nums)):
            return False

    # Check 3x3 subgrids
    for box_row in range(3):
        for box_col in range(3):
            nums = []
            for i in range(3):
                for j in range(3):
                    val = grid[3 * box_row + i][3 * box_col + j]
                    if val != 0:
                        nums.append(val)
            if len(nums) != len(set(nums)):
                return False

    return True

# Main function
# Load the Sudoku grid from the image

def backend(id):
    val = pre_process(id)
    if(val != StatusCode.SUCCESS):
        return val
    # print("Image pre-processed successfully!")
    grid = warpedToGrid(id)
    if grid is None:
        return StatusCode.GRID_EXTRACTION_FAILED
    warped_path = os.path.join(images_path, f"sudoku_warped_{id}.png")
    if(os.path.exists(warped_path)):
        os.remove(warped_path)
    original_grid = copy.deepcopy(grid)
    if(not is_valid_initial_grid(grid)):
        return StatusCode.INVALID_INPUT
    
    if not solve(grid):
        return StatusCode.SUDOKU_UNSOLVABLE

    save_grid_to_csv(original_grid, grid,id)
    return StatusCode.SUCCESS

if __name__ == "__main__":
    backend()