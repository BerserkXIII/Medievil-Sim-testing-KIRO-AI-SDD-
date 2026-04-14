"""
Tests para el motor del juego (core/motor.py).
Probamos las funciones de cálculo de derivadas y avance del día.
"""

import pytest
from core.motor import (
    calcular_salud_fisica,
    calcular_salud_mental,
    calcular_condicion,
    calcular_vitalidad,
    actualizar_derivadas,
    avanzar_dia,
    esta_vivo,
    UMBRAL_CRITICO,
)
from core.personaje import crear_personaje
from data.linajes_data import LINAJES


# ============================================================================
# FIXTURES: datos reutilizables para los tests
# ============================================================================

@pytest.fixture
def condiciones_base():
    """Condiciones normales de un personaje sano."""
    return {
        "nutricion": 0.7,
        "hidratacion": 0.7,
        "descanso": 0.7,
        "heridas": 0.0,
        "higiene": 0.7,
        "temperatura_corporal": 0.5,
        "presion_social": 0.2,
        "enfermedades": [],
        "peligro_latente": 0.0,
        "peligro_percibido": 0.0,
    }


@pytest.fixture
def atributos_base():
    """Atributos normales (promedio)."""
    return {
        "constitucion": 5,
        "resistencia": 5,
        "inteligencia": 5,
        "percepcion": 5,
        "voluntad": 5,
        "carisma": 5,
        "fe_innata": 5,
        "fortuna": 5,
    }


@pytest.fixture
def personaje_base():
    """Personaje completo con estado inicial."""
    linaje = LINAJES["campesino"]
    p = crear_personaje("Test", "hombre", 25, "aldea", linaje)
    return actualizar_derivadas(p)


# ============================================================================
# TESTS: calcular_salud_fisica
# ============================================================================

def test_salud_fisica_baja_con_nutricion_baja(condiciones_base, atributos_base):
    """
    BOUNDARY TEST: nutricion en extremo bajo.
    Si nutricion es muy baja, salud_fisica debe ser baja.
    """
    condiciones_base["nutricion"] = 0.1
    resultado = calcular_salud_fisica(condiciones_base, atributos_base)
    assert resultado < 0.5, "Nutricion baja debería resultar en salud baja"


def test_salud_fisica_alta_con_condiciones_optimas(condiciones_base, atributos_base):
    """
    EQUIVALENCE PARTITION: condiciones óptimas.
    Si todo está bien, salud_fisica debe ser alta.
    """
    condiciones_base["nutricion"] = 0.9
    condiciones_base["hidratacion"] = 0.9
    condiciones_base["descanso"] = 0.9
    resultado = calcular_salud_fisica(condiciones_base, atributos_base)
    assert resultado > 0.6, "Condiciones óptimas deberían resultar en salud alta"


def test_salud_fisica_penalizada_por_heridas(condiciones_base, atributos_base):
    """
    EQUIVALENCE PARTITION: heridas presentes.
    Las heridas deben reducir salud_fisica significativamente.
    """
    sin_heridas = calcular_salud_fisica(condiciones_base, atributos_base)
    condiciones_base["heridas"] = 0.5
    con_heridas = calcular_salud_fisica(condiciones_base, atributos_base)
    assert con_heridas < sin_heridas, "Heridas deberían reducir salud_fisica"


def test_salud_fisica_constitucion_alta_compensa(condiciones_base, atributos_base):
    """
    EQUIVALENCE PARTITION: constitucion alta.
    Constitucion alta debería compensar condiciones malas.
    """
    condiciones_base["nutricion"] = 0.3
    condiciones_base["heridas"] = 0.3
    
    salud_baja_const = calcular_salud_fisica(condiciones_base, atributos_base)
    
    atributos_base["constitucion"] = 9
    salud_alta_const = calcular_salud_fisica(condiciones_base, atributos_base)
    
    assert salud_alta_const > salud_baja_const, \
        "Constitucion alta debería mejorar salud_fisica"


def test_salud_fisica_siempre_en_rango(condiciones_base, atributos_base):
    """
    BOUNDARY TEST: extremos.
    Salud física nunca debe salir del rango [0, 1], incluso con valores extremos.
    """
    # extremo bajo
    condiciones_base["nutricion"] = 0.0
    condiciones_base["hidratacion"] = 0.0
    condiciones_base["descanso"] = 0.0
    condiciones_base["heridas"] = 1.0
    condiciones_base["enfermedades"] = ["fiebre", "infeccion", "plaga"]
    atributos_base["constitucion"] = 1
    
    resultado = calcular_salud_fisica(condiciones_base, atributos_base)
    assert 0.0 <= resultado <= 1.0, "Salud física debe estar siempre en [0, 1]"


# ============================================================================
# TESTS: calcular_salud_mental
# ============================================================================

def test_salud_mental_baja_con_presion_social_alta(condiciones_base, atributos_base):
    """
    BOUNDARY TEST: presion_social en extremo alto.
    Presion social alta debería reducir salud_mental.
    """
    condiciones_base["presion_social"] = 0.9
    resultado = calcular_salud_mental(condiciones_base, atributos_base, {"fe": 0.3})
    assert resultado < 0.6, "Presion social alta debería reducir salud_mental"


def test_salud_mental_fe_protege(condiciones_base, atributos_base):
    """
    EQUIVALENCE PARTITION: fe como escudo.
    Fe alta con fe_innata alta debería proteger la salud_mental.
    """
    condiciones_base["presion_social"] = 0.7
    atributos_base["fe_innata"] = 9
    
    salud_sin_fe = calcular_salud_mental(condiciones_base, atributos_base, {"fe": 0.1})
    salud_con_fe = calcular_salud_mental(condiciones_base, atributos_base, {"fe": 0.9})
    
    assert salud_con_fe > salud_sin_fe, "Fe alta debería mejorar salud_mental"


def test_salud_mental_voluntad_ralentiza_degradacion(condiciones_base, atributos_base):
    """
    EQUIVALENCE PARTITION: voluntad como resistencia mental.
    Voluntad alta debería ralentizar la degradación de salud_mental.
    """
    condiciones_base["presion_social"] = 0.8
    
    salud_baja_voluntad = calcular_salud_mental(condiciones_base, atributos_base, {"fe": 0.3})
    
    atributos_base["voluntad"] = 9
    salud_alta_voluntad = calcular_salud_mental(condiciones_base, atributos_base, {"fe": 0.3})
    
    assert salud_alta_voluntad > salud_baja_voluntad, \
        "Voluntad alta debería mejorar salud_mental"


# ============================================================================
# TESTS: actualizar_derivadas y vitalidad
# ============================================================================

def test_vitalidad_baja_con_condicion_baja(personaje_base):
    """
    EQUIVALENCE PARTITION: condicion baja.
    Si condicion es baja, vitalidad debe ser baja.
    """
    personaje_base["condiciones"]["nutricion"] = 0.1
    personaje_base["condiciones"]["descanso"] = 0.1
    personaje_base = actualizar_derivadas(personaje_base)
    assert personaje_base["vitalidad"] < 0.5, "Vitalidad baja con condicion baja"


def test_esta_vivo_mientras_vitalidad_sobre_umbral(personaje_base):
    """
    BOUNDARY TEST: umbral de muerte.
    Mientras vitalidad > umbral_critico, el personaje está vivo.
    """
    personaje_base["vitalidad"] = UMBRAL_CRITICO + 0.01
    personaje_base["dias_criticos"] = 0
    assert esta_vivo(personaje_base), "Personaje vivo si vitalidad > umbral"


def test_muere_tras_3_dias_bajo_umbral(personaje_base):
    """
    BOUNDARY TEST: contador de días críticos.
    Tras 3 días bajo umbral, el personaje muere.
    """
    personaje_base["vitalidad"] = UMBRAL_CRITICO - 0.01
    personaje_base["dias_criticos"] = 2
    assert esta_vivo(personaje_base), "Aún vivo con 2 días críticos"
    
    personaje_base["dias_criticos"] = 3
    assert not esta_vivo(personaje_base), "Muere tras 3 días críticos"


# ============================================================================
# TESTS: avanzar_dia
# ============================================================================

def test_avanzar_dia_incrementa_contador(personaje_base):
    """
    FUNCTIONAL TEST: avance del tiempo.
    Cada día que pasa, el contador de días sube.
    """
    dia_inicial = personaje_base["dia"]
    personaje_base = avanzar_dia(personaje_base)
    assert personaje_base["dia"] == dia_inicial + 1, "Día debe incrementarse"


def test_avanzar_dia_degrada_necesidades(personaje_base):
    """
    FUNCTIONAL TEST: degradación pasiva.
    Sin acción del jugador, las necesidades bajan cada día.
    """
    nutricion_inicial = personaje_base["condiciones"]["nutricion"]
    personaje_base = avanzar_dia(personaje_base)
    nutricion_final = personaje_base["condiciones"]["nutricion"]
    assert nutricion_final < nutricion_inicial, "Nutricion debe degradarse"


def test_avanzar_dia_recalcula_derivadas(personaje_base):
    """
    FUNCTIONAL TEST: recalculación de estado.
    Después de avanzar día, las derivadas se recalculan.
    """
    personaje_base["condiciones"]["nutricion"] = 0.1
    personaje_base = avanzar_dia(personaje_base)
    # Si nutricion es baja, salud_fisica debe ser baja
    assert personaje_base["estado"]["salud_fisica"] < 0.5, \
        "Derivadas deben recalcularse tras avanzar día"
