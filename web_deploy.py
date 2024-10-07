import cv2
import streamlit as st
from src.face_query import query_face
from src.new_face import new_face

st.title("Automatic Attendance System")

# Initialize session_state variables if they don't exist
if 'user_name' not in st.session_state:
    st.session_state.user_name = ''

if 'register_clicked' not in st.session_state:
    st.session_state.register_clicked = False

if 'authenticate_clicked' not in st.session_state:
    st.session_state.authenticate_clicked = False

# Create two buttons: Register and Authenticate
st.sidebar.title("Options")
if st.sidebar.button("Register"):
    st.session_state.register_clicked = True  # Record that the Register button has been clicked

if st.sidebar.button("Authenticate"):
    st.session_state.authenticate_clicked = True  # Record that the Authenticate button has been clicked

# Variable to control webcam display
show_webcam_flag = False

# Handle logic when the "Register" button is clicked
if st.session_state.register_clicked:
    st.write("Please enter your username to register.")
    st.session_state.user_name = st.text_input("Enter your name:", st.session_state.user_name)

    if st.session_state.user_name:
        st.write(f"Registering user with name: {st.session_state.user_name}")
        show_webcam_flag = True

# Handle logic when the "Authenticate" button is clicked
if st.session_state.authenticate_clicked:
    show_webcam_flag = True

# Function to capture and display video from webcam
def show_webcam():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        st.error("Cannot access the webcam.")
        return

    ret, frame = cap.read()
    if not ret:
        st.error("Cannot read frames from the webcam.")

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    st.image(frame)
    cap.release()
    return frame

# Function to display images during registration
def display_register():
    cap = cv2.VideoCapture(0)  # Open webcam

    if not cap.isOpened():
        st.error("Cannot access the webcam.")
        return

    images = []  # List to store the captured frames

    for i in range(10):  # Capture 10 images from the webcam
        ret, frame = cap.read()  # Read each frame
        if not ret:
            st.error("Cannot read frames from the webcam.")
            break

        # Convert color from BGR to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Store the frame in the list
        images.append(frame_rgb)

    cap.release()  # Close the webcam

    # Display the captured frames in the Streamlit interface
    cols = st.columns(5)  # Split into 5 columns to show 5 images per row

    for i, img in enumerate(images):
        col = cols[i % 5]  # Get the corresponding column
        col.image(img, use_column_width=True)  # Display image in the column

        # After 5 images, create a new row
        if (i + 1) % 5 == 0 and i != 0:
            cols = st.columns(5)
    return images

# Only display the webcam if one of the buttons has been clicked
if show_webcam_flag:
    st.write("Capturing face from camera...")

    if st.session_state.authenticate_clicked:
        name_recog = st.empty()
        img = show_webcam()
        name = query_face(img)
        name_recog.write(f'Successfully recognized: {name}')

    if st.session_state.register_clicked:
        images = display_register()
        success = st.empty()
        new_face(name=st.session_state.user_name, images=images)
        success.write('Register success!!!')
