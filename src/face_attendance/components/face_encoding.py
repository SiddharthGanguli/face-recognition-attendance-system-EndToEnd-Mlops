import pickle
import logging
from pathlib import Path

import cv2
import face_recognition

from face_attendance.entity.config_entity import FaceEncodingConfig
from face_attendance.logger import setup_logger


setup_logger("face_encoding.log")
logger = logging.getLogger(__name__)


class FaceEncoding:


    def __init__(self, config: FaceEncodingConfig, source_dir: Path):
        self.config = config
        self.source_dir = source_dir

    def _preprocess_image(self, image_path: Path):

        image = cv2.imread(str(image_path))
        if image is None:
            logger.warning(f"Failed to read image: {image_path}")
            return None

        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return rgb_image

    def encode(self):
        logger.info("Starting face encoding process...")

        if not self.source_dir.exists():
            raise FileNotFoundError(
                f"Source directory not found: {self.source_dir}"
            )

        encodings = {}

        for class_dir in self.source_dir.iterdir():
            if not class_dir.is_dir():
                continue

            person_name = class_dir.name
            encodings[person_name] = []

            logger.info(f"Processing class: {person_name}")

            for image_path in class_dir.iterdir():
                if image_path.suffix.lower() not in [".jpg", ".jpeg", ".png"]:
                    continue

                rgb_image = self._preprocess_image(image_path)
                if rgb_image is None:
                    continue

                face_locations = face_recognition.face_locations(rgb_image)

                if len(face_locations) == 0:
                    logger.warning(
                        f"No face detected inyour image: {image_path}"
                    )
                    continue

                if len(face_locations) > 1:
                    logger.warning(
                        f"Multiple faces detected, skipping image: {image_path}"
                    )
                    continue

                face_encodings = face_recognition.face_encodings(
                    rgb_image, face_locations
                )

                if not face_encodings:
                    logger.warning(
                        f"Failed to encode face in image: {image_path}"
                    )
                    continue

                encodings[person_name].append(face_encodings[0])

            if len(encodings[person_name]) == 0:
                logger.warning(
                    f"No valid encodings found for class: {person_name}"
                )
            else:
                logger.info(
                    f"Encoded {len(encodings[person_name])} faces for class '{person_name}'"
                )

        if not encodings:
            raise ValueError("No face encodings generated. Check dataset quality.")

        encoding_path = self.config.ROOT_DIR / self.config.encoding_file
        encoding_path.parent.mkdir(parents=True, exist_ok=True)

        with open(encoding_path, "wb") as f:
            pickle.dump(encodings, f)

        logger.info(f"Face encodings saved at: {encoding_path}")
        logger.info("Face encoding process completed successfully")

        return encoding_path
