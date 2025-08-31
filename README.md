# 🚗 Tyre Shield – CV-based Tyre Health Monitoring

Tyre Shield is a **Computer Vision (CV) + Streamlit** project that helps monitor the health of vehicle tyres using a camera feed.  
It detects tyres using **YOLOv8** and estimates key parameters such as:

- ✅ Tyre Strength  
- ✅ Rotation Condition  
- ✅ Friction Estimation  
- ✅ Life Span Prediction  
- ✅ Durability Score  
- ✅ Installation Date  

⚡ Works with **webcam / mobile camera** input (via browser access) and shows results in a **Streamlit dashboard**.

---

## 📸 Demo (Prototype UI)

- Detects **tyres/wheels** in the image.  
- If no tyre is detected → shows a warning.  
- Displays tyre metrics in real time.  

---

## 🛠️ Tech Stack

- [Streamlit](https://streamlit.io/) – for interactive dashboard  
- [YOLOv8 (Ultralytics)](https://github.com/ultralytics/ultralytics) – tyre/wheel detection  
- [OpenCV](https://opencv.org/) – image processing (edges, shapes, etc.)  
- [Pillow](https://pillow.readthedocs.io/) – image handling  
- [NumPy](https://numpy.org/) – numerical analysis  

---

## 📦 Installation

Clone the repo:

```bash
git clone https://github.com/ShekharSha/tyre_health_iot.git
cd tyre_health_iot
