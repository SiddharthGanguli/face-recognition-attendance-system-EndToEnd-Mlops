import cv2
from pathlib import Path
from face_attendance.components.face_matching import RealTimeFaceRecognizer

recognizer = RealTimeFaceRecognizer(
    encodings_path=Path("artifacts/face_encoding/encodings.pkl"),
    threshold=0.5
)

img = cv2.imread("data/dataset/akash/akash01.jpeg")
name, distance = recognizer.identify(img)

print(name, distance)
