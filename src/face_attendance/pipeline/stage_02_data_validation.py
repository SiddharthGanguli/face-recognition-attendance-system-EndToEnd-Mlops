import logging
from pathlib import Path

from face_attendance.config.configuration import ConfigurationManager
from face_attendance.components.data_validation import DataValidation
from face_attendance.logger import setup_logger


setup_logger("data_validation_pipeline.log")
logger = logging.getLogger(__name__)


class DataValidationPipeline:

    def __init__(self):
        self.config_manager = ConfigurationManager()

    def run(self, source_dir: Path):
        try:
            logger.info("Starting Data Validation Pipeline")

            data_validation_config = self.config_manager.get_data_validation_config()
            validation = DataValidation(
                config=data_validation_config,
                source_dir=source_dir
            )

            validation_artifact = validation.validate()

            logger.info(
                f"Data Validation Pipeline completed successfully. "
                f"Artifact: {validation_artifact}"
            )

            return validation_artifact

        except Exception as e:
            logger.error("Data Validation Pipeline failed", exc_info=True)
            raise e
