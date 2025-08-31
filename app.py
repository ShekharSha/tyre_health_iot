import streamlit as st
import datetime
import random
import numpy as np
import cv2
from PIL import Image
import time

# -------------------------
# Streamlit Page Settings
# -------------------------
st.set_page_config(page_title="Tyre Protection Dashboard", layout="wide")
st.title("🚗 Vehicle Tyre Protection Dashboard")

# -------------------------
# Sidebar for Controls
# -------------------------
st.sidebar.header("⚙️ Controls")
strength_thresh = st.sidebar.slider("Min Strength (%)", 0, 100, 30)
durability_thresh = st.sidebar.slider("Min Durability (%)", 0, 100, 40)
friction_thresh = st.sidebar.slider("Min Friction (%)", 0, 100, 35)

live_mode = st.sidebar.checkbox("Enable Live Inspection Mode", value=False)

# -------------------------
# Simulated Tyre Data Generator
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
# Tyre Image Analysis (basic CV prototype)
# -------------------------
def analyse_tyre(image_data):
    img = Image.open(image_data)
    img = np.array(img.convert("RGB"))

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
# Live Mode
# -------------------------
if live_mode:
    st.subheader("📷 Live Tyre Inspection Mode")
    st.info("Camera will capture a new frame every 5 seconds. Disable Live Mode in the sidebar to exit.")

    camera_placeholder = st.empty()
    result_placeholder = st.empty()

    while live_mode:
        camera_image = camera_placeholder.camera_input("Live Tyre Feed")

        if camera_image is not None:
            edges, condition, strength_val, durability_val = analyse_tyre(camera_image)

            with result_placeholder.container():
                st.image(camera_image, caption="Live Tyre Frame", use_container_width=True)
                st.image(edges, caption=f"Edge Detection → {condition}", use_container_width=True)
                st.metric("Strength", f"{strength_val}%")
                st.metric("Durability", f"{durability_val}%")
                st.info(f"Tread Condition: {condition}")

        time.sleep(5)  # wait 5s
        st.rerun()     # 🔄 modern API for rerun

# -------------------------
# Manual Mode
# -------------------------
else:
    st.subheader("📷 Capture Tyre Image (Manual Mode)")
    camera_image = st.camera_input("Take a picture of your tyre")

    if camera_image is not None:
        st.success("✅ Tyre image captured!")
        st.image(camera_image, caption="Captured Tyre", use_container_width=True)

        edges, condition, strength_val, durability_val = analyse_tyre(camera_image)

        st.subheader("🧪 Tyre Condition Analysis")
        st.image(edges, caption=f"Edge Detection Result → {condition}", use_container_width=True)
        st.info(f"Tread Condition: {condition}")

        st.subheader("📊 Tyre Health Metrics (AI-assisted)")
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
# Footer
# -------------------------
st.markdown("---")
st.caption("🔧 Tyre Shield CV Prototype | Streamlit + OpenCV | Live & Manual Camera Modes")
