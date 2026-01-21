import cv2
import logging
from pathlib import Path

from face_attendance.components.face_matching import RealTimeFaceRecognizer
from face_attendance.logger import setup_logger

setup_logger("webcam_recognition.log")
logger = logging.getLogger(__name__)


class WebcamFaceRecognition:
    """
    Webcam interface for real-time face recognition.
    Only handles camera input and visualization.
    """

    def __init__(
        self,
        encodings_path: Path,
        threshold: float = 0.5,
        camera_index: int = 1
    ):
        self.recognizer = RealTimeFaceRecognizer(
            encodings_path=encodings_path,
            threshold=threshold
        )
        self.camera_index = camera_index

    def start(self):
        logger.info("Starting webcam face recognition")

        cap = cv2.VideoCapture(self.camera_index)

        if not cap.isOpened():
            logger.error("Unable to access webcam")
            raise RuntimeError("Webcam not accessible")

        logger.info("Webcam accessed successfully")

        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    logger.warning("Failed to read frame from webcam")
                    break

                name, distance = self.recognizer.identify(frame)

                label = name
                if distance is not None:
                    label = f"{name} ({distance:.2f})"

                # Draw label on frame
                cv2.putText(
                    frame,
                    label,
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )

                cv2.imshow("Face Recognition", frame)

                # Press 'q' to exit
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    logger.info("Exit key pressed")
                    break

        finally:
            cap.release()
            cv2.destroyAllWindows()
            logger.info("Webcam released and windows closed")
