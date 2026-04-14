"""
Módulos narrativos del juego.
Cada módulo es un evento con condiciones, opciones y transformaciones.
Organizados por franja del día: mañana, mediodia, tarde, noche.
"""

MODULOS = [

    # -------------------------------------------------------------------------
    # MAÑANA
    # -------------------------------------------------------------------------

    {
        "id": "comer_bien",
        "franja": "mañana",
        "condiciones": {
            "riqueza": (0.5, 1.0),
            "disponibilidad_comida": (0.5, 1.0),
        },
        "texto": "Tu despensa está surtida. Puedes permitirte un buen desayuno.",
        "opciones": [
            {
                "texto_boton": "Comer bien",
                "transformaciones": {"nutricion": +0.35, "riqueza": -0.04},
                "texto_resultado": "Desayunas con calma. El día empieza con fuerza.",
            },
            {
                "texto_boton": "Comer frugal",
                "transformaciones": {"nutricion": +0.15},
                "texto_resultado": "Comes lo justo. Guardas el resto para después.",
            },
        ],
    },

    {
        "id": "comer_escaso",
        "franja": "mañana",
        "condiciones": {
            "nutricion": (0.0, 0.4),
            "disponibilidad_comida": (0.1, 0.5),
        },
        "texto": "Hay poco en la despensa. El hambre ya aprieta.",
        "opciones": [
            {
                "texto_boton": "Comer lo que hay",
                "transformaciones": {"nutricion": +0.15, "riqueza": -0.02},
                "texto_resultado": "No es suficiente, pero algo es algo.",
            },
            {
                "texto_boton": "Buscar comida fuera",
                "transformaciones": {"nutricion": +0.1, "heridas": +0.02, "descanso": -0.1},
                "texto_resultado": "Encuentras algo en el campo. El esfuerzo pasa factura.",
            },
        ],
    },

    {
        "id": "rezar_devoto",
        "franja": "mañana",
        "condiciones": {
            "fe": (0.5, 1.0),
            "flags_ausentes": ["excomulgado"],
        },
        "texto": "La mañana invita a la oración. Tu fe es firme.",
        "opciones": [
            {
                "texto_boton": "Rezar en casa",
                "transformaciones": {"fe": +0.05, "presion_social": -0.05},
                "texto_resultado": "La oración te da calma. El día pesa menos.",
            },
            {
                "texto_boton": "Ir a la iglesia",
                "transformaciones": {"fe": +0.08, "reputacion": +0.05, "presion_social": -0.08},
                "texto_resultado": "El cura te saluda. La comunidad te ve como uno de los suyos.",
            },
        ],
    },

    {
        "id": "rezar_sin_fe",
        "franja": "mañana",
        "condiciones": {
            "fe": (0.0, 0.3),
            "region": ["aldea", "ciudad"],
        },
        "texto": "El cura del pueblo te mira con insistencia. "
                 "Dicen que la vieja del bosque también tiene sus historias.",
        "opciones": [
            {
                "texto_boton": "Escuchar al cura",
                "transformaciones": {"fe": +0.08, "reputacion": +0.05, "presion_social": -0.04},
                "texto_resultado": "Sus palabras no te convencen del todo, "
                                   "pero la comunidad te ve bien.",
            },
            {
                "texto_boton": "Buscar a la vieja del bosque",
                "transformaciones": {
                    "fe": +0.06,
                    "reputacion": -0.08,
                    "flags_add": ["fe_heretica"],
                },
                "texto_resultado": "Sus historias son extrañas y fascinantes. "
                                   "Alguien te ha visto salir del bosque.",
            },
            {
                "texto_boton": "Ignorar ambos",
                "transformaciones": {"presion_social": +0.05},
                "texto_resultado": "No es asunto tuyo. Aunque el cura no lo olvida.",
            },
        ],
    },

    # -------------------------------------------------------------------------
    # MEDIODÍA
    # -------------------------------------------------------------------------

    {
        "id": "trabajar_oficio",
        "franja": "mediodia",
        "condiciones": {
            "condicion": (0.3, 1.0),  # necesitas estar en forma
        },
        "texto": "Es hora de trabajar. Tu oficio te espera.",
        "opciones": [
            {
                "texto_boton": "Trabajar duro",
                "transformaciones": {
                    "riqueza": +0.08,
                    "descanso": -0.15,
                    "nutricion": -0.05,
                    "reputacion": +0.03,
                },
                "texto_resultado": "Un día de trabajo duro. La bolsa pesa un poco más.",
            },
            {
                "texto_boton": "Trabajar lo justo",
                "transformaciones": {"riqueza": +0.04, "descanso": -0.07},
                "texto_resultado": "Haces lo necesario. Sin más.",
            },
        ],
    },

    {
        "id": "socializar_aldea",
        "franja": "mediodia",
        "condiciones": {
            "region": ["aldea", "ciudad"],
            "reputacion": (-0.3, 1.0),
        },
        "texto": "La plaza está animada. Hay gente con quien hablar.",
        "opciones": [
            {
                "texto_boton": "Charlar con vecinos",
                "transformaciones": {"reputacion": +0.04, "presion_social": -0.06},
                "texto_resultado": "Las noticias corren. Te sientes parte del lugar.",
            },
            {
                "texto_boton": "Escuchar rumores",
                "transformaciones": {"percepcion": +0.0, "peligro_percibido": +0.05},
                "texto_resultado": "Oyes cosas interesantes. No todas son buenas.",
            },
        ],
    },

    {
        "id": "recaudador",
        "franja": "mediodia",
        "condiciones": {
            "region": ["aldea", "ciudad"],
            "riqueza": (0.1, 1.0),
            "flags_ausentes": ["buscado"],
        },
        "texto": "Un recaudador del señor llega a la aldea. Exige el pago del diezmo.",
        "opciones": [
            {
                "texto_boton": "Pagar sin rechistar",
                "transformaciones": {"riqueza": -0.12, "lealtad": +0.08, "reputacion": +0.03},
                "texto_resultado": "Pagas. El recaudador asiente y sigue su camino.",
            },
            {
                "texto_boton": "Negociar",
                "transformaciones": {"riqueza": -0.05, "reputacion": -0.04, "peligro_latente": +0.1},
                "texto_resultado": "Consigues pagar menos. El recaudador no parece satisfecho.",
            },
            {
                "texto_boton": "Resistirse",
                "transformaciones": {
                    "peligro_percibido": +0.2,
                    "lealtad": -0.15,
                    "flags_add": ["buscado"],
                },
                "texto_resultado": "Te niegas. El recaudador se va, pero volverá con refuerzos.",
            },
        ],
    },

    # -------------------------------------------------------------------------
    # TARDE
    # -------------------------------------------------------------------------

    {
        "id": "descansar_tarde",
        "franja": "tarde",
        "condiciones": {},  # siempre disponible
        "texto": "La tarde avanza. Podrías tomarte un respiro.",
        "opciones": [
            {
                "texto_boton": "Descansar",
                "transformaciones": {"descanso": +0.2, "nutricion": -0.03},
                "texto_resultado": "Te tumbas un rato. El cuerpo lo agradece.",
            },
            {
                "texto_boton": "Seguir activo",
                "transformaciones": {"descanso": -0.1, "riqueza": +0.03},
                "texto_resultado": "Aprovechas la tarde. Cansado, pero productivo.",
            },
        ],
    },

    {
        "id": "cuidar_heridas",
        "franja": "tarde",
        "condiciones": {
            "heridas": (0.2, 1.0),
        },
        "texto": "Tus heridas necesitan atención. Si las ignoras, empeorarán.",
        "opciones": [
            {
                "texto_boton": "Curar las heridas",
                "transformaciones": {"heridas": -0.2, "riqueza": -0.05},
                "texto_resultado": "Limpias y vendas las heridas. Duele, pero mejora.",
            },
            {
                "texto_boton": "Ignorarlas",
                "transformaciones": {"heridas": +0.05, "peligro_latente": +0.05},
                "texto_resultado": "Las ignoras. Por ahora no empeoran... mucho.",
            },
        ],
    },

    # -------------------------------------------------------------------------
    # NOCHE
    # -------------------------------------------------------------------------

    {
        "id": "dormir_refugio",
        "franja": "noche",
        "condiciones": {
            "flags_ausentes": ["sin_refugio"],
        },
        "texto": "La noche cae. Tienes donde dormir.",
        "opciones": [
            {
                "texto_boton": "Dormir bien",
                "transformaciones": {"descanso": +0.4, "nutricion": -0.04},
                "texto_resultado": "Duermes profundamente. Mañana será otro día.",
            },
            {
                "texto_boton": "Dormir poco (madrugar)",
                "transformaciones": {"descanso": +0.2, "riqueza": +0.02},
                "texto_resultado": "Madrugas. Ganas tiempo, pierdes sueño.",
            },
        ],
    },

    {
        "id": "dormir_intemperie",
        "franja": "noche",
        "condiciones": {
            "flags_activos": ["sin_refugio"],
        },
        "texto": "No tienes donde dormir. La noche es fría.",
        "opciones": [
            {
                "texto_boton": "Buscar refugio improvisado",
                "transformaciones": {
                    "descanso": +0.15,
                    "heridas": +0.05,
                    "temperatura_corporal": -0.1,
                },
                "texto_resultado": "Encuentras un rincón. No es cómodo, pero sobrevives.",
            },
            {
                "texto_boton": "Pedir ayuda a un vecino",
                "transformaciones": {
                    "descanso": +0.25,
                    "reputacion": -0.05,
                    "presion_social": +0.08,
                },
                "texto_resultado": "Alguien te deja pasar la noche. Te debes un favor.",
            },
        ],
    },
]
