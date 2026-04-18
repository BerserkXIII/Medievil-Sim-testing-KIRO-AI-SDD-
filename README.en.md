# Medieval Life Sim

A narrative sandbox RPG based on emergent systems, inspired by Dwarf Fortress. The player lives day by day in the Middle Ages, where basic needs, social relationships, and chance converge to generate emergent stories.

**[Versión en español](README.md)**

## Features

- **Layered system architecture**: innate attributes, bodily conditions, derived health metrics, vitality
- **Emergent narrative**: reusable modules that activate based on character state
- **Functional fractal**: the same types of events repeat at different scales and contexts
- **Consequential decisions**: every action has consequences that shape the future
- **Travel between regions**: dynamic movement with encounters and preparation
- **Living world**: regions with properties that change based on events

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
│   ├── modulos.py     # Module evaluation and application
│   ├── mundo.py       # Region system and world
│   └── viaje.py       # Travel system and encounters
├── data/              # Game data
│   ├── linajes_data.py        # Available lineages
│   ├── modulos_data.py        # Narrative modules
│   ├── regiones_data.py       # World regions
│   └── encuentros_viaje_data.py # Travel encounters
├── ui/                # User interface
│   └── interfaz.py    # UI with tkinter
├── tests/             # Automated tests
│   ├── test_motor.py
│   ├── test_modulos.py
│   ├── test_personaje.py
│   ├── test_mundo.py
│   └── test_viaje.py
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

## How to Play

1. **Create character**: choose name, sex, age, region, and lineage
2. **Each day has 4 time periods**: morning, midday, afternoon, night
3. **Each period**: choose an action from available options
4. **Actions have consequences**: they affect your state and the world
5. **Travel between regions**: encounter events on the road
6. **Survive**: keep your basic needs covered

## Character State Layers

### Layer -1: Attributes (innate)
- Constitution, Resistance, Intelligence, Perception, Will, Charisma, Faith Innate, Fortune

### Layer 0: Conditions (bodily)
- Nutrition, Hydration, Rest, Wounds, Hygiene, Body Temperature, Social Pressure, Diseases

### Layer 1: Derived (calculated)
- Physical Health, Mental Health, Condition

### Layer 2: Existential
- Vitality (determines if you're alive)

### Layer 3: Circumstantial (social)
- Wealth, Reputation, Faith, Loyalty

## Region System

Each region has:
- **Base properties**: geography, climate
- **Conditions**: population, stability, religion, government, epidemic, conflict
- **Derived**: abundance, security, social cohesion
- **Emergent flags**: famine, pagan cults, bandits, epidemic, civil war

Regions affect:
- Which modules are available
- What encounters can occur
- How the character's context changes

## Travel System

- **Distance**: each region has distance to others (0.5 to 3.0 days)
- **Classification**: short trips (no prep), medium (warnings), long (preparation)
- **Encounters**: bandits, animals, travelers (based on region and preparation)
- **Preparation**: carrying weapons, money, etc. affects encounters

## Development

### Main branch: `main`
- Stable code, ready to play
- Only changes that pass all tests

### Development branch: `develop`
- Main working branch
- New features are integrated here

### Feature branches: `feature/name`
- One branch per feature
- Created from `develop`, merged back with PR

## Roadmap

- [ ] Free-form text parser for actions
- [ ] More narrative modules (commerce, travel, conflicts)
- [ ] Living world: latent dangers that affect without player knowledge
- [ ] Regions with distinct personality and sub-regions
- [ ] Skills that evolve through use
- [ ] Procedural backstory generation (simulation from birth)
- [ ] Save/load system
- [ ] Expansion to other geographic zones

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

## Status

**Functional prototype**. Core systems working:
- ✓ Character creation
- ✓ Daily loop with modules
- ✓ Travel system with encounters
- ✓ World with regions
- ✓ 136 automated tests

Next steps: text parser, more events, persistence.

## Contact

Questions or suggestions? Open an issue on GitHub.
