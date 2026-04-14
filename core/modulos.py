"""
Evaluación y aplicación de módulos narrativos.
Un módulo es un evento con condiciones, opciones y transformaciones.
"""


def _cumple_condiciones(personaje: dict, condiciones: dict) -> bool:
    """
    Evalúa si el personaje cumple las condiciones de activación de un módulo.
    Soporta: rangos de float, listas de valores válidos, flags, bools.
    """
    c = personaje["condiciones"]
    s = personaje["social"]
    flags = personaje["flags"]

    for clave, valor in condiciones.items():

        # flags
        if clave == "flags_activos":
            for flag in valor:
                if flag not in flags:
                    return False
            continue

        if clave == "flags_ausentes":
            for flag in valor:
                if flag in flags:
                    return False
            continue

        # región
        if clave == "region":
            if personaje["region"] not in valor:
                return False
            continue

        # rangos de variables continuas
        fuente = {**c, **s}
        if clave in fuente:
            v_actual = fuente[clave]
            if isinstance(valor, tuple) and len(valor) == 2:
                if not (valor[0] <= v_actual <= valor[1]):
                    return False
            elif isinstance(valor, list):
                if v_actual not in valor:
                    return False
            elif isinstance(valor, bool):
                if v_actual != valor:
                    return False

    return True


def _aplicar_transformaciones(personaje: dict, transformaciones: dict) -> dict:
    """
    Aplica los cambios de estado de una opción elegida.
    Soporta: deltas en condiciones/social, flags add/remove.
    """
    c = personaje["condiciones"]
    s = personaje["social"]

    for clave, delta in transformaciones.items():

        if clave == "flags_add":
            for flag in delta:
                personaje["flags"].add(flag)
            continue

        if clave == "flags_remove":
            for flag in delta:
                personaje["flags"].discard(flag)
            continue

        if clave in c:
            c[clave] = max(0.0, min(1.0, c[clave] + delta))
        elif clave in s:
            # reputacion puede ser negativa
            if clave == "reputacion":
                s[clave] = max(-1.0, min(1.0, s[clave] + delta))
            else:
                s[clave] = max(0.0, min(1.0, s[clave] + delta))

    return personaje


def modulos_disponibles(personaje: dict, franja: str, todos_modulos: list) -> list:
    """
    Filtra los módulos disponibles para el personaje en una franja del día.
    """
    return [
        m for m in todos_modulos
        if m.get("franja") == franja
        and _cumple_condiciones(personaje, m.get("condiciones", {}))
    ]


def aplicar_opcion(personaje: dict, modulo: dict, indice_opcion: int) -> tuple[dict, str]:
    """
    Aplica la opción elegida por el jugador y devuelve el personaje actualizado
    y el texto de resultado.
    """
    opcion = modulo["opciones"][indice_opcion]
    personaje = _aplicar_transformaciones(personaje, opcion.get("transformaciones", {}))

    # registrar en historial
    personaje["historial"].append({
        "dia":    personaje["dia"],
        "modulo": modulo["id"],
        "opcion": opcion["texto_boton"],
    })

    return personaje, opcion["texto_resultado"]
