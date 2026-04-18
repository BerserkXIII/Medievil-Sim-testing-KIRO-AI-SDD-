"""
World system: regions and their properties.
Each region has layers like the character:
- Layer -1: base attributes (climate, geography)
- Layer 0: conditions (population, stability)
- Layer 1: derived (security, cohesion)
- Layer 2: emergent (flags like "hambruna", "cultos_paganos")
"""


def _normalizar(valor: float) -> float:
    """Clamp value to [0, 1]."""
    return max(0.0, min(1.0, valor))


def calcular_abundancia(poblacion: float, clima: float, geografia: float) -> float:
    """
    Layer 0 → Layer 1.
    Abundance depends on population, climate, and geography.
    Better climate and geography = more resources.
    """
    # Geography affects base resource availability
    base_recursos = geografia * 0.6 + clima * 0.4
    
    # Population affects how much is available per person
    # High population = more competition, less per capita
    # But also more trade and organization
    eficiencia = 0.5 + (poblacion * 0.3)
    
    abundancia = base_recursos * eficiencia
    return _normalizar(abundancia)


def calcular_seguridad(estabilidad: float, poblacion: float, gobierno: float) -> float:
    """
    Layer 0 → Layer 1.
    Security depends on political stability, population, and government type.
    """
    # Stability is the main factor
    base_seguridad = estabilidad * 0.5
    
    # Government affects security (tyranny can be stable but oppressive)
    # Moderate government is safest
    mod_gobierno = 1.0 - abs(gobierno - 0.5) * 0.3
    
    # Population affects security (more people = more crime, but also more guards)
    mod_poblacion = 0.7 + (poblacion * 0.3)
    
    seguridad = base_seguridad * mod_gobierno * mod_poblacion
    return _normalizar(seguridad)


def calcular_cohesion_social(religion: float, gobierno: float, abundancia: float) -> float:
    """
    Layer 0 → Layer 1.
    Social cohesion depends on religion, government, and abundance.
    """
    # Religion provides unity
    aporte_religion = religion * 0.4
    
    # Moderate government is best for cohesion
    # Tyranny and anarchy both reduce it
    mod_gobierno = 1.0 - abs(gobierno - 0.5) * 0.4
    
    # Abundance helps cohesion (people are happier when fed)
    aporte_abundancia = abundancia * 0.3
    
    cohesion = (aporte_religion + aporte_abundancia) * mod_gobierno
    return _normalizar(cohesion)


def calcular_peligro_latente(seguridad: float, conflicto: float, epidemia: float) -> float:
    """
    Layer 1 → Layer 2.
    Latent danger: threats the character doesn't know about yet.
    """
    # Low security = bandits, criminals
    peligro_seguridad = (1.0 - seguridad) * 0.5
    
    # Active conflict = war, violence
    peligro_conflicto = conflicto * 0.3
    
    # Epidemic = disease
    peligro_epidemia = epidemia * 0.2
    
    peligro = peligro_seguridad + peligro_conflicto + peligro_epidemia
    return _normalizar(peligro)


def actualizar_derivadas_region(region: dict) -> dict:
    """
    Recalculate all derived values for a region.
    Called once per day cycle.
    """
    c = region["condiciones"]
    
    # Layer 1: derived
    abundancia = calcular_abundancia(c["poblacion"], c["clima"], region["geografia"])
    seguridad = calcular_seguridad(c["estabilidad"], c["poblacion"], c["gobierno"])
    cohesion = calcular_cohesion_social(c["religion"], c["gobierno"], abundancia)
    
    region["derivadas"]["abundancia"] = abundancia
    region["derivadas"]["seguridad"] = seguridad
    region["derivadas"]["cohesion"] = cohesion
    
    # Layer 2: emergent flags
    region["flags"].clear()
    
    if abundancia < 0.2:
        region["flags"].add("hambruna")
    
    if cohesion < 0.3 and c["religion"] < 0.4:
        region["flags"].add("cultos_paganos")
    
    if seguridad < 0.2:
        region["flags"].add("bandidos_organizados")
    
    if c["epidemia"] > 0.5:
        region["flags"].add("epidemia_activa")
    
    if c["conflicto"] > 0.6:
        region["flags"].add("guerra_civil")
    
    # Layer 2: peligro latente
    peligro = calcular_peligro_latente(seguridad, c["conflicto"], c["epidemia"])
    region["peligro_latente"] = peligro
    
    return region


def obtener_contexto_personaje(region: dict) -> dict:
    """
    Extract the environmental context that affects the character.
    This is what goes into personaje["contexto"].
    """
    d = region["derivadas"]
    c = region["condiciones"]
    
    return {
        "clima_region": c["clima"],
        "disponibilidad_agua": d["abundancia"] * 0.8,
        "disponibilidad_comida": d["abundancia"] * 0.7,
        "tension_social": (1.0 - d["cohesion"]) * 0.8,  # inverse
        "peligro_latente": region["peligro_latente"],
    }


def avanzar_ciclo_region(region: dict) -> dict:
    """
    Advance one day cycle for the region.
    Apply passive degradation and changes.
    """
    c = region["condiciones"]
    
    # Stability slowly returns to base (unless there's active conflict)
    if c["conflicto"] > 0.3:
        c["estabilidad"] = _normalizar(c["estabilidad"] - 0.05)
    else:
        c["estabilidad"] = _normalizar(c["estabilidad"] + 0.02)
    
    # Epidemia slowly fades if no new cases
    c["epidemia"] = _normalizar(c["epidemia"] - 0.03)
    
    # Conflict slowly de-escalates
    c["conflicto"] = _normalizar(c["conflicto"] - 0.02)
    
    # Recalculate all derivates
    return actualizar_derivadas_region(region)
