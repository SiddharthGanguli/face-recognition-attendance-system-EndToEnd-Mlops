from dataclasses import dataclass
from pathlib import Path
from typing import List

@dataclass
class DataIngestionConfig:
    ROOT_DIR: Path
    SOURCE_DIR: Path

@dataclass
class DataValidationConfig:
    ROOT_DIR: Path
    allowed_extensions: List[str]
    min_images_per_class: int


@dataclass
class FaceEncodingConfig:
    ROOT_DIR: Path
    model_name: str
    image_size: tuple
    encoding_file: str