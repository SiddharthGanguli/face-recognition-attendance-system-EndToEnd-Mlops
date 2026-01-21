from pathlib import Path
import yaml

from face_attendance.entity.config_entity import (
    DataIngestionConfig,
    DataValidationConfig,
    FaceEncodingConfig
)


class ConfigurationManager:
    def __init__(self, config_filepath: Path = Path("config/config.yaml")):
        self.config = self._read_yaml(config_filepath)
        self.artifacts_root = Path(self.config["artifacts_root"])
        self.artifacts_root.mkdir(parents=True, exist_ok=True)

    def _read_yaml(self, path: Path) -> dict:
        with open(path, "r") as file:
            return yaml.safe_load(file)

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config["data_ingestion"]

        root_dir = Path(config["ROOT_DIR"])
        source_dir = Path(config["SOURCE_DIR"])

        root_dir.mkdir(parents=True, exist_ok=True)

        return DataIngestionConfig(
            ROOT_DIR=root_dir,
            SOURCE_DIR=source_dir
        )

    def get_data_validation_config(self) -> DataValidationConfig:
        config = self.config["data_validation"]

        root_dir = Path(config["ROOT_DIR"])
        root_dir.mkdir(parents=True, exist_ok=True)

        return DataValidationConfig(
            ROOT_DIR=root_dir,
            allowed_extensions=config["allowed_extensions"],
            min_images_per_class=config["min_images_per_class"]
        )

    def get_face_encoding_config(self) -> FaceEncodingConfig:
        config = self.config["face_encoding"]
        root_dir = Path(config["ROOT_DIR"])
        root_dir.mkdir(parents=True, exist_ok=True)

        return FaceEncodingConfig(
            ROOT_DIR=root_dir,
            model_name=config["model_name"],
            image_size=tuple(config["image_size"]),
            encoding_file=config["encoding_file"]
        )