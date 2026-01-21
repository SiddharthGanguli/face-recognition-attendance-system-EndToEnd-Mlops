from pathlib import Path
from face_attendance.components.webcam_recognition import WebcamFaceRecognition

app = WebcamFaceRecognition(
    encodings_path=Path("artifacts/face_encoding/encodings.pkl"),
    threshold=0.5
)

app.start()
