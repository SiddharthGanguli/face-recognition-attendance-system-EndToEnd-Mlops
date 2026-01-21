from pathlib import Path
import logging

from face_attendance.pipeline.stage_01_data_ingestion import DataIngestionPipeline
from face_attendance.pipeline.stage_02_data_validation import DataValidationPipeline
from face_attendance.pipeline.stage_03_face_encoding import FaceEncodingPipeline
from face_attendance.logger import setup_logger


setup_logger("main.log")
logger = logging.getLogger(__name__)


def main():
    try:
        logger.info("Starting Face Attendance ML Pipeline")

        ingestion_pipeline = DataIngestionPipeline()
        ingestion_pipeline.run()

        validation_pipeline = DataValidationPipeline()
        validation_pipeline.run(source_dir=Path("data/dataset"))

        encoding_pipeline = FaceEncodingPipeline()
        encoding_pipeline.run(source_dir=Path("data/dataset"))

        logger.info("Pipeline completed successfully")

    except Exception:
        logger.error("Pipeline failed", exc_info=True)
        raise


if __name__ == "__main__":
    main()
