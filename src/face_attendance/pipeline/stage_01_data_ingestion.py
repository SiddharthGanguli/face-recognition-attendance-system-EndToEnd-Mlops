import logging

from face_attendance.config.configuration import ConfigurationManager
from face_attendance.components.data_ingestion import DataIngestion
from face_attendance.logger import setup_logger


setup_logger("data_ingestion_pipeline.log")
logger = logging.getLogger(__name__)


class DataIngestionPipeline:

    def __init__(self):
        self.config_manager = ConfigurationManager()

    def run(self):
        try:
            logger.info("Starting Data Ingestion Pipeline")

            data_ingestion_config = self.config_manager.get_data_ingestion_config()
            ingestion = DataIngestion(data_ingestion_config)

            ingestion_artifact = ingestion.ingestion()

            logger.info(
                f"Data Ingestion Pipeline completed successfully. "
                f"Artifact: {ingestion_artifact}"
            )

            return ingestion_artifact

        except Exception as e:
            logger.error("Data Ingestion Pipeline failed", exc_info=True)
            raise e
