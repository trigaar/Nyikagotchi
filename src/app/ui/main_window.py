"""Main UI window placeholder."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from app.sim.state import SimulationState
from app.persistence.storage import SaveManager


class MainWindow:
    """Minimal Tkinter shell to host the simulation UI."""

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Nyikagotchi")
        self.state = SimulationState.new_game()
        self.save_manager = SaveManager()
        self._build_layout()

    def _build_layout(self) -> None:
        container = ttk.Frame(self.root, padding=12)
        container.pack(fill=tk.BOTH, expand=True)

        header = ttk.Label(
            container,
            text="Nyikagotchi (Scaffold)",
            font=("Segoe UI", 16, "bold"),
        )
        header.pack(anchor=tk.W)

        description = ttk.Label(
            container,
            text="Offline-first simulation scaffold. Replace this with real UI panels.",
            wraplength=520,
        )
        description.pack(anchor=tk.W, pady=(8, 16))

        info = ttk.Label(
            container,
            text=f"Stage: {self.state.stage} | Age (days): {self.state.age_days}",
        )
        info.pack(anchor=tk.W)

        button_row = ttk.Frame(container)
        button_row.pack(anchor=tk.W, pady=(16, 0))

        save_button = ttk.Button(button_row, text="Save", command=self._save)
        save_button.pack(side=tk.LEFT)

        load_button = ttk.Button(button_row, text="Load", command=self._load)
        load_button.pack(side=tk.LEFT, padx=(8, 0))

    def _save(self) -> None:
        self.save_manager.save(self.state)

    def _load(self) -> None:
        loaded = self.save_manager.load()
        if loaded:
            self.state = loaded

    def run(self) -> None:
        self.root.mainloop()
