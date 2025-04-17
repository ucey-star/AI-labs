# 🚴‍♂️ Object Detection & Risk Assessment for Cyclists

This project is a real-time AI safety system for cyclists that detects and tracks vehicles and pedestrians, estimates their speed and distance, and raises audio alerts if there's a high risk of collision. It acts as a virtual co-pilot, helping cyclists stay safe in urban environments.

---

## 🔧 Features

- **Real-Time Object Detection** using YOLOv8
- **Object Tracking** with DeepSORT
- **Distance Estimation** using the pinhole camera model
- **Speed Calculation** between frames
- **Lane Detection** to identify objects within the cyclist’s path
- **Risk Alerts** (visual and audio) when a fast-moving object gets too close
- **Text-to-Speech Alerts** via `pyttsx3`
- **Webcam Live Feed Visualization**

---

## 🧠 How It Works

1. **YOLOv8** detects objects (e.g., people, cars) in each video frame.
2. **DeepSORT** assigns persistent track IDs to detected objects.
3. For each tracked object:
   - **Distance** is estimated using its bounding box size and known object height.
   - **Speed** is calculated from the movement between frames.
   - The system checks if the object is **in the cyclist's lane**.
4. If the object is:
   - **Too close**,  
   - **Moving fast**,  
   - And **in the lane**,  
   → a **high-risk alert** is triggered.

---

## 🖥️ Requirements

Install dependencies using pip:

```bash
pip install opencv-python ultralytics numpy pyttsx3 deep_sort_realtime
```

---

## 📁 File Structure

```
.
├── main.py                 # Main script for real-time detection and alerting
└── yolov8n.pt              # Pretrained YOLOv8n weights (downloaded automatically or place manually)
```

---

## ▶️ Running the Project

Make sure your webcam is connected. Then run:

```bash
python main.py
```

Press **`q`** to quit the app at any time.

---

## 🧪 Detection Logic

- **Distance Calculation**:
  ```
  distance = (known_height * focal_length) / bounding_box_height
  ```
- **Speed Calculation**:
  ```
  speed = Euclidean distance / time
  ```
- **High Risk Criteria**:
  - Distance < 100 pixels
  - Speed > 50 pixels/sec
  - Object is in the lower half (cyclist's lane)

---

## 🔊 Audio Alerts

Text-to-speech warnings are spoken when a high-risk object is detected. You can disable the audio alert by commenting out the `speak_alert()` line in the code.

---

## 📸 Sample Output

- Bounding boxes with ID and class name
- "HIGH RISK!" text shown in red if danger is detected
- Real-time FPS display

---

## 🛠️ Future Improvements

- Add GPS & orientation data for outdoor cycling
- Use a more precise focal length from real camera calibration
- Add helmet-mounted or mobile support

---

## 📄 License

This project is for educational and personal research use. Attribution appreciated.

---