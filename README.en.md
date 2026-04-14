# Medieval Life Sim

A narrative sandbox RPG based on emergent systems, inspired by Dwarf Fortress. The player lives day by day in the Middle Ages, where basic needs, social relationships, and chance converge to generate emergent stories.

**[Versión en español](README.md)**

## Features

- **Layered system architecture**: innate attributes, bodily conditions, derived health metrics, vitality
- **Emergent narrative**: reusable modules that activate based on character state
- **Functional fractal**: the same types of events repeat at different scales and contexts
- **Consequential decisions**: every action has consequences that shape the future

## Installation

```bash
pip install -r requirements.txt
```

## Running the Game

```bash
python medieval_life/main.py
```

## Project Structure

```
medieval_life/
├── core/              # Game engine
│   ├── personaje.py   # Character data structure
│   ├── motor.py       # Derivative calculation and day advancement
│   └── modulos.py     # Module evaluation and application
├── data/              # Game data
│   ├── linajes_data.py    # Available lineages
│   └── modulos_data.py    # Narrative modules
├── ui/                # User interface
│   └── interfaz.py    # UI with tkinter
├── tests/             # Automated tests
│   ├── test_motor.py
│   ├── test_modulos.py
│   └── test_personaje.py
├── main.py            # Entry point
└── README.en.md       # This file
```

## Testing

Run tests with:

```bash
pytest tests/ -v
```

For coverage report:

```bash
pytest tests/ --cov=core --cov-report=html
```

## Development Workflow

### Main branches

- **`main`**: stable code, ready to play. Only changes that pass all tests.
- **`develop`**: integration branch. New features are merged here.

### Feature branches

Create a new branch for each feature:

```bash
git checkout develop
git checkout -b feature/your-feature-name
# ... make changes ...
git add .
git commit -m "feat: description of changes"
git push origin feature/your-feature-name
# Create a Pull Request on GitHub
```

### Commit message conventions

- `feat:` new feature
- `fix:` bug fix
- `test:` test additions or modifications
- `refactor:` code refactoring
- `docs:` documentation changes
- `chore:` maintenance tasks

Example:
```bash
git commit -m "feat: add 5 new commerce modules"
git commit -m "test: add boundary tests for vitalidad calculation"
git commit -m "fix: constitucion modifier was too strong"
```

## System Design

### Character State Layers

The character is represented as a multi-layered state machine:

**Layer -1: Attributes** (innate, semi-random based on lineage)
- Constitution, Resistance, Intelligence, Perception, Will, Charisma, Faith Innate, Fortune

**Layer 0: Conditions** (environmental and bodily)
- Nutrition, Hydration, Rest, Wounds, Hygiene, Body Temperature, Social Pressure, Diseases

**Layer 0b: Environmental Context** (comes from the world)
- Region Climate, Water Availability, Food Availability, Social Tension

**Layer 1: Derived** (recalculated daily)
- Physical Health, Mental Health, Condition

**Layer 2: Existential**
- Vitality (determines if character is alive)

**Layer 3: Circumstantial** (affect available modules)
- Wealth, Reputation, Faith, Loyalty

### Narrative Modules

Each module is a narrative event with:
- **Activation conditions**: what must be true for the module to appear
- **Options**: 2-3 player choices
- **Transformations**: how the character state changes based on choice
- **Text**: narrative description (with variable interpolation)

Modules are organized by time of day: morning, midday, afternoon, night.

### Fractal Structure

The system is fractal in:
- **Repetition**: the same module types appear at different scales
- **Transformation rules**: consistent rules apply recursively
- **Conflict escalation**: micro conflicts can escalate to macro events

Example: `M_authority` appears as:
- Micro: local bailiff demands payment
- Meso: lord summons for judgment
- Macro: bishop declares heresy in the region

## Roadmap

- [ ] More narrative modules (commerce, travel, conflicts)
- [ ] Living world: latent dangers that affect the player without their knowledge
- [ ] Regions with distinct personalities and mechanics
- [ ] Skills that evolve through use
- [ ] Procedural backstory generation (simulation from birth)
- [ ] Free-form text parser for actions
- [ ] Save/load system
- [ ] Multiple character runs and legacy system

## Design Philosophy

This project explores how complex, engaging narratives can emerge from simple, interacting systems rather than authored branching paths. Inspired by:

- **Dwarf Fortress**: emergent complexity from system interaction
- **Crusader Kings II**: personal narrative from mechanical systems
- **Kingdom Come: Deliverance**: immersive medieval life simulation

The goal is to create a game where the player feels they're living a life, not following a story.

## License

MIT

## Contributing

Contributions are welcome. Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Contact

Questions or suggestions? Open an issue on GitHub.

---

**Status**: Early prototype. Core systems working, expanding content and features.
