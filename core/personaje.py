"""
Estructura de datos del personaje.
Capas: -1 (atributos), 0 (condiciones), 0b (contexto),
       1 (derivadas), 2 (vitalidad), 3 (circunstanciales)
"""

import random


RANGOS_EDAD = {
    "niño":    (10, 14),
    "joven":   (15, 25),
    "adulto":  (26, 45),
    "maduro":  (46, 60),
    "anciano": (61, 90),
}


def _stat_semialeat(base: int, modificador: int, minimo: int = 1, maximo: int = 10) -> int:
    """Genera un stat con base aleatoria sesgada por modificador de linaje/región."""
    ruido = random.randint(-1, 1)
    return max(minimo, min(maximo, base + modificador + ruido))


def crear_personaje(nombre: str, sexo: str, edad: int, region: str, linaje: dict) -> dict:
    """
    Crea el estado inicial del personaje a partir de los inputs del jugador.
    linaje es un dict con modificadores de stats y tags narrativos.
    """

    # --- capa -1: atributos (semialeatarios, sesgados por linaje y región) ---
    mods = linaje.get("modificadores_stats", {})
    atributos = {
        "constitucion": _stat_semialeat(5, mods.get("constitucion", 0)),
        "resistencia":  _stat_semialeat(5, mods.get("resistencia", 0)),
        "inteligencia": _stat_semialeat(5, mods.get("inteligencia", 0)),
        "percepcion":   _stat_semialeat(5, mods.get("percepcion", 0)),
        "voluntad":     _stat_semialeat(5, mods.get("voluntad", 0)),
        "carisma":      _stat_semialeat(5, mods.get("carisma", 0)),
        "fe_innata":    _stat_semialeat(5, mods.get("fe_innata", 0)),
        "fortuna":      _stat_semialeat(5, 0),  # siempre puro aleatorio
    }

    # --- capa -1b: habilidades (aprendidas, empiezan según linaje) ---
    habilidades_base = linaje.get("habilidades_base", {})
    habilidades = {
        "combate":      habilidades_base.get("combate", 0),
        "oficio":       habilidades_base.get("oficio", 0),
        "conocimiento": habilidades_base.get("conocimiento", 0),
        "sigilo":       habilidades_base.get("sigilo", 0),
    }

    # --- capa 0: condiciones personales ---
    condiciones = {
        "nutricion":            0.7,
        "hidratacion":          0.7,
        "descanso":             0.8,
        "heridas":              0.0,
        "higiene":              0.6,
        "temperatura_corporal": 0.7,
        "presion_social":       0.2,
        "enfermedades":         [],
        "peligro_latente":      0.0,
        "peligro_percibido":    0.0,
    }

    # --- capa 0b: contexto ambiental (viene del mundo, no del personaje) ---
    contexto = {
        "clima_region":           0.5,
        "disponibilidad_agua":    0.7,
        "disponibilidad_comida":  0.7,
        "tension_social":         0.2,
    }

    # --- capa 1: derivadas (se recalculan cada día) ---
    estado = {
        "salud_fisica": 0.0,
        "salud_mental": 0.0,
        "condicion":    0.0,
    }

    # --- capa 2: existencial ---
    vitalidad = 1.0
    dias_criticos = 0  # contador de días bajo umbral crítico

    # --- capa 3: circunstanciales ---
    social = {
        "riqueza":    linaje.get("riqueza_inicial", 0.3),
        "reputacion": 0.0,
        "fe":         0.3,
        "lealtad":    0.3,
    }

    return {
        # identidad
        "nombre":   nombre,
        "sexo":     sexo,
        "edad":     edad,
        "region":   region,
        "linaje":   linaje.get("nombre", "desconocido"),
        "tags":     linaje.get("tags", []),

        # capas
        "atributos":    atributos,
        "habilidades":  habilidades,
        "condiciones":  condiciones,
        "contexto":     contexto,
        "estado":       estado,
        "vitalidad":    vitalidad,
        "dias_criticos": dias_criticos,
        "social":       social,

        # flags narrativos activos
        "flags": set(),

        # historial (para convergencia estructural futura)
        "dia": 1,
        "historial": [],
    }
