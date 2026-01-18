# Nyikagotchi

Offline, single-user “Tamagotchi for adults” simulation.

## Implementation-Ready Outline (Flutter / Android, Offline-First)
This section is a detailed, implementation-ready plan for an offline-first Android pet simulation built in Flutter (Dart), focusing on fast iteration, clean architecture, and a maintainable simulation engine.

### 1) High-Level Architecture (Modules + Responsibilities)
**Core modules**
- **app/**: app bootstrap, routing, theme, global providers. Owns navigation and high-level app lifecycle hooks (resume/pause).  
- **ui/**: screens and shared widgets. Pure UI with minimal logic.  
- **state/**: Riverpod providers, view models, and UI-facing state.  
- **data/**: Isar collections, repositories, seed loader, migrations.  
- **simulation/**: pure engine (deterministic), rules pipeline, RNG abstraction, balancing constants.  
- **models/**: domain models and DTOs (immutable).  
- **utils/**: time helpers, serialization, math/clamp, formatting.  

**Why Riverpod**
- Testable providers with minimal boilerplate.
- Supports scoped overrides (for deterministic RNG in tests).
- Good for fast iteration and modular state (no monolithic widget state).

### 2) Data Model Schema (Entities, Fields, Relationships)
**Storage approach:** Isar (fast, offline-only, simple schema, good Flutter support).

**Collections**
- **PetState**
  - `id` (isarId, singleton)
  - `name` (string)
  - `createdAt` (DateTime)
  - `lastUpdatedAt` (DateTime)
  - `ageStage` (enum: baby/teen/adult)
  - `careScore` (int, 0–100)
  - `hunger` (int, 0–100)
  - `energy` (int, 0–100)
  - `cleanliness` (int, 0–100)
  - `mood` (int, 0–100)
  - `traitIds` (list<string>)
  - `inventoryId` (string, fk to Inventory)
  - `journalId` (string, fk to Journal)

- **Trait**
  - `id` (string)
  - `name` (string)
  - `description` (string)
  - `modifiers` (JSON map: decay multipliers, event weight multipliers)

- **Item**
  - `id` (string)
  - `name` (string)
  - `type` (enum: food/toy/cleaning/boost)
  - `effects` (JSON map: stat deltas)
  - `cooldownMinutes` (int)
  - `cost` (int)

- **InventoryEntry**
  - `id` (isarId)
  - `itemId` (string)
  - `quantity` (int)

- **JournalEntry**
  - `id` (isarId)
  - `timestamp` (DateTime)
  - `type` (enum: event/action/system)
  - `text` (string)
  - `statSnapshot` (JSON map of stats)

- **EventDefinition**
  - `id` (string)
  - `name` (string)
  - `triggerConditions` (JSON rule expression)
  - `weight` (double)
  - `outcomes` (JSON: stat deltas, journal text, optional item grants)

- **BalanceConfig**
  - `id` (singleton)
  - `tickMinutes` (int, default 5)
  - `baseDecayRates` (JSON: per-stat decay per tick)
  - `thresholds` (JSON: e.g. hungry < 30)
  - `stageRules` (JSON: age thresholds + careScore requirements)

**Relationships**
- `PetState.traitIds` -> `Trait.id` (many-to-many via ids).
- `PetState.inventoryId` -> `InventoryEntry` list (1-to-many).
- `PetState.journalId` -> `JournalEntry` list (1-to-many).
- `EventDefinition` and `BalanceConfig` are seed data loaded once.

### 3) Simulation Engine Design (Tick Algorithm, Rules Pipeline, Events)
**Tick cadence**
- `tickMinutes = 5`
- `elapsedMinutes = now - lastUpdatedAt`
- `ticks = floor(elapsedMinutes / tickMinutes)`  
- Cap catch-up (e.g., max 7 days → 2016 ticks).

**Deterministic rules pipeline (testable)**
1. **applyDecay**: reduce stats by base decay rates.
2. **applyTraitModifiers**: adjust decay and event weights.
3. **evaluateThresholds**: compute threshold-based flags.
4. **rollEvents**: weighted selection from triggered events.
5. **applyConsequences**: apply event and trait effects.
6. **clamp**: ensure stats 0–100.
7. **persist**: write updated state + journal.

**Event model**
- Event definitions live in JSON/Isar, not hardcoded.
- Each event uses trigger conditions:
  - Example: `hunger < 30 AND mood < 40 AND trait = "Anxious"`.
- Weighting: base `weight` * trait modifiers.
- Outcomes: stat deltas + journal text + optional item grants.

**“While you were away” summary**
- Aggregate event counts and stat changes during catch-up.
- Example:
  - “While you were away (6h): Hunger -24, Energy -18. Events: 2x ‘Restless’, 1x ‘Messy Room’.”

### 4) Storage + Persistence Plan (Offline Only)
**Isar + JSON seed**
- **Seed data** stored in `assets/seed/*.json`: traits, items, events, balance config.
- On first launch: load seed into Isar if missing.
- **Migrations**: use Isar schema versioning and simple migration functions per version.
- **Single source of truth**: Isar collections; in-memory cache in repositories.

**Local-only**
- No network, no accounts.
- Backups deferred to future extension (export JSON).

### 5) UI Flow (Screens, Navigation, Widgets)
**Screens (max 4)**
1. **Pet Screen (Home)**
   - Pet sprite + stat bars (hunger, energy, cleanliness, mood).
   - Actions: Feed, Clean, Play, Sleep.
   - “While you were away” banner after catch-up.

2. **Stats Screen**
   - Detailed stats + careScore + ageStage.
   - Trait list with descriptions and effects.

3. **Inventory/Shop Screen**
   - Inventory items + shop list (buy with coins).
   - Item usage (apply effects).

4. **History/Journal Screen**
   - Scrollable journal timeline with event entries and snapshots.

**Navigation**
- Bottom navigation bar with 4 tabs.
- Deep links: none (offline-only).

**Widgets**
- `PetSpriteWidget`, `StatBarWidget`, `ActionButtonWidget`, `JournalEntryCard`.

### 6) Minimal MVP Vertical Slice Plan (Step-by-Step Tasks)
1. **Project scaffold**
   - Flutter app with Riverpod + Isar setup.
   - Base folder structure.
2. **Data layer**
   - Define Isar collections, seed loader.
   - Load initial `PetState`, `BalanceConfig`, `Traits`, `Items`, `Events`.
3. **Simulation engine**
   - Implement deterministic tick pipeline (pure Dart).
   - Add RNG abstraction + fixed-seed mode.
4. **State management**
   - Providers for pet state, inventory, journal.
   - App lifecycle hook (resume) triggers catch-up.
5. **UI**
   - Pet screen with sprite + stat bars + actions.
   - Stats + Inventory/Shop + Journal screens.
6. **Vertical slice flow**
   - Create pet → feed → persist → close app → time passes → reopen → catch-up → “While you were away”.

### 7) Pseudocode for Core Functions (Dart-like)
```dart
Future<void> runCatchUpTick(PetState pet, BalanceConfig balance, RNG rng) async {
  final now = DateTime.now();
  final elapsedMinutes = now.difference(pet.lastUpdatedAt).inMinutes;
  final ticks = (elapsedMinutes / balance.tickMinutes).floor();
  final cappedTicks = min(ticks, balance.maxCatchUpTicks);

  final summary = CatchUpSummary();
  var current = pet;

  for (var i = 0; i < cappedTicks; i++) {
    final result = runSingleTick(current, balance, rng);
    current = result.pet;
    summary.absorb(result);
  }

  current = current.copyWith(
    lastUpdatedAt: now.subtract(Duration(minutes: elapsedMinutes % balance.tickMinutes)),
  );

  await petRepository.save(current);
  await journalRepository.append(summary.toJournalEntries());
}

TickResult runSingleTick(PetState pet, BalanceConfig balance, RNG rng) {
  var next = pet;

  next = applyDecay(next, balance.baseDecayRates);
  next = applyTraitModifiers(next, balance, pet.traitIds);
  final triggers = evaluateThresholds(next, balance.thresholds);
  final events = rollEvents(triggers, pet.traitIds, rng);
  next = applyConsequences(next, events);
  next = clampStats(next, 0, 100);
  next = updateCareScore(next);

  return TickResult(pet: next, events: events);
}

List<EventDefinition> rollEvents(
  TriggerSet triggers,
  List<String> traitIds,
  RNG rng,
) {
  final candidates = eventRepository.queryByTriggers(triggers);
  final weighted = candidates.map((event) {
    final weight = event.weight * traitWeightModifier(event, traitIds);
    return WeightedEvent(event, weight);
  }).toList();
  return rng.rollWeighted(weighted, maxEventsPerTick: 1);
}
```

### 8) Test Plan (Unit Tests for Engine + Regression Cases)
**Unit tests**
- `applyDecay` reduces stats correctly.
- `applyTraitModifiers` applies multiplier by trait.
- `evaluateThresholds` flags correct trigger states.
- `rollEvents` uses deterministic RNG (fixed seed).
- `applyConsequences` modifies stats & journal entries.
- `runCatchUpTick` handles elapsed time, caps ticks, and updates `lastUpdatedAt`.

**Regression cases**
- Stats never exceed 0–100.
- Long catch-up (7 days) produces bounded output.
- Trait interactions don’t invert stats (e.g., negative multipliers).
- Events with zero candidates yield no crash.
- Stage progression (baby → teen → adult) respects careScore.

### 9) Future Extensions
- **Notifications**: local reminders based on thresholds or scheduled checks.
- **Backups**: export/import save to JSON or zip.
- **Content packs**: downloadable JSON packs for items, traits, and events.
- **Graphics**: simple frame animation or mood-based sprite variations.
- **Mini-games**: increase mood/coins without complicating core loop.

### Suggested Folder Structure (Flutter)
```
lib/
  app/            # routing, theme, app shell
  ui/             # screens, widgets
  state/          # Riverpod providers, viewmodels
  data/           # Isar collections, repositories, seed loader
  simulation/     # tick engine, rules, RNG, balance config
  models/         # domain models + DTOs
  utils/          # time, math, serialization
assets/
  seed/
    traits.json
    items.json
    events.json
    balance.json
```
