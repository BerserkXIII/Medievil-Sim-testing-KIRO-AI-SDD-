"""
Travel system: moving between regions with encounters and preparation.
"""

import random
from core.mundo import obtener_contexto_personaje, actualizar_derivadas_region
from data.regiones_data import obtener_region


def _normalizar(valor: float) -> float:
    """Clamp value to [0, 1]."""
    return max(0.0, min(1.0, valor))


def calcular_distancia(region_origen_nombre: str, region_destino_nombre: str) -> float:
    """
    Get travel distance between two regions in days.
    """
    region_origen = obtener_region(region_origen_nombre)
    
    if region_destino_nombre not in region_origen["distancias"]:
        raise ValueError(f"No route from {region_origen_nombre} to {region_destino_nombre}")
    
    return region_origen["distancias"][region_destino_nombre]


def obtener_destinos_disponibles(region_actual: str) -> dict:
    """
    Get all available destinations from current region.
    Returns dict with destination name and distance.
    """
    region = obtener_region(region_actual)
    return region["distancias"]


def clasificar_viaje(distancia: float) -> str:
    """
    Classify travel by distance.
    - "corto": < 0.5 days (no preparation needed)
    - "medio": 0.5-1.5 days (preparation recommended)
    - "largo": >= 1.5 days (preparation required)
    """
    if distancia < 0.5:
        return "corto"
    elif distancia < 1.5:
        return "medio"
    else:
        return "largo"


def generar_advertencias_viaje(region_destino_obj: dict) -> list:
    """
    Generate travel warnings based on destination region conditions.
    """
    advertencias = []
    
    if region_destino_obj["peligro_latente"] > 0.5:
        advertencias.append("Escuchaste rumores de bandidos en el camino.")
    
    if region_destino_obj["condiciones"]["epidemia"] > 0.3:
        advertencias.append("Hay enfermedad reportada en la región.")
    
    if "guerra_civil" in region_destino_obj["flags"]:
        advertencias.append("Hay conflicto político en la zona.")
    
    if region_destino_obj["derivadas"]["seguridad"] < 0.3:
        advertencias.append("La región es conocida por ser peligrosa.")
    
    return advertencias


def preparar_viaje(personaje: dict, region_destino_nombre: str) -> dict:
    """
    Prepare travel. Returns travel info and options based on distance and warnings.
    """
    distancia = calcular_distancia(personaje["region"], region_destino_nombre)
    tipo_viaje = clasificar_viaje(distancia)
    region_destino = obtener_region(region_destino_nombre)
    advertencias = generar_advertencias_viaje(region_destino)
    
    return {
        "distancia": distancia,
        "tipo_viaje": tipo_viaje,
        "region_destino": region_destino_nombre,
        "advertencias": advertencias,
        "requiere_preparacion": tipo_viaje in ["medio", "largo"],
    }


def generar_encuentro_bandidos(personaje: dict, preparacion: str = None) -> dict:
    """
    Generate bandit encounter. Options vary by preparation.
    """
    opciones = [
        {
            "texto_boton": "Huir",
            "transformaciones": {"heridas": +0.05},
            "texto_resultado": "Logras escapar corriendo.",
        }
    ]
    
    # Si llevas arma, puedes luchar
    if preparacion == "arma":
        opciones.insert(0, {
            "texto_boton": "Luchar",
            "transformaciones": {"heridas": +0.15, "peligro_percibido": -0.1},
            "texto_resultado": "Luchas valientemente. Logras ahuyentarlos.",
        })
    
    # Si llevas dinero, puedes sobornar
    if preparacion == "dinero":
        opciones.insert(0, {
            "texto_boton": "Sobornar",
            "transformaciones": {"riqueza": -0.1},
            "texto_resultado": "Les das dinero. Te dejan pasar.",
        })
    
    return {
        "tipo": "bandidos",
        "texto": "En el camino, unos bandidos te cierran el paso.",
        "opciones": opciones,
    }


def generar_encuentro_animal(personaje: dict) -> dict:
    """
    Generate wild animal encounter.
    """
    animales = [
        ("lobo", 0.2),
        ("oso", 0.3),
        ("jabalí", 0.15),
    ]
    animal, daño = random.choice(animales)
    
    return {
        "tipo": "animal",
        "texto": f"Un {animal} salvaje aparece en el camino.",
        "opciones": [
            {
                "texto_boton": "Luchar",
                "transformaciones": {"heridas": +daño},
                "texto_resultado": f"Luchas contra el {animal}. Resultas herido.",
            },
            {
                "texto_boton": "Huir",
                "transformaciones": {"heridas": +daño * 0.3},
                "texto_resultado": f"Huyes del {animal}. Logras escapar con rasguños.",
            },
        ],
    }


def generar_encuentro_viajero(personaje: dict) -> dict:
    """
    Generate neutral traveler encounter.
    """
    return {
        "tipo": "viajero",
        "texto": "Encuentras a otro viajero en el camino.",
        "opciones": [
            {
                "texto_boton": "Hablar",
                "transformaciones": {"presion_social": -0.05},
                "texto_resultado": "Compartes historias. El viaje se hace menos tedioso.",
            },
            {
                "texto_boton": "Ignorar",
                "transformaciones": {},
                "texto_resultado": "Continúas tu camino sin interactuar.",
            },
        ],
    }


def generar_encuentro_viaje(personaje: dict, region_destino_nombre: str, preparacion: str = None) -> dict:
    """
    Generate a travel encounter based on region conditions and preparation.
    Returns None if no encounter, or encounter dict if one occurs.
    """
    region_destino = obtener_region(region_destino_nombre)
    
    # Probabilidad base de encuentro
    prob_encuentro = region_destino["peligro_latente"]
    
    # Preparación reduce probabilidad
    if preparacion == "arma":
        prob_encuentro *= 0.6
    elif preparacion == "dinero":
        prob_encuentro *= 0.8
    
    # Flags aumentan probabilidad
    if "bandidos_organizados" in region_destino["flags"]:
        prob_encuentro += 0.3
    
    # Normalizar probabilidad
    prob_encuentro = _normalizar(prob_encuentro)
    
    # Decidir si hay encuentro
    if random.random() > prob_encuentro:
        return None
    
    # Generar encuentro según flags
    if "bandidos_organizados" in region_destino["flags"]:
        return generar_encuentro_bandidos(personaje, preparacion)
    elif random.random() > 0.5:
        return generar_encuentro_animal(personaje)
    else:
        return generar_encuentro_viajero(personaje)


def aplicar_degradacion_viaje(personaje: dict, distancia: float) -> dict:
    """
    Apply daily degradation during travel.
    """
    dias = int(distancia)
    
    for _ in range(dias):
        personaje["condiciones"]["nutricion"] = _normalizar(
            personaje["condiciones"]["nutricion"] - 0.08
        )
        personaje["condiciones"]["hidratacion"] = _normalizar(
            personaje["condiciones"]["hidratacion"] - 0.12
        )
        personaje["condiciones"]["descanso"] = _normalizar(
            personaje["condiciones"]["descanso"] - 0.1
        )
    
    return personaje


def realizar_viaje(personaje: dict, region_destino_nombre: str, preparacion: str = None) -> dict:
    """
    Perform travel. Returns result with state, encounter (if any), and updated character.
    """
    distancia = calcular_distancia(personaje["region"], region_destino_nombre)
    
    # Apply degradation
    personaje = aplicar_degradacion_viaje(personaje, distancia)
    
    # Generate encounter
    encuentro = generar_encuentro_viaje(personaje, region_destino_nombre, preparacion)
    
    if encuentro:
        # Encounter occurred, return for player to handle
        return {
            "estado": "encuentro",
            "encuentro": encuentro,
            "personaje": personaje,
            "region_destino": region_destino_nombre,
        }
    
    # Travel completed successfully
    personaje["region"] = region_destino_nombre
    region_nueva = obtener_region(region_destino_nombre)
    personaje["contexto"] = obtener_contexto_personaje(region_nueva)
    
    return {
        "estado": "llegada",
        "personaje": personaje,
        "texto": f"Llegas a {region_nueva['nombre']}.",
    }


def completar_viaje_tras_encuentro(personaje: dict, region_destino_nombre: str) -> dict:
    """
    Complete travel after handling an encounter.
    """
    personaje["region"] = region_destino_nombre
    region_nueva = obtener_region(region_destino_nombre)
    personaje["contexto"] = obtener_contexto_personaje(region_nueva)
    
    return {
        "estado": "llegada",
        "personaje": personaje,
        "texto": f"Continúas tu camino y llegas a {region_nueva['nombre']}.",
    }
