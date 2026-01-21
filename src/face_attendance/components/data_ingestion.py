import os
import json
import logging
from pathlib import Path

from face_attendance.entity.config_entity import DataIngestionConfig
from face_attendance.logger import setup_logger


setup_logger("data_ingestion.log")
logger = logging.getLogger(__name__)


class DataIngestion:

    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def ingestion(self):
        logger.info("Starting data ingestion")

        if not self.config.SOURCE_DIR.exists():
            logger.error(
                f"Source data not found: {self.config.SOURCE_DIR}"
            )
            raise FileNotFoundError(
                f"Source data not found: {self.config.SOURCE_DIR}"
            )

        logger.info(
            f"Source data directory found: {self.config.SOURCE_DIR}"
        )

        os.makedirs(self.config.ROOT_DIR, exist_ok=True)
        logger.info(
            f"Created ingestion artifact directory: {self.config.ROOT_DIR}"
        )

        ingestion_report = {
            "source_dir": str(self.config.SOURCE_DIR),
            "status": "ingestion_completed"
        }

        report_path = Path(self.config.ROOT_DIR) / "ingestion_report.json"

        with open(report_path, "w") as file:
            json.dump(ingestion_report, file, indent=4)

        logger.info(
            f"Ingestion report saved at: {report_path}"
        )

        logger.info("Data ingestion completed successfully")
        return report_path
