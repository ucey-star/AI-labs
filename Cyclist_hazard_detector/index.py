import cv2
import time
import pyttsx3
from ultralytics import YOLO
import numpy as np
from deep_sort_realtime.deepsort_tracker import DeepSort

# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak_alert(message):
    engine.say(message)
    engine.runAndWait()

# Global dictionary of known object heights in meters
KNOWN_HEIGHTS = {
    "person": 1.7,  # average human height in meters
    "car": 1.5      # approximate height of a car in meters
}

def estimate_distance(box, frame_height, class_name, focal_length=800):
    """
    Estimate distance using the pinhole camera model if a known object height is available.
    For a known object, distance (in meters) is computed as:
        distance = (known_height * focal_length) / box_height_pixels
    If the object class is not known, falls back to a simple inverse relation.
    """
    x1, y1, x2, y2 = box
    box_height = y2 - y1
    if box_height <= 0:
        return float("inf")
    
    if class_name in KNOWN_HEIGHTS:
        known_height = KNOWN_HEIGHTS[class_name]
        distance = (known_height * focal_length) / box_height
    else:
        distance = frame_height / (box_height + 1e-6)
    return distance

def estimate_speed(current_center, previous_center, dt):
    """
    Estimate speed as the Euclidean distance moved per time unit.
    """
    if previous_center is None:
        return 0.0
    dx = current_center[0] - previous_center[0]
    dy = current_center[1] - previous_center[1]
    speed = np.sqrt(dx**2 + dy**2) / dt
    return speed

def is_in_lane(box, frame_width, frame_height):
    """
    For simplicity, assume the "lane" is the bottom half of the frame.
    Return True if the center of the box is in the bottom half.
    """
    x1, y1, x2, y2 = box
    center_y = (y1 + y2) / 2
    return center_y > frame_height / 2

def main():
    # 1. Load the YOLOv8 model
    model = YOLO('yolov8n.pt')  # Pre-trained lightweight model

    # 2. Initialize video capture (0 = default webcam)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return

    # Initialize DeepSORT tracker for persistent tracking
    tracker = DeepSort(max_age=30, n_init=3, nms_max_overlap=1.0)

    # For FPS calculation
    prev_time = time.time()
    fps = 0
    frame_count = 0

    # For tracking speed, store previous centers per track id
    previous_centers = {}

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        frame_height, frame_width = frame.shape[:2]
        current_time = time.time()
        dt = current_time - prev_time if current_time - prev_time > 0 else 1.0

        # 3. Perform object detection on the frame using YOLO
        results = model(frame)
        
        # Prepare detections for DeepSORT:
        # Each detection format: [x1, y1, x2, y2, confidence, class_id]
        detections = []
        for box in results[0].boxes:
            coords = box.xyxy[0].cpu().numpy().tolist()  # [x1, y1, x2, y2]
            conf = float(box.conf[0])
            class_id = int(box.cls[0])
            detections.append([coords, conf, class_id])

        
        # 4. Update tracker with the current detections; this returns persistent tracks.
        tracks = tracker.update_tracks(detections, frame=frame)
        
        # 5. Start with base YOLO annotations
        annotated_frame = results[0].plot()

        # Process each track
        for track in tracks:
            if not track.is_confirmed():
                continue  # Only process confirmed tracks

            track_id = track.track_id
            bbox = track.to_ltrb()  # Bounding box in [x1, y1, x2, y2]
            x1, y1, x2, y2 = map(int, bbox)
            # Use detection's class if available
            class_id = track.det_class if hasattr(track, "det_class") else None
            class_name = results[0].names[class_id] if class_id is not None and class_id in results[0].names else "object"

            # Estimate distance using our function
            distance = estimate_distance((x1, y1, x2, y2), frame_height, class_name)
            # Compute center of the box
            center = ((x1 + x2) // 2, (y1 + y2) // 2)
            prev_center = previous_centers.get(track_id, None)
            speed = estimate_speed(center, prev_center, dt)
            previous_centers[track_id] = center

            in_lane = is_in_lane((x1, y1, x2, y2), frame_width, frame_height)
            risk = (distance < 100) and (speed > 50) and in_lane

            # Draw bounding box and tracking information
            label = f"ID:{track_id} {class_name}"
            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (255, 255, 0), 2)
            cv2.putText(annotated_frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
            
            if risk:
                cv2.putText(annotated_frame, "HIGH RISK!", (x1, y1 - 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                print(f"[ALERT] High risk: {class_name} (ID:{track_id}) detected! Distance: {distance:.2f}, Speed: {speed:.2f}")
                # Uncomment to enable audio alert
                speak_alert("Warning! High risk ahead!")
            else:
                if class_name in ["person", "car"]:
                    print(f"Alert: {class_name} detected (ID:{track_id})")

            cv2.circle(annotated_frame, center, 4, (0, 255, 0), -1)

        # 6. FPS Calculation and display
        frame_count += 1
        if current_time - prev_time >= 1.0:
            fps = frame_count / (current_time - prev_time)
            prev_time = current_time
            frame_count = 0
        cv2.putText(annotated_frame, f"FPS: {fps:.2f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

        # 7. Display the annotated frame
        cv2.imshow("Object Detection & Tracking", annotated_frame)

        # 8. Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
