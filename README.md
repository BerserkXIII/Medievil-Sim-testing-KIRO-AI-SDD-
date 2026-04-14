# Medieval Life Sim

Un RPG sandbox narrativo basado en sistemas, inspirado en Dwarf Fortress. El jugador vive día a día en la Edad Media, donde las necesidades básicas, las relaciones sociales y el azar convergen para generar historias emergentes.

## Características

- **Sistema de capas**: atributos innatos, condiciones corporales, derivadas de salud, vitalidad
- **Narrativa emergente**: módulos reutilizables que se activan según el estado del personaje
- **Fractal funcional**: los mismos tipos de eventos se repiten a distintas escalas y contextos
- **Decisiones con peso**: cada acción tiene consecuencias que afectan el futuro

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
│   └── modulos.py     # Evaluación y aplicación de módulos
├── data/              # Datos del juego
│   ├── linajes_data.py    # Linajes disponibles
│   └── modulos_data.py    # Módulos narrativos
├── ui/                # Interfaz
│   └── interfaz.py    # UI con tkinter
├── tests/             # Tests automatizados
│   ├── test_motor.py
│   ├── test_modulos.py
│   └── test_personaje.py
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

Ejemplo:
```bash
git checkout develop
git checkout -b feature/mas-modulos
# ... hacer cambios ...
git add .
git commit -m "feat: añadir 5 módulos nuevos de comercio"
git push origin feature/mas-modulos
# Crear PR en GitHub
```

## Roadmap

- [ ] Más módulos narrativos (comercio, viajes, conflictos)
- [ ] Mundo vivo: peligros latentes que afectan sin que el jugador lo sepa
- [ ] Regiones con personalidad propia
- [ ] Habilidades que evolucionan con el uso
- [ ] Generación de historia previa (simulación desde el nacimiento)
- [ ] Parser de texto libre para acciones

## Licencia

MIT (o la que prefieras)
