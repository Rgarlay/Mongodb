from dataclasses import dataclass

@dataclass

class DataIngestionArtifact:
    train_file_path: str
    test_file_path : str


@dataclass
class DataValidationArtifact:
    validation_status: bool
    valid_train_file_path: str
    valid_test_file_path: str
    invalid_train_file_path: str
    invalid_test_file_path: str
    drift_report_file_path: str


@dataclass
class DataTransformationArtifact:
    transformed_obj_file_path: str
    train_obj_file_path: str
    test_obj_file_path: str


@dataclass
class ClassificationMetricArtifact:
    r2_score: float
    root_mean_squared_error: float
    mean_absolute_error: float


@dataclass
class ModelTrainerArtifact:
    trained_model_file_path: str
    train_metric_artifact: ClassificationMetricArtifact
    test_metric_artifact: ClassificationMetricArtifact
    