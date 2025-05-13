import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

# Load DNN Model
dnn_model = cv2.dnn.readNetFromCaffe(
    'deploy.prototxt',
    'res10_300x300_ssd_iter_140000.caffemodel'
)

# Streamlit App
st.set_page_config(page_title="Face Detection App", layout="wide")
st.title("🤖 Face Detection App")

# Theme switcher
theme = st.sidebar.radio("🎨 Choose Theme", ["Light", "Dark"])
if theme == "Dark":
    st.markdown("<style>body{background-color:#111;color:white;}</style>", unsafe_allow_html=True)

# Sidebar options
st.sidebar.markdown("### ⚙️ Settings")
image_source = st.sidebar.radio("Select Image Source", ["Upload Image", "Use Webcam"])
grayscale = st.sidebar.checkbox("Convert to Grayscale")
blur_faces = st.sidebar.checkbox("Blur Detected Faces")
show_cropped_faces = st.sidebar.checkbox("Show Cropped Faces")

# Image uploader
img = None
if image_source == "Upload Image":
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, 1)
else:
    run_webcam = st.checkbox("Start Webcam")
    FRAME_WINDOW = st.image([])
    camera = cv2.VideoCapture(0)
    while run_webcam:
        success, img = camera.read()
        if not success:
            st.warning("Webcam not working.")
            break

        # Face Detection Logic (inside webcam loop)
        h, w = img.shape[:2]
        blob = cv2.dnn.blobFromImage(img, 1.0, (300, 300), (104, 117, 123))
        dnn_model.setInput(blob)
        detections = dnn_model.forward()

        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (x1, y1, x2, y2) = box.astype("int")
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                label = f"{confidence*100:.1f}%"
                cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        FRAME_WINDOW.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    camera.release()

# If static image
if img is not None:
    st.subheader("📸 Original Image")
    st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), use_column_width=True)

    h, w = img.shape[:2]
    blob = cv2.dnn.blobFromImage(img, 1.0, (300, 300), (104, 117, 123))
    dnn_model.setInput(blob)
    detections = dnn_model.forward()

    cropped_faces = []
    high_conf_count = 0

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:
            if confidence > 0.8:
                high_conf_count += 1

            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (x1, y1, x2, y2) = box.astype("int")

            face_roi = img[y1:y2, x1:x2]
            if blur_faces:
                face_roi = cv2.GaussianBlur(face_roi, (99, 99), 30)
            img[y1:y2, x1:x2] = face_roi

            if show_cropped_faces:
                cropped_faces.append(face_roi)

            text = f"{confidence*100:.1f}%"
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

    # Optional grayscale
    if grayscale:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    st.subheader("🧠 Processed Image with Detections")
    st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), use_column_width=True)

    st.info(f"✅ Total Faces: {detections.shape[2]} | High Confidence Faces (>80%): {high_conf_count}")

    # Save Button
    save_btn = st.button("💾 Download Processed Image")
    if save_btn:
        is_success, buffer = cv2.imencode(".jpg", img)
        st.download_button(
            label="Download as JPG",
            data=buffer.tobytes(),
            file_name="processed_face.jpg",
            mime="image/jpeg"
        )

    # Show cropped faces
    if show_cropped_faces and cropped_faces:
        st.subheader("📦 Cropped Faces")
        for i, face in enumerate(cropped_faces):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.image(cv2.cvtColor(face, cv2.COLOR_BGR2RGB), width=200)
            with col2:
                is_success, buffer = cv2.imencode(".jpg", face)
                st.download_button(
                    label=f"⬇️ Download Face {i+1}",
                    data=buffer.tobytes(),
                    file_name=f"face_{i+1}.jpg",
                    mime="image/jpeg"
                )
else:
    if image_source == "Upload Image":
        st.warning("👆 Please upload an image to begin.")
