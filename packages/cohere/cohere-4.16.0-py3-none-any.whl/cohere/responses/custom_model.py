from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional

try:
    from typing import Literal, TypedDict
except ImportError:
    from typing_extensions import Literal, TypedDict

from cohere.responses.base import CohereObject

CUSTOM_MODEL_STATUS = Literal[
    "UNKNOWN",
    "CREATED",
    "DATA_PROCESSING",
    "FINETUNING",
    "EXPORTING_MODEL",
    "DEPLOYING_API",
    "READY",
    "FAILED",
    "DELETED",
    "DELETE_FAILED",
    "CANCELLED",
    "TEMPORARILY_OFFLINE",
    "PAUSED",
    "QUEUED",
]

INTERNAL_CUSTOM_MODEL_TYPE = Literal["GENERATIVE", "CLASSIFICATION", "RERANK"]
CUSTOM_MODEL_TYPE = Literal["GENERATIVE", "CLASSIFY", "RERANK"]
CUSTOM_MODEL_PRODUCT_MAPPING: Dict[CUSTOM_MODEL_TYPE, INTERNAL_CUSTOM_MODEL_TYPE] = {
    "GENERATIVE": "GENERATIVE",
    "CLASSIFY": "CLASSIFICATION",
    "RERANK": "RERANK",
}
REVERSE_CUSTOM_MODEL_PRODUCT_MAPPING: Dict[INTERNAL_CUSTOM_MODEL_TYPE, CUSTOM_MODEL_TYPE] = {
    v: k for k, v in CUSTOM_MODEL_PRODUCT_MAPPING.items()
}


@dataclass
class HyperParameters:
    early_stopping_patience: int
    early_stopping_threshold: float
    train_batch_size: int
    train_steps: int
    learning_rate: float

    @staticmethod
    def from_response(response: Optional[dict]) -> "HyperParameters":
        return HyperParameters(
            early_stopping_patience=response["earlyStoppingPatience"],
            early_stopping_threshold=response["earlyStoppingThreshold"],
            train_batch_size=response["trainBatchSize"],
            train_steps=response["trainSteps"],
            learning_rate=response["learningRate"],
        )


class HyperParametersInput(TypedDict):
    """
    early_stopping_patience: int (default=6, min=0, max=10)
    early_stopping_threshold: float (default=0.01, min=0, max=0.1)
    train_batch_size: int (default=16, min=2, max=16)
    train_steps: int (default=2500, min=100, max=20000)
    learning_rate: float (default=0.01, min=0.000005, max=0.1)
    """

    early_stopping_patience: int
    early_stopping_threshold: float
    train_batch_size: int
    train_steps: int
    learning_rate: float


class CustomModel(CohereObject):
    def __init__(
        self,
        id: str,
        name: str,
        status: CUSTOM_MODEL_STATUS,
        model_type: CUSTOM_MODEL_TYPE,
        created_at: datetime,
        completed_at: Optional[datetime],
        model_id: Optional[str] = None,
        hyperparameters: Optional[HyperParameters] = None,
    ) -> None:
        super().__init__()
        self.id = id
        self.name = name
        self.status = status
        self.model_type = model_type
        self.created_at = created_at
        self.completed_at = completed_at
        self.model_id = model_id
        self.hyperparameters = hyperparameters

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CustomModel":
        return cls(
            id=data["id"],
            name=data["name"],
            status=data["status"],
            model_type=REVERSE_CUSTOM_MODEL_PRODUCT_MAPPING[data["settings"]["finetuneType"]],
            created_at=_parse_date(data["created_at"]),
            completed_at=_parse_date(data["completed_at"]) if "completed_at" in data else None,
            model_id=data["model"]["route"] if "model" in data else None,
            hyperparameters=HyperParameters.from_response(data["settings"]["hyperparameters"])
            if data["settings"]["hyperparameters"]
            else None,
        )


def _parse_date(datetime_string: str) -> datetime:
    return datetime.strptime(datetime_string, "%Y-%m-%dT%H:%M:%S.%f%z")
