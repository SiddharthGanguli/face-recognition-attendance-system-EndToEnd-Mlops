import logging
from pathlib import Path

from face_attendance.config.configuration import ConfigurationManager
from face_attendance.components.face_encoding import FaceEncoding
from face_attendance.logger import setup_logger


setup_logger("face_encoding_pipeline.log")
logger = logging.getLogger(__name__)


class FaceEncodingPipeline:

    def __init__(self):
        self.config_manager = ConfigurationManager()

    def run(self, source_dir: Path):
        try:
            logger.info("Starting Face Encoding Pipeline")

            encoding_config = self.config_manager.get_face_encoding_config()
            encoder = FaceEncoding(
                config=encoding_config,
                source_dir=source_dir
            )

            encoding_artifact = encoder.encode()

            logger.info(
                f"Face Encoding Pipeline completed successfully. "
                f"Artifact: {encoding_artifact}"
            )

            return encoding_artifact

        except Exception as e:
            logger.error("Face Encoding Pipeline failed", exc_info=True)
            raise e
