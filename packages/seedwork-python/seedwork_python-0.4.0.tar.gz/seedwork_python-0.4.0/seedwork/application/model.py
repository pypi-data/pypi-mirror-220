from dataclasses import asdict

from pydantic import BaseModel as _BaseModel
from typing_extensions import Self

from seedwork.domain import Entity


class BaseModel(_BaseModel):
    @classmethod
    def from_entity(cls, entity: Entity) -> Self:
        return cls(**asdict(entity))
