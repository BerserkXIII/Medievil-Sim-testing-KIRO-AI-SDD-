# Medieval Life Sim

Un RPG sandbox narrativo basado en sistemas, inspirado en Dwarf Fortress. El jugador vive día a día en la Edad Media, donde las necesidades básicas, las relaciones sociales y el azar convergen para generar historias emergentes.

**[English version](README.en.md)**

## Características

- **Sistema de capas**: atributos innatos, condiciones corporales, derivadas de salud, vitalidad
- **Narrativa emergente**: módulos reutilizables que se activan según el estado del personaje
- **Fractal funcional**: los mismos tipos de eventos se repiten a distintas escalas y contextos
- **Decisiones con peso**: cada acción tiene consecuencias que afectan el futuro
- **Viajes entre regiones**: movimiento dinámico con encuentros y preparación
- **Mundo vivo**: regiones con propiedades que cambian según eventos

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecución

```bash
python medieval_life/main.py
```

## Estructura del proyecto

```
medieval_life/
├── core/              # Motor del juego
│   ├── personaje.py   # Estructura de datos del personaje
│   ├── motor.py       # Cálculo de derivadas y avance del día
│   ├── modulos.py     # Evaluación y aplicación de módulos
│   ├── mundo.py       # Sistema de regiones y mundo
│   └── viaje.py       # Sistema de viajes y encuentros
├── data/              # Datos del juego
│   ├── linajes_data.py        # Linajes disponibles
│   ├── modulos_data.py        # Módulos narrativos
│   ├── regiones_data.py       # Regiones del mundo
│   └── encuentros_viaje_data.py # Encuentros de viaje
├── ui/                # Interfaz
│   └── interfaz.py    # UI con tkinter
├── tests/             # Tests automatizados
│   ├── test_motor.py
│   ├── test_modulos.py
│   ├── test_personaje.py
│   ├── test_mundo.py
│   └── test_viaje.py
├── main.py            # Punto de entrada
└── README.md          # Este archivo
```

## Testing

Ejecuta los tests con:

```bash
pytest tests/ -v
```

Para ver cobertura:

```bash
pytest tests/ --cov=core --cov-report=html
```

## Cómo jugar

1. **Crear personaje**: elige nombre, sexo, edad, región y linaje
2. **Cada día tiene 4 franjas**: mañana, mediodía, tarde, noche
3. **En cada franja**: elige una acción de las disponibles
4. **Las acciones tienen consecuencias**: afectan tu estado y el mundo
5. **Viaja entre regiones**: encuentra encuentros en el camino
6. **Sobrevive**: mantén tus necesidades básicas cubiertas

## Sistema de capas del personaje

### Capa -1: Atributos (innatos)
- Constitución, Resistencia, Inteligencia, Percepción, Voluntad, Carisma, Fe Innata, Fortuna

### Capa 0: Condiciones (corporales)
- Nutrición, Hidratación, Descanso, Heridas, Higiene, Temperatura Corporal, Presión Social, Enfermedades

### Capa 1: Derivadas (calculadas)
- Salud Física, Salud Mental, Condición

### Capa 2: Existencial
- Vitalidad (determina si estás vivo)

### Capa 3: Circunstanciales (sociales)
- Riqueza, Reputación, Fe, Lealtad

## Sistema de regiones

Cada región tiene:
- **Propiedades base**: geografía, clima
- **Condiciones**: población, estabilidad, religión, gobierno, epidemia, conflicto
- **Derivadas**: abundancia, seguridad, cohesión social
- **Flags emergentes**: hambruna, cultos paganos, bandidos, epidemia, guerra civil

Las regiones afectan:
- Qué módulos están disponibles
- Qué encuentros pueden ocurrir
- Cómo cambia el contexto del personaje

## Sistema de viajes

- **Distancia**: cada región tiene distancia a otras (0.5 a 3.0 días)
- **Clasificación**: viajes cortos (sin preparación), medios (advertencias), largos (preparación)
- **Encuentros**: bandidos, animales, viajeros (según región y preparación)
- **Preparación**: llevar arma, dinero, etc. afecta encuentros

## Desarrollo

### Rama principal: `main`
- Código estable, listo para jugar
- Solo cambios que pasan todos los tests

### Rama de desarrollo: `develop`
- Rama de trabajo principal
- Aquí se integran nuevas features

### Ramas de feature: `feature/nombre`
- Una rama por feature
- Se crea desde `develop`, se mergea de vuelta con PR

## Roadmap

- [ ] Parser de texto libre para acciones
- [ ] Más módulos narrativos (comercio, viajes, conflictos)
- [ ] Mundo vivo: peligros latentes que afectan sin que el jugador lo sepa
- [ ] Regiones con personalidad propia y sub-regiones
- [ ] Habilidades que evolucionan con el uso
- [ ] Generación de historia previa (simulación desde el nacimiento)
- [ ] Sistema de guardado/carga
- [ ] Expansión a otras zonas geográficas

## Filosofía de diseño

Este proyecto explora cómo narrativas complejas y atractivas pueden emerger de sistemas simples que interactúan, en lugar de historias ramificadas escritas a mano. Inspirado por:

- **Dwarf Fortress**: complejidad emergente de sistemas simples
- **Crusader Kings II**: narrativa personal de mecánicas sistémicas
- **Kingdom Come: Deliverance**: simulación inmersiva de vida medieval

El objetivo es crear un juego donde el jugador sienta que está viviendo una vida, no siguiendo una historia.

## Licencia

MIT

## Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el repositorio
2. Crea una rama de feature (`git checkout -b feature/amazing-feature`)
3. Commit tus cambios (`git commit -m 'feat: add amazing feature'`)
4. Push a la rama (`git push origin feature/amazing-feature`)
5. Abre un Pull Request

## Estado

**Prototipo funcional**. Los sistemas principales funcionan:
- ✓ Creación de personaje
- ✓ Loop diario con módulos
- ✓ Sistema de viajes con encuentros
- ✓ Mundo con regiones
- ✓ 136 tests automatizados

Próximos pasos: parser de texto, más eventos, persistencia.

## Contacto

Preguntas o sugerencias? Abre un issue en GitHub.
