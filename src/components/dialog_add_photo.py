import streamlit as st
from PIL import Image


@st.dialog("Add Classroom Photos")
def add_photos_dialog():
    st.write("Upload or take classroom photos to run AI facial attendance.")

    tab1, tab2 = st.tabs(["Upload Photos", "Use Camera"])

    with tab1:
        uploaded_files = st.file_uploader(
            "Choose photos",
            type=["png", "jpg", "jpeg"],
            accept_multiple_files=True,
            key="photo_upload_input",
        )
        if st.button("Add Uploaded Photos", type="primary", use_container_width=True):
            if uploaded_files:
                if "attendance_images" not in st.session_state:
                    st.session_state.attendance_images = []
                for f in uploaded_files:
                    st.session_state.attendance_images.append(Image.open(f))
                st.success(f"Added {len(uploaded_files)} photos!")
                st.rerun()
            else:
                st.warning("Please select at least one photo.")

    with tab2:
        captured = st.camera_input("Capture classroom picture")
        if captured and st.button("Add Captured Photo", type="primary", use_container_width=True):
            if "attendance_images" not in st.session_state:
                st.session_state.attendance_images = []
            st.session_state.attendance_images.append(Image.open(captured))
            st.success("Photo added!")
            st.rerun()
