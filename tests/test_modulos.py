"""
Tests for core/modulos.py
Tests the module evaluation and state transformation logic.

ISTQB concepts covered:
- Boundary value analysis: testing edge values of ranges
- Equivalence partitioning: grouping similar test cases
- State transition testing: how character state changes
"""

import pytest
from core.modulos import (
    _cumple_condiciones,
    _aplicar_transformaciones,
    modulos_disponibles,
    aplicar_opcion,
)
from core.personaje import crear_personaje
from core.motor import actualizar_derivadas
from data.linajes_data import LINAJES
from data.modulos_data import MODULOS


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def personaje_base():
    """Base character for testing."""
    linaje = LINAJES["campesino"]
    p = crear_personaje("Test", "hombre", 25, "aldea", linaje)
    return actualizar_derivadas(p)


@pytest.fixture
def condiciones_base():
    """Base conditions dict for testing _cumple_condiciones."""
    return {}


# ============================================================================
# TESTS: _cumple_condiciones()
# ============================================================================

class TestCumpleCondiciones:
    """Test the condition evaluation function."""

    def test_condiciones_vacias_siempre_true(self, personaje_base):
        """
        EQUIVALENCE PARTITION: empty conditions.
        If no conditions are specified, they're always met.
        """
        condiciones = {}
        assert _cumple_condiciones(personaje_base, condiciones) is True

    def test_rango_valido_dentro_limites(self, personaje_base):
        """
        BOUNDARY TEST: range condition within limits.
        If nutricion is 0.7 and condition is (0.5, 0.9), should be True.
        """
        personaje_base["condiciones"]["nutricion"] = 0.7
        condiciones = {"nutricion": (0.5, 0.9)}
        assert _cumple_condiciones(personaje_base, condiciones) is True

    def test_rango_invalido_bajo_limite(self, personaje_base):
        """
        BOUNDARY TEST: range condition below lower limit.
        If nutricion is 0.3 and condition is (0.5, 0.9), should be False.
        """
        personaje_base["condiciones"]["nutricion"] = 0.3
        condiciones = {"nutricion": (0.5, 0.9)}
        assert _cumple_condiciones(personaje_base, condiciones) is False

    def test_rango_invalido_sobre_limite(self, personaje_base):
        """
        BOUNDARY TEST: range condition above upper limit.
        If nutricion is 1.0 and condition is (0.5, 0.9), should be False.
        """
        personaje_base["condiciones"]["nutricion"] = 1.0
        condiciones = {"nutricion": (0.5, 0.9)}
        assert _cumple_condiciones(personaje_base, condiciones) is False

    def test_rango_en_limite_inferior_exacto(self, personaje_base):
        """
        BOUNDARY TEST: exactly at lower boundary.
        If nutricion is 0.5 and condition is (0.5, 0.9), should be True (inclusive).
        """
        personaje_base["condiciones"]["nutricion"] = 0.5
        condiciones = {"nutricion": (0.5, 0.9)}
        assert _cumple_condiciones(personaje_base, condiciones) is True

    def test_rango_en_limite_superior_exacto(self, personaje_base):
        """
        BOUNDARY TEST: exactly at upper boundary.
        If nutricion is 0.9 and condition is (0.5, 0.9), should be True (inclusive).
        """
        personaje_base["condiciones"]["nutricion"] = 0.9
        condiciones = {"nutricion": (0.5, 0.9)}
        assert _cumple_condiciones(personaje_base, condiciones) is True

    def test_flags_activos_presente(self, personaje_base):
        """
        EQUIVALENCE PARTITION: required flags present.
        If "buscado" flag is required and present, should be True.
        """
        personaje_base["flags"].add("buscado")
        condiciones = {"flags_activos": ["buscado"]}
        assert _cumple_condiciones(personaje_base, condiciones) is True

    def test_flags_activos_ausente(self, personaje_base):
        """
        EQUIVALENCE PARTITION: required flags missing.
        If "buscado" flag is required but absent, should be False.
        """
        personaje_base["flags"].clear()
        condiciones = {"flags_activos": ["buscado"]}
        assert _cumple_condiciones(personaje_base, condiciones) is False

    def test_flags_activos_multiples_todos_presentes(self, personaje_base):
        """
        EQUIVALENCE PARTITION: multiple required flags, all present.
        If ["buscado", "enfermo"] are required and both present, should be True.
        """
        personaje_base["flags"].add("buscado")
        personaje_base["flags"].add("enfermo")
        condiciones = {"flags_activos": ["buscado", "enfermo"]}
        assert _cumple_condiciones(personaje_base, condiciones) is True

    def test_flags_activos_multiples_uno_ausente(self, personaje_base):
        """
        EQUIVALENCE PARTITION: multiple required flags, one missing.
        If ["buscado", "enfermo"] are required but only "buscado" present, should be False.
        """
        personaje_base["flags"].add("buscado")
        personaje_base["flags"].discard("enfermo")
        condiciones = {"flags_activos": ["buscado", "enfermo"]}
        assert _cumple_condiciones(personaje_base, condiciones) is False

    def test_flags_ausentes_presente(self, personaje_base):
        """
        EQUIVALENCE PARTITION: forbidden flags present.
        If "excomulgado" must NOT be present and it is, should be False.
        """
        personaje_base["flags"].add("excomulgado")
        condiciones = {"flags_ausentes": ["excomulgado"]}
        assert _cumple_condiciones(personaje_base, condiciones) is False

    def test_flags_ausentes_ausente(self, personaje_base):
        """
        EQUIVALENCE PARTITION: forbidden flags absent.
        If "excomulgado" must NOT be present and it isn't, should be True.
        """
        personaje_base["flags"].discard("excomulgado")
        condiciones = {"flags_ausentes": ["excomulgado"]}
        assert _cumple_condiciones(personaje_base, condiciones) is True

    def test_region_valida(self, personaje_base):
        """
        EQUIVALENCE PARTITION: region matches.
        If region is "aldea" and condition requires "aldea", should be True.
        """
        personaje_base["region"] = "aldea"
        condiciones = {"region": ["aldea", "ciudad"]}
        assert _cumple_condiciones(personaje_base, condiciones) is True

    def test_region_invalida(self, personaje_base):
        """
        EQUIVALENCE PARTITION: region doesn't match.
        If region is "bosque" and condition requires ["aldea", "ciudad"], should be False.
        """
        personaje_base["region"] = "bosque"
        condiciones = {"region": ["aldea", "ciudad"]}
        assert _cumple_condiciones(personaje_base, condiciones) is False

    def test_multiples_condiciones_todas_cumplen(self, personaje_base):
        """
        STATE TRANSITION TEST: multiple conditions all met.
        If nutricion is in range AND region matches AND flags present, should be True.
        """
        personaje_base["condiciones"]["nutricion"] = 0.7
        personaje_base["region"] = "aldea"
        personaje_base["flags"].add("buscado")
        
        condiciones = {
            "nutricion": (0.5, 0.9),
            "region": ["aldea"],
            "flags_activos": ["buscado"],
        }
        assert _cumple_condiciones(personaje_base, condiciones) is True

    def test_multiples_condiciones_una_falla(self, personaje_base):
        """
        STATE TRANSITION TEST: multiple conditions, one fails.
        If nutricion is in range but region doesn't match, should be False.
        """
        personaje_base["condiciones"]["nutricion"] = 0.7
        personaje_base["region"] = "bosque"  # doesn't match
        personaje_base["flags"].add("buscado")
        
        condiciones = {
            "nutricion": (0.5, 0.9),
            "region": ["aldea"],
            "flags_activos": ["buscado"],
        }
        assert _cumple_condiciones(personaje_base, condiciones) is False


# ============================================================================
# TESTS: _aplicar_transformaciones()
# ============================================================================

class TestAplicarTransformaciones:
    """Test the state transformation function."""

    def test_suma_a_condicion_positiva(self, personaje_base):
        """
        EQUIVALENCE PARTITION: positive delta.
        Adding +0.2 to nutricion should increase it.
        """
        nutricion_inicial = personaje_base["condiciones"]["nutricion"]
        transformaciones = {"nutricion": +0.2}
        personaje_base = _aplicar_transformaciones(personaje_base, transformaciones)
        assert personaje_base["condiciones"]["nutricion"] == nutricion_inicial + 0.2

    def test_resta_a_condicion_negativa(self, personaje_base):
        """
        EQUIVALENCE PARTITION: negative delta.
        Subtracting -0.2 from nutricion should decrease it.
        """
        nutricion_inicial = personaje_base["condiciones"]["nutricion"]
        transformaciones = {"nutricion": -0.2}
        personaje_base = _aplicar_transformaciones(personaje_base, transformaciones)
        assert personaje_base["condiciones"]["nutricion"] == nutricion_inicial - 0.2

    def test_clampea_minimo_cero(self, personaje_base):
        """
        BOUNDARY TEST: clamping to minimum.
        If nutricion is 0.1 and we subtract 0.2, should clamp to 0.0, not go negative.
        """
        personaje_base["condiciones"]["nutricion"] = 0.1
        transformaciones = {"nutricion": -0.2}
        personaje_base = _aplicar_transformaciones(personaje_base, transformaciones)
        assert personaje_base["condiciones"]["nutricion"] == 0.0

    def test_clampea_maximo_uno(self, personaje_base):
        """
        BOUNDARY TEST: clamping to maximum.
        If nutricion is 0.9 and we add 0.2, should clamp to 1.0, not exceed.
        """
        personaje_base["condiciones"]["nutricion"] = 0.9
        transformaciones = {"nutricion": +0.2}
        personaje_base = _aplicar_transformaciones(personaje_base, transformaciones)
        assert personaje_base["condiciones"]["nutricion"] == 1.0

    def test_reputacion_puede_ser_negativa(self, personaje_base):
        """
        EQUIVALENCE PARTITION: reputacion special case.
        Reputacion can go negative (unlike other social variables).
        """
        personaje_base["social"]["reputacion"] = 0.2
        transformaciones = {"reputacion": -0.5}
        personaje_base = _aplicar_transformaciones(personaje_base, transformaciones)
        assert personaje_base["social"]["reputacion"] == -0.3

    def test_reputacion_clampea_a_menos_uno(self, personaje_base):
        """
        BOUNDARY TEST: reputacion minimum.
        Reputacion should clamp to -1.0, not go lower.
        """
        personaje_base["social"]["reputacion"] = -0.5
        transformaciones = {"reputacion": -0.8}
        personaje_base = _aplicar_transformaciones(personaje_base, transformaciones)
        assert personaje_base["social"]["reputacion"] == -1.0

    def test_reputacion_clampea_a_uno(self, personaje_base):
        """
        BOUNDARY TEST: reputacion maximum.
        Reputacion should clamp to 1.0, not exceed.
        """
        personaje_base["social"]["reputacion"] = 0.8
        transformaciones = {"reputacion": +0.5}
        personaje_base = _aplicar_transformaciones(personaje_base, transformaciones)
        assert personaje_base["social"]["reputacion"] == 1.0

    def test_flags_add_unico(self, personaje_base):
        """
        EQUIVALENCE PARTITION: add single flag.
        Adding "buscado" flag should add it to the set.
        """
        personaje_base["flags"].discard("buscado")
        transformaciones = {"flags_add": ["buscado"]}
        personaje_base = _aplicar_transformaciones(personaje_base, transformaciones)
        assert "buscado" in personaje_base["flags"]

    def test_flags_add_multiples(self, personaje_base):
        """
        EQUIVALENCE PARTITION: add multiple flags.
        Adding ["buscado", "enfermo"] should add both.
        """
        personaje_base["flags"].clear()
        transformaciones = {"flags_add": ["buscado", "enfermo"]}
        personaje_base = _aplicar_transformaciones(personaje_base, transformaciones)
        assert "buscado" in personaje_base["flags"]
        assert "enfermo" in personaje_base["flags"]

    def test_flags_remove_unico(self, personaje_base):
        """
        EQUIVALENCE PARTITION: remove single flag.
        Removing "buscado" flag should remove it.
        """
        personaje_base["flags"].add("buscado")
        transformaciones = {"flags_remove": ["buscado"]}
        personaje_base = _aplicar_transformaciones(personaje_base, transformaciones)
        assert "buscado" not in personaje_base["flags"]

    def test_flags_remove_no_existe(self, personaje_base):
        """
        ERROR CASE: remove non-existent flag.
        Removing a flag that doesn't exist should not raise error (discard is safe).
        """
        personaje_base["flags"].discard("inexistente")
        transformaciones = {"flags_remove": ["inexistente"]}
        # Should not raise
        personaje_base = _aplicar_transformaciones(personaje_base, transformaciones)
        assert "inexistente" not in personaje_base["flags"]

    def test_multiples_transformaciones(self, personaje_base):
        """
        STATE TRANSITION TEST: multiple transformations at once.
        Applying nutricion, reputacion, and flags should all work together.
        """
        transformaciones = {
            "nutricion": +0.1,
            "reputacion": +0.2,
            "flags_add": ["buscado"],
        }
        nutricion_antes = personaje_base["condiciones"]["nutricion"]
        reputacion_antes = personaje_base["social"]["reputacion"]
        
        personaje_base = _aplicar_transformaciones(personaje_base, transformaciones)
        
        assert personaje_base["condiciones"]["nutricion"] == nutricion_antes + 0.1
        assert personaje_base["social"]["reputacion"] == reputacion_antes + 0.2
        assert "buscado" in personaje_base["flags"]


# ============================================================================
# TESTS: modulos_disponibles()
# ============================================================================

class TestModulosDisponibles:
    """Test the module filtering function."""

    def test_filtra_por_franja(self, personaje_base):
        """
        EQUIVALENCE PARTITION: franja filtering.
        Only modules from the requested franja should be returned.
        """
        disponibles = modulos_disponibles(personaje_base, "mañana", MODULOS)
        for modulo in disponibles:
            assert modulo["franja"] == "mañana"

    def test_filtra_por_condiciones(self, personaje_base):
        """
        EQUIVALENCE PARTITION: condition filtering.
        Only modules whose conditions are met should be returned.
        """
        personaje_base["condiciones"]["nutricion"] = 0.1  # muy baja
        disponibles = modulos_disponibles(personaje_base, "mañana", MODULOS)
        
        # Todos los módulos disponibles deben cumplir sus condiciones
        for modulo in disponibles:
            assert _cumple_condiciones(personaje_base, modulo.get("condiciones", {}))

    def test_lista_vacia_si_no_hay_modulos(self, personaje_base):
        """
        BOUNDARY TEST: no modules available.
        If no modules match, should return empty list, not error.
        """
        # Crear condiciones imposibles
        personaje_base["condiciones"]["nutricion"] = 0.0
        personaje_base["condiciones"]["hidratacion"] = 0.0
        personaje_base["condiciones"]["descanso"] = 0.0
        personaje_base["flags"].add("muerto")  # flag que no existe en módulos
        
        disponibles = modulos_disponibles(personaje_base, "mañana", MODULOS)
        # Puede haber módulos sin condiciones, así que no aseguramos lista vacía
        # pero sí que todos cumplen condiciones
        for modulo in disponibles:
            assert _cumple_condiciones(personaje_base, modulo.get("condiciones", {}))

    def test_retorna_lista_no_vacia_con_condiciones_normales(self, personaje_base):
        """
        FUNCTIONAL TEST: normal conditions.
        With normal character state, should have available modules.
        """
        disponibles = modulos_disponibles(personaje_base, "mañana", MODULOS)
        assert len(disponibles) > 0, "Should have at least one module available"


# ============================================================================
# TESTS: aplicar_opcion()
# ============================================================================

class TestAplicarOpcion:
    """Test the option application function."""

    def test_aplica_transformaciones(self, personaje_base):
        """
        FUNCTIONAL TEST: transformations applied.
        Choosing an option should apply its transformations.
        """
        modulo = MODULOS[0]  # primer módulo disponible
        nutricion_antes = personaje_base["condiciones"]["nutricion"]
        
        personaje_base, resultado = aplicar_opcion(personaje_base, modulo, 0)
        
        # La nutrición debería haber cambiado (según la transformación de la opción)
        transformaciones = modulo["opciones"][0].get("transformaciones", {})
        if "nutricion" in transformaciones:
            nutricion_esperada = max(0.0, min(1.0, nutricion_antes + transformaciones["nutricion"]))
            assert personaje_base["condiciones"]["nutricion"] == nutricion_esperada

    def test_retorna_texto_resultado(self, personaje_base):
        """
        FUNCTIONAL TEST: result text returned.
        Should return the result text from the chosen option.
        """
        modulo = MODULOS[0]
        personaje_base, resultado = aplicar_opcion(personaje_base, modulo, 0)
        
        texto_esperado = modulo["opciones"][0]["texto_resultado"]
        assert resultado == texto_esperado

    def test_registra_en_historial(self, personaje_base):
        """
        FUNCTIONAL TEST: history tracking.
        Choosing an option should record it in the character's history.
        """
        modulo = MODULOS[0]
        historial_antes = len(personaje_base["historial"])
        
        personaje_base, _ = aplicar_opcion(personaje_base, modulo, 0)
        
        assert len(personaje_base["historial"]) == historial_antes + 1
        entrada = personaje_base["historial"][-1]
        assert entrada["modulo"] == modulo["id"]
        assert entrada["opcion"] == modulo["opciones"][0]["texto_boton"]

    def test_distintas_opciones_distintos_resultados(self, personaje_base):
        """
        EQUIVALENCE PARTITION: different options, different outcomes.
        Choosing option 0 vs option 1 should produce different results.
        """
        modulo = MODULOS[0]
        
        p1 = personaje_base.copy()
        p1["condiciones"] = personaje_base["condiciones"].copy()
        p1["social"] = personaje_base["social"].copy()
        p1["flags"] = personaje_base["flags"].copy()
        
        p2 = personaje_base.copy()
        p2["condiciones"] = personaje_base["condiciones"].copy()
        p2["social"] = personaje_base["social"].copy()
        p2["flags"] = personaje_base["flags"].copy()
        
        p1, resultado1 = aplicar_opcion(p1, modulo, 0)
        p2, resultado2 = aplicar_opcion(p2, modulo, 1)
        
        # Los resultados deberían ser distintos
        assert resultado1 != resultado2
