"""
Motor del juego: cálculo de variables derivadas y avance del día.
Aquí viven las fórmulas entre capas. Sin valores exactos definitivos,
diseñados para ser ajustados durante el desarrollo.
"""

UMBRAL_CRITICO = 0.15
DIAS_PARA_MORIR = 3


def _normalizar(valor: float) -> float:
    return max(0.0, min(1.0, valor))


def _modificador_edad(edad: int) -> float:
    """
    Devuelve un multiplicador de recuperación según la edad.
    Joven recupera rápido, anciano se degrada más.
    """
    if edad <= 14:   return 1.1
    if edad <= 25:   return 1.2
    if edad <= 45:   return 1.0
    if edad <= 60:   return 0.85
    return 0.65


def calcular_salud_fisica(condiciones: dict, atributos: dict) -> float:
    """
    Capa 0 → Capa 1.
    Base: nutricion + hidratacion + descanso (pesos similares)
    Resta: heridas, enfermedades, temperatura fuera de rango
    Modificador: constitucion, resistencia
    """
    base = (
        condiciones["nutricion"]    * 0.35 +
        condiciones["hidratacion"]  * 0.30 +
        condiciones["descanso"]     * 0.25
    )

    penalizacion_heridas = condiciones["heridas"] * 0.4

    penalizacion_enfermedades = len(condiciones["enfermedades"]) * 0.08

    # temperatura: 0.5 es óptimo, alejarse penaliza
    desviacion_temp = abs(condiciones["temperatura_corporal"] - 0.5) * 0.3

    # constitucion reduce penalizaciones (escala 1-10 → 0.8-1.2)
    mod_constitucion = 0.8 + (atributos["constitucion"] - 1) * (0.4 / 9)
    # resistencia reduce degradación (efecto más suave)
    mod_resistencia  = 0.9 + (atributos["resistencia"] - 1) * (0.2 / 9)

    resultado = (base - penalizacion_heridas - penalizacion_enfermedades - desviacion_temp)
    resultado *= mod_constitucion * mod_resistencia

    return _normalizar(resultado)


def calcular_salud_mental(condiciones: dict, atributos: dict, social: dict) -> float:
    """
    Capa 0 → Capa 1.
    Base: descanso + fe (si fe_innata es alta)
    Resta: presion_social, peligro_percibido, enfermedades graves
    Modificador: voluntad, fe_innata
    """
    base = condiciones["descanso"] * 0.4

    # fe protege la mente si fe_innata es alta
    mod_fe_innata = atributos["fe_innata"] / 10.0
    aporte_fe = social["fe"] * mod_fe_innata * 0.3
    base += aporte_fe

    penalizacion_presion  = condiciones["presion_social"]   * 0.35
    penalizacion_peligro  = condiciones["peligro_percibido"] * 0.25
    penalizacion_enfermed = len(condiciones["enfermedades"]) * 0.05

    # voluntad ralentiza degradación mental (escala 1-10 → 0.8-1.2)
    mod_voluntad = 0.8 + (atributos["voluntad"] - 1) * (0.4 / 9)

    resultado = (base - penalizacion_presion - penalizacion_peligro - penalizacion_enfermed)
    resultado *= mod_voluntad

    return _normalizar(resultado)


def calcular_condicion(salud_fisica: float, salud_mental: float, edad: int) -> float:
    """
    Capa 1 → Capa 1 (síntesis).
    Salud física tiene algo más de peso a corto plazo.
    La edad modifica el techo máximo alcanzable.
    """
    base = salud_fisica * 0.6 + salud_mental * 0.4
    return _normalizar(base * _modificador_edad(edad))


def calcular_vitalidad(condicion: float, edad: int, fortuna: int) -> float:
    """
    Capa 1 → Capa 2.
    Fortuna es un modificador silencioso y pequeño.
    """
    mod_fortuna = 0.95 + (fortuna - 1) * (0.1 / 9)  # 0.95 a 1.05
    return _normalizar(condicion * _modificador_edad(edad) * mod_fortuna)


def actualizar_derivadas(personaje: dict) -> dict:
    """
    Recalcula todas las variables derivadas del personaje.
    Se llama una vez por día, después de aplicar transformaciones.
    """
    c  = personaje["condiciones"]
    a  = personaje["atributos"]
    s  = personaje["social"]
    edad = personaje["edad"]

    salud_fisica = calcular_salud_fisica(c, a)
    salud_mental = calcular_salud_mental(c, a, s)
    condicion    = calcular_condicion(salud_fisica, salud_mental, edad)
    vitalidad    = calcular_vitalidad(condicion, edad, a["fortuna"])

    personaje["estado"]["salud_fisica"] = salud_fisica
    personaje["estado"]["salud_mental"] = salud_mental
    personaje["estado"]["condicion"]    = condicion
    personaje["vitalidad"]              = vitalidad

    # control de días críticos
    if vitalidad < UMBRAL_CRITICO:
        personaje["dias_criticos"] += 1
    else:
        personaje["dias_criticos"] = 0

    return personaje


def esta_vivo(personaje: dict) -> bool:
    return personaje["dias_criticos"] < DIAS_PARA_MORIR


def avanzar_dia(personaje: dict) -> dict:
    """
    Incrementa el día y aplica degradación natural pasiva.
    Las necesidades básicas bajan un poco cada día sin acción del jugador.
    """
    personaje["dia"] += 1
    personaje["edad"] = personaje["edad"]  # la edad avanza cada 365 días (futuro)

    c = personaje["condiciones"]

    # degradación diaria pasiva (el mundo no espera)
    c["nutricion"]    = _normalizar(c["nutricion"]    - 0.08)
    c["hidratacion"]  = _normalizar(c["hidratacion"]  - 0.10)
    c["descanso"]     = _normalizar(c["descanso"]     - 0.15)
    c["higiene"]      = _normalizar(c["higiene"]      - 0.03)

    # la presion social decae lentamente si no hay eventos
    c["presion_social"] = _normalizar(c["presion_social"] - 0.02)

    return actualizar_derivadas(personaje)
