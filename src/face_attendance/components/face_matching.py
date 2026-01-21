import pickle
import logging
from pathlib import Path
from typing import Tuple, Optional

import cv2
import face_recognition
import numpy as np

from face_attendance.logger import setup_logger

setup_logger("real_time_recognizer.log")
logger = logging.getLogger(__name__)


class RealTimeFaceRecognizer:

    def __init__(
        self,
        encodings_path: Path,
        threshold: float = 0.5
    ):
        self.encodings_path = encodings_path
        self.threshold = threshold
        self.known_encodings = self._load_encodings()

    def _load_encodings(self) -> dict:
        if not self.encodings_path.exists():
            raise FileNotFoundError(
                f"Encodings file not found: {self.encodings_path}"
            )

        with open(self.encodings_path, "rb") as f:
            encodings = pickle.load(f)

        logger.info("Face encodings loaded successfully....")
        return encodings

    def identify(self, image) -> Tuple[str, Optional[float]]:
 
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_image)

        if len(face_locations) == 0:
            logger.debug("No face detected...Sorry ")
            return "Unknown", None

        if len(face_locations) > 1:
            logger.debug("!!!...Multiple faces detected")
            return "Unknown", None

        face_encoding = face_recognition.face_encodings(
            rgb_image, face_locations
        )[0]

        best_match = "Unknown"
        best_distance = float("inf")

        for person_name, enc_list in self.known_encodings.items():
            for known_enc in enc_list:
                distance = np.linalg.norm(known_enc - face_encoding)

                if distance < best_distance:
                    best_distance = distance
                    best_match = person_name

        if best_distance < self.threshold:
            logger.info(
                f"Recognized {best_match} (distance={best_distance:.3f})"
            )
            return best_match, best_distance

        logger.info(
            f"Face not recognized (min distance={best_distance:.3f}..)"
        )
        return "Unknown", None
