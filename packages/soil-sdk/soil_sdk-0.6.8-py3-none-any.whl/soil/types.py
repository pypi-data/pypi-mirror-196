""" Types used by soil library"""
# pylint:disable=unnecessary-ellipsis
from enum import Enum
from typing import Any, Dict, List, Protocol, Self, Type, TypedDict

from soil.storage.base_storage import BaseStorage

Plan = List[Dict[str, str]]


class GetModule(TypedDict):
    """Type for GET modules/:moduleId"""

    is_package: bool
    public_api: List[str]
    package_type: str


class GetModuleHash(TypedDict):
    """Type for GET modules/"""

    name: str
    hash: str


class ExperimentStatuses(Enum):
    """Experiment Statuses"""

    WAITING = "WAITING"
    EXECUTING = "EXECUTING"
    DONE = "DONE"
    ERROR = "ERROR"


class Experiment(TypedDict):
    """Type for GET experiments/:experimentId"""

    _id: str
    app_id: str
    outputs: Dict[str, str]
    experiment_status: str


class Result(TypedDict):
    """Type for GET results/:resultId"""

    _id: str
    type: str


class SerializableDataStructure(Protocol):
    """Data Strucutre base protocol"""

    @property
    def metadata(self: Self) -> TypedDict:
        """Metadata of the DS protocol"""
        ...

    def serialize(self) -> BaseStorage:
        """Serializes the DS."""
        ...

    @classmethod
    def deserialize(
        cls: Type[Self],
        storage: BaseStorage,
        metadata: Any,
    ) -> Self:
        """Deserialize DS method."""
        ...
