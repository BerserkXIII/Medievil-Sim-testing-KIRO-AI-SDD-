"""
Linajes disponibles al inicio del juego.
Cada linaje sesga los stats iniciales y define tags narrativos.
"""

LINAJES = {
    "herrero": {
        "nombre": "Familia de herreros",
        "tags": ["artesano", "trabajador"],
        "modificadores_stats": {
            "constitucion": +2,
            "resistencia":  +1,
            "inteligencia": -1,
        },
        "habilidades_base": {"oficio": 3, "combate": 1},
        "riqueza_inicial": 0.35,
    },

    "campesino": {
        "nombre": "Familia campesina",
        "tags": ["humilde", "rural"],
        "modificadores_stats": {
            "constitucion": +1,
            "resistencia":  +2,
            "fe_innata":    +1,
        },
        "habilidades_base": {"oficio": 2},
        "riqueza_inicial": 0.2,
    },

    "clerigo": {
        "nombre": "Familia de clérigos",
        "tags": ["letrado", "devoto"],
        "modificadores_stats": {
            "inteligencia": +2,
            "fe_innata":    +2,
            "constitucion": -1,
        },
        "habilidades_base": {"conocimiento": 4},
        "riqueza_inicial": 0.3,
    },

    "mercader": {
        "nombre": "Familia mercader",
        "tags": ["viajero", "negociante"],
        "modificadores_stats": {
            "carisma":      +2,
            "inteligencia": +1,
            "resistencia":  -1,
        },
        "habilidades_base": {"oficio": 2, "conocimiento": 1},
        "riqueza_inicial": 0.55,
    },

    "soldado": {
        "nombre": "Familia de soldados",
        "tags": ["ex_militar", "frontera"],
        "modificadores_stats": {
            "constitucion": +2,
            "resistencia":  +2,
            "percepcion":   +1,
            "carisma":      -1,
            "fe_innata":    -1,
        },
        "habilidades_base": {"combate": 4, "sigilo": 1},
        "riqueza_inicial": 0.25,
    },

    "noble_caido": {
        "nombre": "Linaje noble venido a menos",
        "tags": ["noble", "caido", "orgulloso"],
        "modificadores_stats": {
            "carisma":      +2,
            "inteligencia": +1,
            "resistencia":  -2,
        },
        "habilidades_base": {"conocimiento": 2, "combate": 1},
        "riqueza_inicial": 0.15,  # noble pero arruinado
    },
}
