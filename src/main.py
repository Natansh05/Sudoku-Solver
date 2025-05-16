import streamlit as st # type: ignore
from sudoku_display import display_sudoku_grid
from PIL import Image
import pandas as pd # type: ignore
import os
import uuid
from status_codes import StatusCode, status_messages

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # directory of current script

unique_id = str(uuid.uuid4())
image_path = os.path.join(BASE_DIR, "images", f"sudoku_input_{unique_id}.png")
csv_path = os.path.join(BASE_DIR, "outputs", f"sudoku_solution_{unique_id}.csv")
os.makedirs(os.path.dirname(image_path), exist_ok=True)
os.makedirs(os.path.dirname(csv_path), exist_ok=True)


def showSolution():
    df = pd.read_csv(csv_path, header=None)
    st.subheader("Solved Sudoku")
    display_sudoku_grid(df)


st.title("Sudoku Solver 🧠")
st.divider()

st.subheader("Upload an image of a Sudoku puzzle and get it solved automatically.")

st.write("This app uses OpenCV + MNIST Model pretrained for digit recognition and backtracking for solving the puzzle.")

st.divider()


upload_method = st.selectbox("Upload Via:", ["File Upload", "Camera"])
uploaded_image = None
if upload_method == "Camera":
    uploaded_image = st.camera_input("Take a picture of the Sudoku puzzle")
else:
    uploaded_image = st.file_uploader("Insert the image of the Sudoku puzzle", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    st.success("Image uploaded successfully!")
    st.image(uploaded_image,width = 450, caption="Uploaded Image", use_container_width=False)
    st.write("Click the button below to solve the Sudoku puzzle.")

    if st.button("Solve Sudoku"):
        image = Image.open(uploaded_image)
        image.save(image_path)  # Save to use in backend()
        from solver import backend
        with st.spinner("Processing and solving the Sudoku..."):
            solve_status = backend(unique_id)
        if solve_status == StatusCode.SUCCESS:
            st.success(status_messages[solve_status])
            showSolution()
            st.balloons()
        else:
            st.error(status_messages.get(solve_status, "An unknown error occurred."))
            st.error("Please try again with a different image.")

if(os.path.exists(csv_path)):
    os.remove(csv_path)
if(os.path.exists(image_path)):
    os.remove(image_path)

st.divider()
st.info("Feedback feature coming soon!")
st.caption("Built with ❤️ by Natansh Shah | DA-IICT | 2025")