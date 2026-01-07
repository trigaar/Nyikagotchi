"""Simulation state placeholders."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SimulationState:
    stage: str
    age_days: int

    @classmethod
    def new_game(cls) -> "SimulationState":
        return cls(stage="infant", age_days=0)
