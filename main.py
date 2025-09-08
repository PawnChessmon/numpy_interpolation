# main.py
import streamlit as st
import pandas as pd
import numpy as np

# ---------------------------
# Function: Interpolate Data
# ---------------------------
def iterative_interpolation(df):
    """
    Interpolates missing values (NaN) using the average of non-diagonal neighbors.
    """
    df = df.copy()
    rows, cols = df.shape
    for i in range(rows):
        for j in range(cols):
            if pd.isna(df.iat[i, j]):
                # Collect neighbors (up, down, left, right)
                neighbors = []
                if i > 0 and not pd.isna(df.iat[i-1, j]):
                    neighbors.append(df.iat[i-1, j])
                if i < rows-1 and not pd.isna(df.iat[i+1, j]):
                    neighbors.append(df.iat[i+1, j])
                if j > 0 and not pd.isna(df.iat[i, j-1]):
                    neighbors.append(df.iat[i, j-1])
                if j < cols-1 and not pd.isna(df.iat[i, j+1]):
                    neighbors.append(df.iat[i, j+1])
                if neighbors:
                    df.iat[i, j] = np.mean(neighbors)
    return df

# ---------------------------
# Streamlit App Layout
# ---------------------------
st.title("CSV Interpolation App")
st.write("Upload a CSV file, interpolate missing values, preview results, and download.")

# ---------------------------
# File Upload
# ---------------------------
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file:
    # Read CSV exactly as it is (no headers)
    df_input = pd.read_csv(uploaded_file, header=None)
    st.subheader("Original Data")
    st.dataframe(df_input)

    if st.button("Interpolate Missing Values"):
        df_result = iterative_interpolation(df_input)
        st.subheader("Interpolated Data")
        st.dataframe(df_result)

        csv = df_result.to_csv(index=False, header=False).encode('utf-8')
        st.download_button(
            label="Download Interpolated CSV",
            data=csv,
            file_name="interpolated_results.csv",
            mime="text/csv"
        )
