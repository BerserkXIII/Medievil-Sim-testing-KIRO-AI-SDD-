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

    # =========================================================================
    # MÓDULOS ADICIONALES: Comercio, religión, conflicto, etc
    # =========================================================================

    {
        "id": "mercader_ambulante",
        "franja": "mediodia",
        "condiciones": {
            "region": ["puerto_costero", "ciudad_amurallada", "aldea_agricola"],
        },
        "texto": "Un mercader ambulante te ofrece sus wares.",
        "opciones": [
            {
                "texto_boton": "Comprar algo útil",
                "transformaciones": {"riqueza": -0.08, "nutricion": +0.1},
                "texto_resultado": "Compras comida y suministros. Buen negocio.",
            },
            {
                "texto_boton": "Ignorar",
                "transformaciones": {},
                "texto_resultado": "Continúas tu camino.",
            },
        ],
    },

    {
        "id": "sacerdote_confesion",
        "franja": "tarde",
        "condiciones": {
            "region": ["aldea_agricola", "ciudad_amurallada"],
            "fe": (0.3, 1.0),
        },
        "texto": "El sacerdote te invita a confesarte.",
        "opciones": [
            {
                "texto_boton": "Confesarse",
                "transformaciones": {"fe": +0.1, "presion_social": -0.1},
                "texto_resultado": "Te sientes en paz. La comunidad te ve bien.",
            },
            {
                "texto_boton": "Declinar",
                "transformaciones": {"presion_social": +0.05},
                "texto_resultado": "El sacerdote frunce el ceño.",
            },
        ],
    },

    {
        "id": "taberna_noticias",
        "franja": "tarde",
        "condiciones": {
            "region": ["puerto_costero", "ciudad_amurallada"],
            "riqueza": (0.1, 1.0),
        },
        "texto": "En la taberna, los viajeros comparten historias.",
        "opciones": [
            {
                "texto_boton": "Beber y escuchar",
                "transformaciones": {"riqueza": -0.05, "reputacion": +0.05},
                "texto_resultado": "Oyes historias interesantes. Te haces amigos.",
            },
            {
                "texto_boton": "Jugar a los dados",
                "transformaciones": {"riqueza": +0.1},
                "texto_resultado": "¡Tienes suerte! Ganas dinero.",
            },
        ],
    },

    {
        "id": "trabajo_temporal",
        "franja": "mediodia",
        "condiciones": {
            "condicion": (0.3, 1.0),
            "region": ["puerto_costero", "ciudad_amurallada", "aldea_agricola"],
        },
        "texto": "Hay trabajo temporal disponible.",
        "opciones": [
            {
                "texto_boton": "Trabajar duro",
                "transformaciones": {"riqueza": +0.12, "descanso": -0.2},
                "texto_resultado": "Trabajas todo el día. Ganas buen dinero.",
            },
            {
                "texto_boton": "Trabajar poco",
                "transformaciones": {"riqueza": +0.05, "descanso": -0.08},
                "texto_resultado": "Haces algo de trabajo. Poco dinero.",
            },
        ],
    },

    {
        "id": "cazador_bosque",
        "franja": "mediodia",
        "condiciones": {
            "region": ["bosque_denso", "montaña_rocosa"],
        },
        "texto": "Un cazador te invita a cazar.",
        "opciones": [
            {
                "texto_boton": "Cazar",
                "transformaciones": {"nutricion": +0.2, "heridas": +0.08},
                "texto_resultado": "Cazas un animal. Consigues comida, pero te hieres.",
            },
            {
                "texto_boton": "Declinar",
                "transformaciones": {},
                "texto_resultado": "Prefieres no arriesgarte.",
            },
        ],
    },

    {
        "id": "ermitano_sabiduria",
        "franja": "tarde",
        "condiciones": {
            "region": ["montaña_rocosa", "bosque_denso"],
        },
        "texto": "Un ermitaño te ofrece enseñanzas.",
        "opciones": [
            {
                "texto_boton": "Aprender",
                "transformaciones": {"presion_social": -0.1, "fe": +0.05},
                "texto_resultado": "Aprendes cosas sobre la vida. Te sientes más sabio.",
            },
            {
                "texto_boton": "Ignorar",
                "transformaciones": {},
                "texto_resultado": "Continúas tu camino.",
            },
        ],
    },

    {
        "id": "enfermedad_leve",
        "franja": "mañana",
        "condiciones": {
            "salud_fisica": (0.2, 0.5),
        },
        "texto": "Te despiertas con fiebre leve.",
        "opciones": [
            {
                "texto_boton": "Descansar",
                "transformaciones": {"descanso": +0.2, "nutricion": -0.05},
                "texto_resultado": "Descansas. La fiebre baja.",
            },
            {
                "texto_boton": "Ignorar y continuar",
                "transformaciones": {"heridas": +0.1},
                "texto_resultado": "Ignoras la fiebre. Empeora.",
            },
        ],
    },

    {
        "id": "nobleza_encuentro",
        "franja": "mediodia",
        "condiciones": {
            "region": ["ciudad_amurallada"],
            "reputacion": (0.5, 1.0),
        },
        "texto": "Un noble te reconoce en la calle.",
        "opciones": [
            {
                "texto_boton": "Saludar respetuosamente",
                "transformaciones": {"reputacion": +0.1, "lealtad": +0.05},
                "texto_resultado": "El noble te saluda. Tu reputación sube.",
            },
            {
                "texto_boton": "Ignorar",
                "transformaciones": {"reputacion": -0.1},
                "texto_resultado": "El noble se ofende.",
            },
        ],
    },

    {
        "id": "pordiosero_caridad",
        "franja": "tarde",
        "condiciones": {
            "riqueza": (0.3, 1.0),
        },
        "texto": "Un pordiosero te pide limosna.",
        "opciones": [
            {
                "texto_boton": "Dar dinero",
                "transformaciones": {"riqueza": -0.05, "reputacion": +0.08},
                "texto_resultado": "Das dinero. Te sientes bien. La gente lo nota.",
            },
            {
                "texto_boton": "Rechazar",
                "transformaciones": {"reputacion": -0.05},
                "texto_resultado": "Rechazas. El pordiosero te maldice.",
            },
        ],
    },

    {
        "id": "guardia_control",
        "franja": "mediodia",
        "condiciones": {
            "region": ["ciudad_amurallada", "puerto_costero"],
            "flags_ausentes": ["buscado"],
        },
        "texto": "Un guardia te detiene para un control.",
        "opciones": [
            {
                "texto_boton": "Cooperar",
                "transformaciones": {"presion_social": -0.05},
                "texto_resultado": "Cooperas. El guardia te deja pasar.",
            },
            {
                "texto_boton": "Ser desafiante",
                "transformaciones": {"peligro_percibido": +0.2, "reputacion": -0.1},
                "texto_resultado": "El guardia se molesta. Mejor no insistir.",
            },
        ],
    },

    {
        "id": "viajero_compania",
        "franja": "tarde",
        "condiciones": {
            "presion_social": (0.0, 0.5),
        },
        "texto": "Un viajero solitario busca compañía.",
        "opciones": [
            {
                "texto_boton": "Acompañarlo",
                "transformaciones": {"presion_social": -0.1, "reputacion": +0.05},
                "texto_resultado": "Compartes historias. El viaje es menos tedioso.",
            },
            {
                "texto_boton": "Declinar",
                "transformaciones": {},
                "texto_resultado": "Prefieres estar solo.",
            },
        ],
    },

    {
        "id": "cosecha_ayuda",
        "franja": "mediodia",
        "condiciones": {
            "region": ["aldea_agricola"],
            "condicion": (0.5, 1.0),
        },
        "texto": "Los aldeanos necesitan ayuda con la cosecha.",
        "opciones": [
            {
                "texto_boton": "Ayudar",
                "transformaciones": {"reputacion": +0.15, "descanso": -0.15},
                "texto_resultado": "Ayudas con la cosecha. Te ganas su gratitud.",
            },
            {
                "texto_boton": "Declinar",
                "transformaciones": {"reputacion": -0.05},
                "texto_resultado": "Los aldeanos se decepcionan.",
            },
        ],
    },

    {
        "id": "tormenta_refugio",
        "franja": "tarde",
        "condiciones": {
            "clima_region": (0.0, 0.3),
        },
        "texto": "Una tormenta se aproxima.",
        "opciones": [
            {
                "texto_boton": "Buscar refugio",
                "transformaciones": {"descanso": +0.1, "temperatura_corporal": +0.1},
                "texto_resultado": "Encuentras refugio. La tormenta pasa.",
            },
            {
                "texto_boton": "Continuar",
                "transformaciones": {"heridas": +0.1, "temperatura_corporal": -0.2},
                "texto_resultado": "La tormenta te golpea. Resultas mojado y herido.",
            },
        ],
    },
]
