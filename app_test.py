import streamlit as st

from components import upload_image

img_file_buffer = st.camera_input("Take a picture")

if img_file_buffer is not None:
    url = upload_image(img_file_buffer)
    st.image(url, use_column_width=True)
