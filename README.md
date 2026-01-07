# Nyikagotchi

Offline, single-user “Tamagotchi for adults” simulation.

## Project Scaffold (Template)
This repository provides a **lightweight, offline-first scaffold** using **Python + Tkinter** (no external UI dependencies). It is designed to be portable, easy to run, and friendly to incremental development.

### Quick Start
1) Ensure Python 3.11+ is installed.
2) From the repo root:
   ```bash
   python -m app.main
   ```

## Repo Structure
```
src/
  app/
    main.py              # App entrypoint (Tkinter shell)
    ui/
      main_window.py     # Main window layout placeholder
    sim/
      state.py           # Core simulation state placeholders
    persistence/
      storage.py         # Local save/load stubs
    assets/
      README.md          # Asset pipeline conventions placeholder
```

## README Template Outline (fill-in guidance)
Use this as the structure for a full product README when the implementation progresses.

### 1) Overview
- One-paragraph summary of the simulation.
- Key pillars: needs, education, environment, genetics, family.

### 2) Features
- Bullet list of major systems (needs, skills, events, family, catch-up).

### 3) Installation
- Offline installer steps.
- Python-based dev setup instructions.

### 4) Usage
- How to start the app.
- How to interpret dashboards/alerts.

### 5) Simulation Model
- Summary of time flow, decay rates, and life stages.

### 6) Data & Persistence
- Save format, versioning, and recovery behavior.

### 7) Asset Pipeline
- Sprite pack folder conventions and naming.

### 8) Development
- How to run tests.
- Code layout and contribution guide.

### 9) Roadmap
- Milestones and planned features.

## Notes
- This scaffold is intentionally minimal and offline-only.
- The UI layer is a placeholder; swap or extend as needed.
