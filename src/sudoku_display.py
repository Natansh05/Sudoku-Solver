# sudoku_display.py
import streamlit as st # type: ignore

def display_sudoku_grid(dataframe):
    st.markdown(
        f"""
        <style>
        .sudoku-grid {{
            display: grid;
            grid-template-columns: repeat(9, 50px);
            grid-template-rows: repeat(9, 50px);
            gap: 0px;
        }}
        .sudoku-cell {{
            background-color: white;
            text-align: center;
            font-size: 20px;
            font-weight: bold;
            line-height: 50px;
            width: 50px;
            height: 50px;
        }}
        </style>
        <div class="sudoku-grid">
        {''.join(
            f'<div class="sudoku-cell" style="{get_cell_style(i, j, val)}">{abs(val)}</div>'
            for i, row in enumerate(dataframe.values)
            for j, val in enumerate(row)
        )}
        </div>
        """,
        unsafe_allow_html=True
    )

def get_cell_style(row, col, val):
    color = "blue" if val < 0 else "black"
    top = "3px" if row % 3 == 0 else "1px"
    left = "3px" if col % 3 == 0 else "1px"
    bottom = "3px" if row == 8 else "1px"
    right = "3px" if col == 8 else "1px"

    return (
        f'color: {color}; '
        f'border-top: {top} solid black; '
        f'border-left: {left} solid black; '
        f'border-right: {right} solid black; '
        f'border-bottom: {bottom} solid black;'
    )
