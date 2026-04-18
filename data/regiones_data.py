"""
Mediterranean region data.
6 base regions with different characteristics.
Each can be expanded into sub-regions later.
"""

REGIONES = {
    "puerto_costero": {
        "nombre": "Puerto Costero",
        "tipo": "ciudad",
        "descripcion": "A bustling coastal city. Trade, merchants, and sailors everywhere.",
        
        # Layer -1: base attributes
        "geografia": 0.8,  # good harbors, fertile land nearby
        "clima": 0.6,      # mediterranean: warm, pleasant
        
        # Layer 0: conditions
        "condiciones": {
            "poblacion": 0.8,        # very populated
            "clima": 0.6,
            "estabilidad": 0.6,      # relatively stable
            "gobierno": 0.6,         # merchant republic or similar
            "religion": 0.7,         # organized church
            "epidemia": 0.0,
            "conflicto": 0.1,        # occasional tensions
        },
        
        # Layer 1: derived (calculated)
        "derivadas": {
            "abundancia": 0.0,       # will be calculated
            "seguridad": 0.0,
            "cohesion": 0.0,
        },
        
        # Layer 2: emergent
        "peligro_latente": 0.0,
        "flags": set(),
        
        # Narrative
        "historial": [],
    },

    "aldea_agricola": {
        "nombre": "Aldea Agrícola",
        "tipo": "aldea",
        "descripcion": "A quiet farming village. Fields, orchards, and simple folk.",
        
        "geografia": 0.7,  # fertile soil
        "clima": 0.6,
        
        "condiciones": {
            "poblacion": 0.3,        # small
            "clima": 0.6,
            "estabilidad": 0.7,      # stable, peaceful
            "gobierno": 0.4,         # feudal, lord's rule
            "religion": 0.8,         # very religious
            "epidemia": 0.0,
            "conflicto": 0.0,        # no conflict
        },
        
        "derivadas": {
            "abundancia": 0.0,
            "seguridad": 0.0,
            "cohesion": 0.0,
        },
        
        "peligro_latente": 0.0,
        "flags": set(),
        "historial": [],
    },

    "montaña_rocosa": {
        "nombre": "Montaña Rocosa",
        "tipo": "montaña",
        "descripcion": "Harsh mountain terrain. Bandits, hunters, and hermits.",
        
        "geografia": 0.2,  # harsh, difficult
        "clima": 0.3,      # cold
        
        "condiciones": {
            "poblacion": 0.1,        # very sparse
            "clima": 0.3,
            "estabilidad": 0.3,      # unstable, lawless
            "gobierno": 0.1,         # no real government
            "religion": 0.2,         # pagan, folk beliefs
            "epidemia": 0.0,
            "conflicto": 0.2,        # constant small conflicts
        },
        
        "derivadas": {
            "abundancia": 0.0,
            "seguridad": 0.0,
            "cohesion": 0.0,
        },
        
        "peligro_latente": 0.0,
        "flags": set(),
        "historial": [],
    },

    "bosque_denso": {
        "nombre": "Bosque Denso",
        "tipo": "bosque",
        "descripcion": "Deep forest. Hunters, outlaws, and wild animals.",
        
        "geografia": 0.4,  # moderate resources
        "clima": 0.5,      # temperate
        
        "condiciones": {
            "poblacion": 0.15,       # very sparse
            "clima": 0.5,
            "estabilidad": 0.4,      # unstable
            "gobierno": 0.0,         # no government
            "religion": 0.3,         # pagan, nature worship
            "epidemia": 0.0,
            "conflicto": 0.1,        # occasional tensions
        },
        
        "derivadas": {
            "abundancia": 0.0,
            "seguridad": 0.0,
            "cohesion": 0.0,
        },
        
        "peligro_latente": 0.0,
        "flags": set(),
        "historial": [],
    },

    "ciudad_amurallada": {
        "nombre": "Ciudad Amurallada",
        "tipo": "ciudad",
        "descripcion": "A fortified city. Soldiers, nobles, and intrigue.",
        
        "geografia": 0.6,  # defensible position
        "clima": 0.5,
        
        "condiciones": {
            "poblacion": 0.7,        # large
            "clima": 0.5,
            "estabilidad": 0.5,      # moderate, political tensions
            "gobierno": 0.8,         # strong, authoritarian
            "religion": 0.6,         # organized but contested
            "epidemia": 0.0,
            "conflicto": 0.3,        # political conflicts
        },
        
        "derivadas": {
            "abundancia": 0.0,
            "seguridad": 0.0,
            "cohesion": 0.0,
        },
        
        "peligro_latente": 0.0,
        "flags": set(),
        "historial": [],
    },

    "desierto_arido": {
        "nombre": "Desierto Árido",
        "tipo": "desierto",
        "descripcion": "Harsh desert. Nomads, oases, and mirages.",
        
        "geografia": 0.1,  # very harsh
        "clima": 0.9,      # very hot
        
        "condiciones": {
            "poblacion": 0.05,       # extremely sparse
            "clima": 0.9,
            "estabilidad": 0.2,      # very unstable
            "gobierno": 0.0,         # no government
            "religion": 0.5,         # mixed beliefs
            "epidemia": 0.0,
            "conflicto": 0.4,        # tribal conflicts
        },
        
        "derivadas": {
            "abundancia": 0.0,
            "seguridad": 0.0,
            "cohesion": 0.0,
        },
        
        "peligro_latente": 0.0,
        "flags": set(),
        "historial": [],
    },
}


def obtener_region(nombre: str) -> dict:
    """Get a region by name. Returns a copy to avoid modifying the original."""
    if nombre not in REGIONES:
        raise ValueError(f"Region '{nombre}' not found")
    
    # Return a deep copy so modifications don't affect the template
    import copy
    return copy.deepcopy(REGIONES[nombre])
