from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field

from moontour_common.models.coordinates import Coordinates


class PhaseStatus(StrEnum):
    waiting = 'waiting'
    running = 'running'
    finished = 'finished'


class Phase(BaseModel):
    status: PhaseStatus
    target: Coordinates
    start_time: datetime = Field(default_factory=datetime.now)
    end_time: datetime | None


class HealthPhase(Phase):
    damage_multiplier: float = 1
