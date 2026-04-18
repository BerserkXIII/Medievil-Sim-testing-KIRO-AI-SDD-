"""
Módulos narrativos del juego.
Cada módulo es un evento con condiciones, opciones y transformaciones.
Organizados por franja del día: mañana, mediodia, tarde, noche.

Estructura:
- Módulos básicos: eventos simples sin progresión
- Módulos de misión: eventos con flags que crean progresión
- Módulos híbridos: simples sin flags, complejos si flags activos
"""

MODULOS = [

    # =========================================================================
    # MÓDULOS BÁSICOS ORIGINALES
    # =========================================================================

    {
        "id": "comer_bien",
        "franja": "mañana",
        "categoria": "comer",
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
        "categoria": "comer",
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
        "categoria": "rezar",
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
        "categoria": "rezar",
        "condiciones": {
            "fe": (0.0, 0.3),
        },
        "texto": "El cura del pueblo te mira con insistencia. Dicen que la vieja del bosque también tiene sus historias.",
        "opciones": [
            {
                "texto_boton": "Escuchar al cura",
                "transformaciones": {"fe": +0.08, "reputacion": +0.05, "presion_social": -0.04},
                "texto_resultado": "Sus palabras no te convencen del todo, pero la comunidad te ve bien.",
            },
            {
                "texto_boton": "Buscar a la vieja del bosque",
                "transformaciones": {
                    "fe": +0.06,
                    "reputacion": -0.08,
                    "flags_add": ["fe_heretica"],
                },
                "texto_resultado": "Sus historias son extrañas y fascinantes. Alguien te ha visto salir del bosque.",
            },
            {
                "texto_boton": "Ignorar ambos",
                "transformaciones": {"presion_social": +0.05},
                "texto_resultado": "No es asunto tuyo. Aunque el cura no lo olvida.",
            },
        ],
    },

    {
        "id": "trabajar_oficio",
        "franja": "mediodia",
        "categoria": "trabajar",
        "condiciones": {
            "condicion": (0.3, 1.0),
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
        "id": "descansar_tarde",
        "franja": "tarde",
        "categoria": "descansar",
        "condiciones": {},
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
        "id": "dormir_refugio",
        "franja": "noche",
        "categoria": "descansar",
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
        "categoria": "descansar",
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
    # MÓDULOS FALLBACK (garantizados, sin condiciones restrictivas)
    # =========================================================================

    {
        "id": "comer_fallback",
        "franja": "mañana",
        "categoria": "comer",
        "condiciones": {},
        "texto": "Tienes hambre. Necesitas comer algo.",
        "opciones": [
            {
                "texto_boton": "Comer algo simple",
                "transformaciones": {"nutricion": +0.2},
                "texto_resultado": "Comes lo que encuentras. Es suficiente.",
            },
            {
                "texto_boton": "Saltarse el desayuno",
                "transformaciones": {"descanso": +0.05},
                "texto_resultado": "Decides no comer. Tienes más tiempo.",
            },
        ],
    },

    {
        "id": "trabajar_fallback",
        "franja": "mediodia",
        "categoria": "trabajar",
        "condiciones": {},
        "texto": "Es mediodía. Podrías hacer algo productivo.",
        "opciones": [
            {
                "texto_boton": "Trabajar un poco",
                "transformaciones": {"riqueza": +0.05, "descanso": -0.08},
                "texto_resultado": "Trabajas sin prisa. Ganas algo de dinero.",
            },
            {
                "texto_boton": "Descansar",
                "transformaciones": {"descanso": +0.1},
                "texto_resultado": "Prefieres descansar. El trabajo puede esperar.",
            },
        ],
    },

    {
        "id": "descansar_fallback",
        "franja": "tarde",
        "categoria": "descansar",
        "condiciones": {},
        "texto": "La tarde avanza. Tu cuerpo pide descanso.",
        "opciones": [
            {
                "texto_boton": "Descansar un rato",
                "transformaciones": {"descanso": +0.15},
                "texto_resultado": "Te relajas. El cuerpo lo agradece.",
            },
            {
                "texto_boton": "Seguir activo",
                "transformaciones": {"riqueza": +0.02, "descanso": -0.05},
                "texto_resultado": "Sigues trabajando. Cansado, pero productivo.",
            },
        ],
    },

    {
        "id": "reflexion_fallback",
        "franja": "noche",
        "categoria": "otro",
        "condiciones": {},
        "texto": "La noche es tranquila. Tienes tiempo para pensar.",
        "opciones": [
            {
                "texto_boton": "Reflexionar sobre el día",
                "transformaciones": {"presion_social": -0.05},
                "texto_resultado": "Reflexionas. El día ha sido largo.",
            },
            {
                "texto_boton": "Dormir sin pensar",
                "transformaciones": {"descanso": +0.2},
                "texto_resultado": "Te duermes rápido. Mañana será otro día.",
            },
        ],
    },

    # =========================================================================
    # LÍNEA DE MISIÓN: IGLESIA (7 módulos con progresión)
    # =========================================================================

    {
        "id": "mision_iglesia_oferta",
        "franja": "mañana",
        "categoria": "misiones",
        "condiciones": {
            "fe": (0.4, 1.0),
            "flags_ausentes": ["mision_iglesia_activa", "mision_iglesia_rechazada"],
        },
        "texto": "El cura te pide que recolectes limosnas para los pobres. Es una obra de caridad.",
        "opciones": [
            {
                "texto_boton": "Aceptar la misión",
                "transformaciones": {
                    "flags_add": ["mision_iglesia_activa"],
                    "presion_social": -0.05,
                    "fe": +0.05,
                },
                "texto_resultado": "El cura te bendice. Tienes 3 días para recolectar limosnas.",
            },
            {
                "texto_boton": "Rechazar",
                "transformaciones": {
                    "flags_add": ["mision_iglesia_rechazada"],
                    "reputacion": -0.1,
                    "presion_social": +0.1,
                },
                "texto_resultado": "El cura frunce el ceño. La comunidad lo nota.",
            },
        ],
    },

    {
        "id": "mision_iglesia_progreso_bien",
        "franja": "mediodia",
        "categoria": "misiones",
        "condiciones": {
            "flags_activos": ["mision_iglesia_activa"],
            "riqueza": (0.3, 1.0),
        },
        "texto": "Mientras recolectas limosnas, encuentras a una viuda pobre. Puedes ayudarla.",
        "opciones": [
            {
                "texto_boton": "Dar dinero a la viuda",
                "transformaciones": {
                    "riqueza": -0.1,
                    "flags_add": ["mision_iglesia_compasion"],
                    "fe": +0.08,
                },
                "texto_resultado": "La viuda te bendice. Sientes que haces lo correcto.",
            },
            {
                "texto_boton": "Seguir recolectando",
                "transformaciones": {
                    "riqueza": +0.05,
                },
                "texto_resultado": "Continúas recolectando. Más dinero, menos compasión.",
            },
        ],
    },

    {
        "id": "mision_iglesia_progreso_mal",
        "franja": "tarde",
        "categoria": "misiones",
        "condiciones": {
            "flags_activos": ["mision_iglesia_activa"],
            "flags_ausentes": ["mision_iglesia_compasion"],
        },
        "texto": "Mientras recolectas, ves a un borracho que necesita ayuda. Nadie lo mira.",
        "opciones": [
            {
                "texto_boton": "Ignorar y seguir",
                "transformaciones": {
                    "riqueza": +0.03,
                    "flags_add": ["mision_iglesia_egoista"],
                },
                "texto_resultado": "Recolectas más dinero. Pero algo te molesta.",
            },
            {
                "texto_boton": "Ayudar al borracho",
                "transformaciones": {
                    "riqueza": -0.05,
                    "flags_add": ["mision_iglesia_compasion"],
                    "fe": +0.06,
                },
                "texto_resultado": "Lo ayudas. Sientes que es lo correcto.",
            },
        ],
    },

    {
        "id": "mision_iglesia_entrega",
        "franja": "mediodia",
        "categoria": "misiones",
        "condiciones": {
            "flags_activos": ["mision_iglesia_activa"],
        },
        "texto": "Es hora de entregar las limosnas al cura.",
        "opciones": [
            {
                "texto_boton": "Entregar todo",
                "transformaciones": {
                    "flags_remove": ["mision_iglesia_activa"],
                    "flags_add": ["mision_iglesia_completada"],
                    "reputacion": +0.15,
                    "fe": +0.1,
                },
                "texto_resultado": "El cura te felicita. La comunidad te ve como un santo.",
            },
            {
                "texto_boton": "Quedarte con parte",
                "transformaciones": {
                    "flags_remove": ["mision_iglesia_activa"],
                    "flags_add": ["mision_iglesia_traicion"],
                    "riqueza": +0.1,
                    "reputacion": -0.2,
                },
                "texto_resultado": "El cura descubre tu engaño. Te mira con desprecio.",
            },
        ],
    },

    {
        "id": "mision_iglesia_consecuencia_bien",
        "franja": "mañana",
        "categoria": "misiones",
        "condiciones": {
            "flags_activos": ["mision_iglesia_completada", "mision_iglesia_compasion"],
        },
        "texto": "El cura te ofrece un trabajo permanente en la iglesia.",
        "opciones": [
            {
                "texto_boton": "Aceptar",
                "transformaciones": {
                    "flags_add": ["trabajo_iglesia"],
                    "fe": +0.1,
                    "reputacion": +0.1,
                },
                "texto_resultado": "Ahora trabajas para la iglesia. Tu vida tiene propósito.",
            },
            {
                "texto_boton": "Declinar",
                "transformaciones": {
                    "reputacion": -0.05,
                },
                "texto_resultado": "El cura se decepciona, pero respeta tu decisión.",
            },
        ],
    },

    {
        "id": "mision_iglesia_consecuencia_mal",
        "franja": "tarde",
        "categoria": "misiones",
        "condiciones": {
            "flags_activos": ["mision_iglesia_traicion"],
        },
        "texto": "El cura te evita. La comunidad murmura sobre ti.",
        "opciones": [
            {
                "texto_boton": "Intentar redimirte",
                "transformaciones": {
                    "flags_add": ["mision_iglesia_redencion"],
                    "reputacion": -0.1,
                    "fe": +0.05,
                },
                "texto_resultado": "Pides perdón. El cura es escéptico, pero te da una oportunidad.",
            },
            {
                "texto_boton": "Ignorar",
                "transformaciones": {
                    "presion_social": +0.15,
                },
                "texto_resultado": "La comunidad te rechaza. Te sientes solo.",
            },
        ],
    },

    {
        "id": "mision_iglesia_redencion_final",
        "franja": "mediodia",
        "categoria": "misiones",
        "condiciones": {
            "flags_activos": ["mision_iglesia_redencion"],
        },
        "texto": "El cura te da una segunda oportunidad: ayudar a los enfermos.",
        "opciones": [
            {
                "texto_boton": "Aceptar",
                "transformaciones": {
                    "flags_remove": ["mision_iglesia_traicion"],
                    "flags_add": ["mision_iglesia_redimido"],
                    "reputacion": +0.1,
                    "fe": +0.1,
                },
                "texto_resultado": "Trabajas con los enfermos. Lentamente, recuperas tu honor.",
            },
            {
                "texto_boton": "Rechazar",
                "transformaciones": {
                    "reputacion": -0.15,
                },
                "texto_resultado": "El cura pierde la paciencia. Eres un paria.",
            },
        ],
    },

    # =========================================================================
    # LÍNEA DE MISIÓN: NOBLEZA (7 módulos con progresión)
    # =========================================================================

    {
        "id": "mision_nobleza_oferta",
        "franja": "mediodia",
        "categoria": "misiones",
        "condiciones": {
            "region": ["ciudad_amurallada"],
            "reputacion": (0.4, 1.0),
            "flags_ausentes": ["mision_nobleza_activa", "mision_nobleza_rechazada"],
        },
        "texto": "Un noble te aborda en la plaza. Necesita alguien de confianza para un trabajo.",
        "opciones": [
            {
                "texto_boton": "Aceptar",
                "transformaciones": {
                    "flags_add": ["mision_nobleza_activa"],
                    "lealtad": +0.1,
                    "reputacion": +0.05,
                },
                "texto_resultado": "El noble te contrata. Trabajarás en el castillo.",
            },
            {
                "texto_boton": "Rechazar",
                "transformaciones": {
                    "flags_add": ["mision_nobleza_rechazada"],
                    "reputacion": -0.1,
                },
                "texto_resultado": "El noble se ofende. Mejor no enemistarse con la nobleza.",
            },
        ],
    },

    {
        "id": "mision_nobleza_trabajo_leal",
        "franja": "mediodia",
        "categoria": "misiones",
        "condiciones": {
            "flags_activos": ["mision_nobleza_activa"],
        },
        "texto": "El noble te pide que espíes a su rival político.",
        "opciones": [
            {
                "texto_boton": "Espiar lealmente",
                "transformaciones": {
                    "flags_add": ["mision_nobleza_leal"],
                    "lealtad": +0.1,
                    "reputacion": +0.08,
                },
                "texto_resultado": "Reúnes información. El noble está satisfecho.",
            },
            {
                "texto_boton": "Negarse",
                "transformaciones": {
                    "flags_add": ["mision_nobleza_rebelde"],
                    "lealtad": -0.1,
                    "reputacion": +0.05,
                },
                "texto_resultado": "Te niegas. El noble no está contento, pero respeta tu integridad.",
            },
        ],
    },

    {
        "id": "mision_nobleza_traicion",
        "franja": "tarde",
        "categoria": "misiones",
        "condiciones": {
            "flags_activos": ["mision_nobleza_leal"],
        },
        "texto": "El rival del noble te ofrece dinero por traicionar a tu patrón.",
        "opciones": [
            {
                "texto_boton": "Mantener lealtad",
                "transformaciones": {
                    "flags_add": ["mision_nobleza_fiel"],
                    "lealtad": +0.15,
                },
                "texto_resultado": "Rechazas la oferta. Tu honor permanece intacto.",
            },
            {
                "texto_boton": "Traicionar",
                "transformaciones": {
                    "flags_remove": ["mision_nobleza_leal"],
                    "flags_add": ["mision_nobleza_traidor"],
                    "riqueza": +0.2,
                    "lealtad": -0.2,
                },
                "texto_resultado": "Aceptas el dinero. Pero sabes que esto tendrá consecuencias.",
            },
        ],
    },

    {
        "id": "mision_nobleza_consecuencia_fiel",
        "franja": "mediodia",
        "categoria": "misiones",
        "condiciones": {
            "flags_activos": ["mision_nobleza_fiel"],
        },
        "texto": "El noble te recompensa por tu lealtad.",
        "opciones": [
            {
                "texto_boton": "Aceptar recompensa",
                "transformaciones": {
                    "flags_remove": ["mision_nobleza_activa"],
                    "flags_add": ["mision_nobleza_completada"],
                    "riqueza": +0.2,
                    "reputacion": +0.15,
                },
                "texto_resultado": "Recibes oro y reconocimiento. Tu lealtad fue recompensada.",
            },
        ],
    },

    {
        "id": "mision_nobleza_consecuencia_traidor",
        "franja": "tarde",
        "categoria": "misiones",
        "condiciones": {
            "flags_activos": ["mision_nobleza_traidor"],
        },
        "texto": "El noble descubre tu traición.",
        "opciones": [
            {
                "texto_boton": "Huir",
                "transformaciones": {
                    "flags_remove": ["mision_nobleza_activa"],
                    "flags_add": ["buscado_nobleza"],
                    "peligro_percibido": +0.3,
                },
                "texto_resultado": "Huyes. Ahora eres un fugitivo de la nobleza.",
            },
            {
                "texto_boton": "Enfrentarlo",
                "transformaciones": {
                    "flags_remove": ["mision_nobleza_activa"],
                    "flags_add": ["enemigo_nobleza"],
                    "heridas": +0.2,
                    "reputacion": -0.3,
                },
                "texto_resultado": "El noble te golpea. Eres su enemigo declarado.",
            },
        ],
    },

    {
        "id": "mision_nobleza_rebelde_final",
        "franja": "mediodia",
        "categoria": "misiones",
        "condiciones": {
            "flags_activos": ["mision_nobleza_rebelde"],
        },
        "texto": "El noble respeta tu negativa. Te ofrece un trabajo honesto.",
        "opciones": [
            {
                "texto_boton": "Aceptar",
                "transformaciones": {
                    "flags_remove": ["mision_nobleza_activa"],
                    "flags_add": ["trabajo_nobleza_honesto"],
                    "reputacion": +0.1,
                    "riqueza": +0.1,
                },
                "texto_resultado": "Trabajas honestamente para la nobleza. Ganas respeto.",
            },
            {
                "texto_boton": "Declinar",
                "transformaciones": {
                    "flags_remove": ["mision_nobleza_activa"],
                    "reputacion": +0.05,
                },
                "texto_resultado": "Te vas. Al menos no eres su enemigo.",
            },
        ],
    },

    # =========================================================================
    # LÍNEA DE MISIÓN: GREMIOS (7 módulos con progresión)
    # =========================================================================

    {
        "id": "mision_gremio_oferta",
        "franja": "mediodia",
        "categoria": "misiones",
        "condiciones": {
            "region": ["ciudad_amurallada", "puerto_costero"],
            "condicion": (0.5, 1.0),
            "flags_ausentes": ["mision_gremio_activa", "mision_gremio_rechazada"],
        },
        "texto": "Un maestro gremial te ofrece aprender un oficio valioso.",
        "opciones": [
            {
                "texto_boton": "Aceptar aprendizaje",
                "transformaciones": {
                    "flags_add": ["mision_gremio_activa"],
                    "reputacion": +0.05,
                    "descanso": -0.1,
                },
                "texto_resultado": "Comienzas tu aprendizaje. Será duro, pero valdrá la pena.",
            },
            {
                "texto_boton": "Rechazar",
                "transformaciones": {
                    "flags_add": ["mision_gremio_rechazada"],
                    "reputacion": -0.05,
                },
                "texto_resultado": "El maestro se decepciona. Pierdes una oportunidad.",
            },
        ],
    },

    {
        "id": "mision_gremio_aprendizaje",
        "franja": "mediodia",
        "categoria": "misiones",
        "condiciones": {
            "flags_activos": ["mision_gremio_activa"],
        },
        "texto": "El maestro te enseña los secretos del oficio.",
        "opciones": [
            {
                "texto_boton": "Aprender bien",
                "transformaciones": {
                    "flags_add": ["mision_gremio_dedicado"],
                    "descanso": -0.15,
                    "riqueza": +0.05,
                },
                "texto_resultado": "Aprendes rápido. El maestro está impresionado.",
            },
            {
                "texto_boton": "Aprender lentamente",
                "transformaciones": {
                    "flags_add": ["mision_gremio_lento"],
                    "descanso": -0.05,
                },
                "texto_resultado": "Aprendes, pero sin prisa. El maestro es paciente.",
            },
        ],
    },

    {
        "id": "mision_gremio_competencia",
        "franja": "tarde",
        "categoria": "misiones",
        "condiciones": {
            "flags_activos": ["mision_gremio_dedicado"],
        },
        "texto": "Otro aprendiz te desafía a una competencia de habilidad.",
        "opciones": [
            {
                "texto_boton": "Competir honestamente",
                "transformaciones": {
                    "flags_add": ["mision_gremio_honesto"],
                    "reputacion": +0.1,
                },
                "texto_resultado": "Compites limpiamente. Ganas respeto, aunque pierdas.",
            },
            {
                "texto_boton": "Sabotear al rival",
                "transformaciones": {
                    "flags_add": ["mision_gremio_traidor"],
                    "riqueza": +0.1,
                    "reputacion": -0.15,
                },
                "texto_resultado": "Ganas, pero de forma deshonesta. Alguien lo vio.",
            },
        ],
    },

    {
        "id": "mision_gremio_maestria",
        "franja": "mediodia",
        "categoria": "misiones",
        "condiciones": {
            "flags_activos": ["mision_gremio_honesto"],
        },
        "texto": "El maestro te reconoce como oficial del gremio.",
        "opciones": [
            {
                "texto_boton": "Aceptar",
                "transformaciones": {
                    "flags_remove": ["mision_gremio_activa"],
                    "flags_add": ["oficial_gremio"],
                    "riqueza": +0.15,
                    "reputacion": +0.2,
                },
                "texto_resultado": "Eres oficial. Tu futuro está asegurado.",
            },
        ],
    },

    {
        "id": "mision_gremio_expulsion",
        "franja": "tarde",
        "categoria": "misiones",
        "condiciones": {
            "flags_activos": ["mision_gremio_traidor"],
        },
        "texto": "El maestro descubre tu sabotaje.",
        "opciones": [
            {
                "texto_boton": "Pedir perdón",
                "transformaciones": {
                    "flags_remove": ["mision_gremio_activa"],
                    "flags_add": ["expulsado_gremio"],
                    "reputacion": -0.2,
                },
                "texto_resultado": "Te expulsan del gremio. Tu reputación está arruinada.",
            },
            {
                "texto_boton": "Huir",
                "transformaciones": {
                    "flags_remove": ["mision_gremio_activa"],
                    "flags_add": ["fugitivo_gremio"],
                    "peligro_percibido": +0.2,
                },
                "texto_resultado": "Huyes. El gremio te busca.",
            },
        ],
    },

    {
        "id": "mision_gremio_lento_final",
        "franja": "mediodia",
        "categoria": "misiones",
        "condiciones": {
            "flags_activos": ["mision_gremio_lento"],
        },
        "texto": "Después de mucho tiempo, finalmente dominas el oficio.",
        "opciones": [
            {
                "texto_boton": "Convertirse en oficial",
                "transformaciones": {
                    "flags_remove": ["mision_gremio_activa"],
                    "flags_add": ["oficial_gremio_lento"],
                    "riqueza": +0.1,
                    "reputacion": +0.1,
                },
                "texto_resultado": "Eres oficial. Tardaste, pero lo lograste.",
            },
        ],
    },

    # =========================================================================
    # MÓDULOS BÁSICOS MEJORADOS (15 módulos híbridos con tweaks)
    # =========================================================================

    {
        "id": "comer_mercado",
        "franja": "mediodia",
        "categoria": "comer",
        "condiciones": {
            "region": ["puerto_costero", "ciudad_amurallada"],
        },
        "texto": "El mercado está lleno de vendedores. Hay comida fresca.",
        "opciones": [
            {
                "texto_boton": "Comprar comida cara",
                "transformaciones": {
                    "nutricion": +0.3,
                    "riqueza": -0.1,
                    "reputacion": +0.02,
                },
                "texto_resultado": "Compras lo mejor. El vendedor te sonríe.",
            },
            {
                "texto_boton": "Comprar comida barata",
                "transformaciones": {
                    "nutricion": +0.15,
                    "riqueza": -0.03,
                },
                "texto_resultado": "Compras lo que puedes. Es suficiente.",
            },
            {
                "texto_boton": "Robar comida",
                "transformaciones": {
                    "nutricion": +0.2,
                    "flags_add": ["ladroncillo"],
                    "peligro_percibido": +0.1,
                },
                "texto_resultado": "Robas algo. Nadie te ve... o eso crees.",
            },
        ],
    },

    {
        "id": "rezar_crisis_fe",
        "franja": "tarde",
        "categoria": "rezar",
        "condiciones": {
            "salud_mental": (0.0, 0.4),
        },
        "texto": "Te sientes perdido. La fe podría ayudarte.",
        "opciones": [
            {
                "texto_boton": "Rezar desesperadamente",
                "transformaciones": {
                    "fe": +0.15,
                    "salud_mental": +0.2,
                    "presion_social": -0.1,
                },
                "texto_resultado": "La oración te calma. Sientes que alguien te escucha.",
            },
            {
                "texto_boton": "Buscar consuelo en la bebida",
                "transformaciones": {
                    "riqueza": -0.05,
                    "salud_mental": +0.1,
                    "nutricion": -0.05,
                },
                "texto_resultado": "Bebes. Temporal, pero efectivo.",
            },
        ],
    },

    {
        "id": "trabajar_peligroso",
        "franja": "mediodia",
        "categoria": "trabajar",
        "condiciones": {
            "condicion": (0.6, 1.0),
            "flags_ausentes": ["trabajo_iglesia", "trabajo_nobleza_honesto"],
        },
        "texto": "Hay trabajo peligroso pero bien pagado.",
        "opciones": [
            {
                "texto_boton": "Aceptar el riesgo",
                "transformaciones": {
                    "riqueza": +0.15,
                    "heridas": +0.1,
                    "reputacion": +0.05,
                },
                "texto_resultado": "Ganas mucho dinero, pero te hieres.",
            },
            {
                "texto_boton": "Buscar trabajo seguro",
                "transformaciones": {
                    "riqueza": +0.05,
                    "descanso": -0.08,
                },
                "texto_resultado": "Trabajas sin riesgos. Menos dinero, más paz.",
            },
        ],
    },

    {
        "id": "socializar_taberna",
        "franja": "tarde",
        "categoria": "otro",
        "condiciones": {
            "riqueza": (0.2, 1.0),
            "region": ["puerto_costero", "ciudad_amurallada"],
        },
        "texto": "La taberna está llena de gente interesante.",
        "opciones": [
            {
                "texto_boton": "Beber y charlar",
                "transformaciones": {
                    "riqueza": -0.05,
                    "reputacion": +0.08,
                    "presion_social": -0.1,
                },
                "texto_resultado": "Haces amigos. La noche es divertida.",
            },
            {
                "texto_boton": "Jugar a los dados",
                "transformaciones": {
                    "riqueza": +0.1,
                },
                "texto_resultado": "¡Tienes suerte! Ganas dinero.",
            },
            {
                "texto_boton": "Pelear",
                "transformaciones": {
                    "heridas": +0.15,
                    "reputacion": -0.1,
                    "peligro_percibido": +0.1,
                },
                "texto_resultado": "Te metes en una pelea. Resultas herido.",
            },
        ],
    },

    {
        "id": "cuidar_heridas_profundas",
        "franja": "tarde",
        "categoria": "descansar",
        "condiciones": {
            "heridas": (0.5, 1.0),
        },
        "texto": "Tus heridas son graves. Necesitan atención urgente.",
        "opciones": [
            {
                "texto_boton": "Ir al sanador",
                "transformaciones": {
                    "heridas": -0.3,
                    "riqueza": -0.15,
                    "salud_fisica": +0.1,
                },
                "texto_resultado": "El sanador te cura. Caro, pero efectivo.",
            },
            {
                "texto_boton": "Curarte solo",
                "transformaciones": {
                    "heridas": -0.1,
                    "salud_fisica": -0.05,
                },
                "texto_resultado": "Te curas como puedes. Mejora lentamente.",
            },
        ],
    },

    {
        "id": "encuentro_bandidos_camino",
        "franja": "mediodia",
        "categoria": "otro",
        "condiciones": {
            "peligro_latente": (0.5, 1.0),
            "flags_ausentes": ["buscado"],
        },
        "texto": "En el camino, ves a unos bandidos.",
        "opciones": [
            {
                "texto_boton": "Evitarlos",
                "transformaciones": {
                    "descanso": -0.1,
                },
                "texto_resultado": "Logras evitarlos. Pero pierdes tiempo.",
            },
            {
                "texto_boton": "Enfrentarlos",
                "transformaciones": {
                    "heridas": +0.2,
                    "riqueza": -0.1,
                    "reputacion": +0.1,
                },
                "texto_resultado": "Luchas. Ganas, pero resultas herido.",
            },
        ],
    },

    {
        "id": "enfermedad_epidemia",
        "franja": "mañana",
        "categoria": "descansar",
        "condiciones": {
            "epidemia_activa": (0.5, 1.0),
        },
        "texto": "Hay una epidemia en la región. Muchos están enfermos.",
        "opciones": [
            {
                "texto_boton": "Ayudar a los enfermos",
                "transformaciones": {
                    "heridas": +0.1,
                    "reputacion": +0.15,
                    "fe": +0.05,
                },
                "texto_resultado": "Ayudas. Te expones, pero ganas respeto.",
            },
            {
                "texto_boton": "Evitar el contacto",
                "transformaciones": {
                    "presion_social": +0.1,
                    "reputacion": -0.05,
                },
                "texto_resultado": "Te proteges. Pero la comunidad te juzga.",
            },
        ],
    },

    {
        "id": "nobleza_impuesto",
        "franja": "mediodia",
        "categoria": "otro",
        "condiciones": {
            "region": ["ciudad_amurallada", "aldea_agricola"],
            "riqueza": (0.2, 1.0),
        },
        "texto": "Un recaudador del señor exige el pago del impuesto.",
        "opciones": [
            {
                "texto_boton": "Pagar sin protestar",
                "transformaciones": {
                    "riqueza": -0.15,
                    "lealtad": +0.1,
                    "reputacion": +0.05,
                },
                "texto_resultado": "Pagas. El recaudador se va satisfecho.",
            },
            {
                "texto_boton": "Negociar",
                "transformaciones": {
                    "riqueza": -0.08,
                    "reputacion": -0.05,
                },
                "texto_resultado": "Negocias. Pagas menos, pero el recaudador no está feliz.",
            },
            {
                "texto_boton": "Resistirse",
                "transformaciones": {
                    "flags_add": ["buscado"],
                    "peligro_percibido": +0.3,
                    "lealtad": -0.2,
                },
                "texto_resultado": "Te niegas. Ahora eres un fugitivo.",
            },
        ],
    },

    {
        "id": "viajero_compania_peligro",
        "franja": "tarde",
        "categoria": "otro",
        "condiciones": {
            "presion_social": (0.0, 0.4),
            "peligro_latente": (0.4, 1.0),
        },
        "texto": "Un viajero solitario te ofrece compañía en el camino.",
        "opciones": [
            {
                "texto_boton": "Acompañarlo",
                "transformaciones": {
                    "presion_social": -0.15,
                    "peligro_percibido": -0.1,
                },
                "texto_resultado": "Viajas juntos. Te sientes más seguro.",
            },
            {
                "texto_boton": "Declinar",
                "transformaciones": {
                    "peligro_percibido": +0.05,
                },
                "texto_resultado": "Prefieres estar solo. Pero el camino es más peligroso.",
            },
        ],
    },

    {
        "id": "cosecha_ayuda_recompensa",
        "franja": "mediodia",
        "categoria": "trabajar",
        "condiciones": {
            "region": ["aldea_agricola"],
            "condicion": (0.5, 1.0),
            "flags_ausentes": ["trabajo_iglesia"],
        },
        "texto": "Los aldeanos necesitan ayuda urgente con la cosecha.",
        "opciones": [
            {
                "texto_boton": "Ayudar generosamente",
                "transformaciones": {
                    "reputacion": +0.2,
                    "descanso": -0.2,
                    "riqueza": +0.1,
                },
                "texto_resultado": "Trabajas duro. Los aldeanos te recompensan.",
            },
            {
                "texto_boton": "Ayudar poco",
                "transformaciones": {
                    "reputacion": +0.05,
                    "descanso": -0.05,
                },
                "texto_resultado": "Ayudas un poco. Es algo.",
            },
        ],
    },

    {
        "id": "tormenta_refugio_encuentro",
        "franja": "tarde",
        "categoria": "otro",
        "condiciones": {
            "clima_region": (0.0, 0.3),
        },
        "texto": "Una tormenta se aproxima. Necesitas refugio.",
        "opciones": [
            {
                "texto_boton": "Buscar refugio en una cueva",
                "transformaciones": {
                    "descanso": +0.15,
                    "temperatura_corporal": +0.1,
                    "peligro_percibido": +0.1,
                },
                "texto_resultado": "Encuentras una cueva. Segura, pero inquietante.",
            },
            {
                "texto_boton": "Buscar refugio en una casa",
                "transformaciones": {
                    "descanso": +0.2,
                    "presion_social": -0.1,
                },
                "texto_resultado": "Una familia te deja entrar. Eres bienvenido.",
            },
            {
                "texto_boton": "Continuar en la tormenta",
                "transformaciones": {
                    "heridas": +0.15,
                    "temperatura_corporal": -0.3,
                },
                "texto_resultado": "La tormenta te golpea. Resultas herido y congelado.",
            },
        ],
    },

    {
        "id": "pordiosero_historia",
        "franja": "tarde",
        "categoria": "otro",
        "condiciones": {
            "riqueza": (0.2, 1.0),
        },
        "texto": "Un pordiosero te cuenta su historia.",
        "opciones": [
            {
                "texto_boton": "Dar dinero y escuchar",
                "transformaciones": {
                    "riqueza": -0.08,
                    "reputacion": +0.1,
                    "fe": +0.05,
                },
                "texto_resultado": "Das dinero. Su historia te toca el corazón.",
            },
            {
                "texto_boton": "Dar poco dinero",
                "transformaciones": {
                    "riqueza": -0.02,
                    "reputacion": +0.02,
                },
                "texto_resultado": "Das poco. Es algo.",
            },
            {
                "texto_boton": "Ignorar",
                "transformaciones": {
                    "reputacion": -0.08,
                },
                "texto_resultado": "Lo ignoras. Pero su mirada te persigue.",
            },
        ],
    },

    {
        "id": "guardia_corrupcion",
        "franja": "mediodia",
        "categoria": "otro",
        "condiciones": {
            "region": ["ciudad_amurallada", "puerto_costero"],
            "riqueza": (0.3, 1.0),
            "flags_ausentes": ["buscado"],
        },
        "texto": "Un guardia corrupto te pide dinero para dejarte pasar.",
        "opciones": [
            {
                "texto_boton": "Pagar el soborno",
                "transformaciones": {
                    "riqueza": -0.1,
                    "presion_social": -0.05,
                },
                "texto_resultado": "Pagas. El guardia te deja pasar sin problemas.",
            },
            {
                "texto_boton": "Negarse",
                "transformaciones": {
                    "peligro_percibido": +0.15,
                    "reputacion": +0.05,
                },
                "texto_resultado": "Te niegas. El guardia te mira con odio.",
            },
        ],
    },

    {
        "id": "mercader_estafa",
        "franja": "mediodia",
        "categoria": "otro",
        "condiciones": {
            "region": ["puerto_costero", "ciudad_amurallada"],
            "riqueza": (0.3, 1.0),
        },
        "texto": "Un mercader te ofrece un 'trato especial'.",
        "opciones": [
            {
                "texto_boton": "Aceptar el trato",
                "transformaciones": {
                    "riqueza": -0.15,
                    "flags_add": ["estafado"],
                },
                "texto_resultado": "Te estafan. Pierdes dinero.",
            },
            {
                "texto_boton": "Ser cauteloso",
                "transformaciones": {
                    "riqueza": -0.05,
                    "reputacion": +0.05,
                },
                "texto_resultado": "Compras poco. Evitas la estafa.",
            },
        ],
    },

    {
        "id": "ermitano_sabiduria_profunda",
        "franja": "tarde",
        "categoria": "otro",
        "condiciones": {
            "region": ["montaña_rocosa", "bosque_denso"],
            "fe": (0.3, 1.0),
        },
        "texto": "Un ermitaño te ofrece enseñanzas profundas.",
        "opciones": [
            {
                "texto_boton": "Aprender",
                "transformaciones": {
                    "presion_social": -0.15,
                    "fe": +0.1,
                    "salud_mental": +0.1,
                },
                "texto_resultado": "Aprendes verdades profundas. Te sientes transformado.",
            },
            {
                "texto_boton": "Ignorar",
                "transformaciones": {},
                "texto_resultado": "Continúas tu camino.",
            },
        ],
    },

]
