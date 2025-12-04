import streamlit as st

st.title("Image Tuner Application")

Input,Output = st.columns([1,1])

with Input:
    st.header("Input Parameters")
    image_type = st.selectbox("Select Image Type", ["grayscale", "binary", "color"])
    width = st.number_input("Width", min_value=1, value=430)
    height = st.number_input("Height", min_value=1, value=860)
    process_button = st.button("Process Image")

with Output:
    st.header("Output")