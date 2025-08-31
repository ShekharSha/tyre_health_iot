import streamlit as st
from PIL import Image
import numpy as np
import cv2
import datetime
import random
import time
from ultralytics import YOLO

# -------------------------
# Streamlit Page Settings
# -------------------------
st.set_page_config(page_title="Tyre Shield CV Dashboard", layout="wide")
st.title("🚗 Tyre Shield – Vehicle Tyre Protection")

# -------------------------
# Sidebar Controls
# -------------------------
st.sidebar.header("⚙️ Controls")
strength_thresh = st.sidebar.slider("Min Strength (%)", 0, 100, 30)
durability_thresh = st.sidebar.slider("Min Durability (%)", 0, 100, 40)
friction_thresh = st.sidebar.slider("Min Friction (%)", 0, 100, 35)
live_mode = st.sidebar.checkbox("Enable Live Inspection Mode", value=False)

# -------------------------
# Load YOLOv8 Model
# -------------------------
@st.cache_resource
def load_yolo_model():
    return YOLO("yolov8n.pt")  # small and fast model

tyre_model = load_yolo_model()

# -------------------------
# Simulate Tyre Metrics
# -------------------------
def simulate_tyre_metrics():
    return {
        "strength": random.randint(20, 100),
        "rotation": random.randint(1000, 4000),
        "friction": random.randint(20, 100),
        "lifespan": random.randint(10000, 60000),
        "durability": random.randint(20, 100),
        "install_date": datetime.date(
            2024, random.randint(1, 12), random.randint(1, 28)
        ),
    }

# -------------------------
# Analyse Tyre (edge-based)
# -------------------------
def analyse_tyre(img):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    edge_density = np.sum(edges > 0) / edges.size * 100

    if edge_density > 15:
        tread_condition = "⚠️ Worn/Cracked"
        strength = random.randint(20, 50)
        durability = random.randint(20, 50)
    else:
        tread_condition = "✅ Good"
        strength = random.randint(70, 100)
        durability = random.randint(70, 100)

    return edges, tread_condition, strength, durability

# -------------------------
# Tyre Detection Function
# -------------------------
def detect_tyre(image_data):
    img = Image.open(image_data).convert("RGB")
    img_np = np.array(img)

    results = tyre_model.predict(img_np, verbose=False)
    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            label = r.names[cls]
            if label in ["wheel", "car"]:  # COCO classes
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cropped = img_np[y1:y2, x1:x2]
                return True, cropped

    return False, None

# -------------------------
# Main App Logic
# -------------------------
def process_image(camera_image):
    detected, tyre_crop = detect_tyre(camera_image)
    if not detected:
        st.error("⚠️ No tyre detected. Please point the camera at a tyre.")
        return

    st.image(tyre_crop, caption="Detected Tyre Region", use_container_width=True)
    edges, condition, strength_val, durability_val = analyse_tyre(tyre_crop)

    st.subheader("🧪 Tyre Condition Analysis")
    st.image(edges, caption=f"Edge Detection → {condition}", use_container_width=True)
    st.info(f"Tread Condition: {condition}")

    st.subheader("📊 Tyre Health Metrics")
    metrics = simulate_tyre_metrics()
    metrics["strength"] = strength_val
    metrics["durability"] = durability_val

    cols = st.columns(3)
    with cols[0]:
        st.metric("Tyre Strength", f"{metrics['strength']}%")
        st.metric("Friction", f"{metrics['friction']}%")
    with cols[1]:
        st.metric("Rotation", f"{metrics['rotation']} rpm")
        st.metric("Durability", f"{metrics['durability']}%")
    with cols[2]:
        st.metric("Lifespan", f"{metrics['lifespan']} km")
        st.metric("Installed On", str(metrics['install_date']))

    # Alerts
    if metrics["strength"] < strength_thresh:
        st.error(f"⚠️ Strength Low: {metrics['strength']}%")
    if metrics["durability"] < durability_thresh:
        st.warning(f"⚠️ Durability Low: {metrics['durability']}%")
    if metrics["friction"] < friction_thresh:
        st.warning(f"⚠️ Friction Low: {metrics['friction']}%")

# -------------------------
# Live or Manual Mode
# -------------------------
if live_mode:
    st.subheader("📷 Live Tyre Inspection Mode")
    st.info("Camera will capture a new frame every 5 seconds. Disable live mode in the sidebar to exit.")

    camera_placeholder = st.empty()
    result_placeholder = st.empty()

    while live_mode:
        camera_image = camera_placeholder.camera_input("Live Tyre Feed")
        if camera_image is not None:
            with result_placeholder.container():
                process_image(camera_image)
        time.sleep(5)
        st.rerun()
else:
    st.subheader("📷 Capture Tyre Image (Manual Mode)")
    camera_image = st.camera_input("Take a picture of your tyre")
    if camera_image is not None:
        process_image(camera_image)

# -------------------------
# Footer
# -------------------------
st.markdown("---")
st.caption("🔧 Tyre Shield CV Prototype | Streamlit + YOLOv8 | Live & Manual Camera Modes")
