"""Local save/load stub."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Optional

from app.sim.state import SimulationState


class SaveManager:
    """Manages local save/load for the simulation state."""

    def __init__(self) -> None:
        self.save_path = Path("save.json")

    def save(self, state: SimulationState) -> None:
        payload = asdict(state)
        self.save_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def load(self) -> Optional[SimulationState]:
        if not self.save_path.exists():
            return None
        payload = json.loads(self.save_path.read_text(encoding="utf-8"))
        return SimulationState(**payload)
