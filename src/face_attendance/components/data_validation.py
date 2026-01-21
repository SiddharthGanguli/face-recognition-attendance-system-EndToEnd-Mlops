import json
import logging
from pathlib import Path

import cv2

from face_attendance.entity.config_entity import DataValidationConfig
from face_attendance.logger import setup_logger


setup_logger("data_validation.log")
logger = logging.getLogger(__name__)


class DataValidation:

    def __init__(self, config: DataValidationConfig, source_dir: Path):
        self.config = config
        self.source_dir = source_dir

    def validate(self):
        logger.info("Starting data validation...")

        validation_report = {
            "status": "passed",
            "class_summary": {},
            "errors": []
        }

        if not self.source_dir.exists():
            raise FileNotFoundError(
                f"Source  not found: {self.source_dir}"
            )

        for class_dir in self.source_dir.iterdir():
            if not class_dir.is_dir():
                continue

            class_name = class_dir.name
            valid_images = 0

            for file in class_dir.iterdir():
                if file.suffix.lower() not in self.config.allowed_extensions:
                    continue

                image = cv2.imread(str(file))
                if image is None:
                    validation_report["errors"].append(
                        f" image: {file}"
                    )
                    validation_report["status"] = "failed"
                    continue

                valid_images += 1

            validation_report["class_summary"][class_name] = valid_images

            if valid_images < self.config.min_images_per_class:
                validation_report["errors"].append(
                    f"Class '{class_name}' has insufficient images: {valid_images}"
                )
                validation_report["status"] = "failed"

        report_path = Path(self.config.ROOT_DIR) / "validation_report.json"

        with open(report_path, "w") as file:
            json.dump(validation_report, file, indent=4)

        logger.info(f"Validation report saved at: {report_path}")

        if validation_report["status"] == "failed":
            logger.error("Data validation failed")
            raise ValueError("Data validation failed. Check yourr report.")

        logger.info("Data validation completed successfully..")
        return report_path
