"""
Tests for core/personaje.py
Tests character creation and initialization.

ISTQB concepts:
- Boundary value analysis: stat ranges [1, 10]
- Equivalence partitioning: different lineages
- Data validation: all layers initialized correctly
"""

import pytest
from core.personaje import crear_personaje, _stat_semialeat
from data.linajes_data import LINAJES


# ============================================================================
# TESTS: _stat_semialeat()
# ============================================================================

class TestStatSemialeat:
    """Test the semi-random stat generation function."""

    def test_stat_siempre_entre_1_y_10(self):
        """
        BOUNDARY TEST: stat range.
        No matter what inputs, stat should always be between 1 and 10.
        """
        for _ in range(100):  # run 100 times to catch randomness
            stat = _stat_semialeat(base=5, modificador=0)
            assert 1 <= stat <= 10, f"Stat {stat} out of range [1, 10]"

    def test_stat_minimo_es_1(self):
        """
        BOUNDARY TEST: minimum boundary.
        Even with base=1 and negative modifier, should clamp to 1.
        """
        stat = _stat_semialeat(base=1, modificador=-5)
        assert stat >= 1, "Stat should never go below 1"

    def test_stat_maximo_es_10(self):
        """
        BOUNDARY TEST: maximum boundary.
        Even with base=10 and positive modifier, should clamp to 10.
        """
        stat = _stat_semialeat(base=10, modificador=+5)
        assert stat <= 10, "Stat should never exceed 10"

    def test_modificador_positivo_sube_stat(self):
        """
        EQUIVALENCE PARTITION: positive modifier effect.
        With positive modifier, stat should be higher on average.
        """
        # Run multiple times to average out randomness
        stats_sin_mod = [_stat_semialeat(base=5, modificador=0) for _ in range(50)]
        stats_con_mod = [_stat_semialeat(base=5, modificador=+3) for _ in range(50)]
        
        promedio_sin = sum(stats_sin_mod) / len(stats_sin_mod)
        promedio_con = sum(stats_con_mod) / len(stats_con_mod)
        
        assert promedio_con > promedio_sin, "Positive modifier should increase average stat"

    def test_modificador_negativo_baja_stat(self):
        """
        EQUIVALENCE PARTITION: negative modifier effect.
        With negative modifier, stat should be lower on average.
        """
        stats_sin_mod = [_stat_semialeat(base=5, modificador=0) for _ in range(50)]
        stats_con_mod = [_stat_semialeat(base=5, modificador=-3) for _ in range(50)]
        
        promedio_sin = sum(stats_sin_mod) / len(stats_sin_mod)
        promedio_con = sum(stats_con_mod) / len(stats_con_mod)
        
        assert promedio_con < promedio_sin, "Negative modifier should decrease average stat"

    def test_ruido_es_pequeno(self):
        """
        BOUNDARY TEST: randomness range.
        The random noise should be small (-1 to +1), not huge.
        """
        # Si base=5 y modificador=0, el resultado debería estar cerca de 5
        stats = [_stat_semialeat(base=5, modificador=0) for _ in range(100)]
        
        # Todos deberían estar entre 4 y 6 (base ± ruido máximo)
        for stat in stats:
            assert 4 <= stat <= 6, f"Stat {stat} has too much variance from base 5"


# ============================================================================
# TESTS: crear_personaje()
# ============================================================================

class TestCrearPersonaje:
    """Test character creation."""

    def test_crea_personaje_con_todos_campos(self):
        """
        FUNCTIONAL TEST: complete initialization.
        Character should have all required fields after creation.
        """
        linaje = LINAJES["campesino"]
        p = crear_personaje("Aldric", "hombre", 25, "aldea", linaje)
        
        # Identidad
        assert p["nombre"] == "Aldric"
        assert p["sexo"] == "hombre"
        assert p["edad"] == 25
        assert p["region"] == "aldea"
        
        # Capas
        assert "atributos" in p
        assert "habilidades" in p
        assert "condiciones" in p
        assert "contexto" in p
        assert "estado" in p
        assert "vitalidad" in p
        assert "social" in p
        assert "flags" in p
        assert "historial" in p

    def test_atributos_en_rango_valido(self):
        """
        BOUNDARY TEST: attribute ranges.
        All attributes should be between 1 and 10.
        """
        linaje = LINAJES["campesino"]
        p = crear_personaje("Test", "hombre", 25, "aldea", linaje)
        
        for nombre_attr, valor in p["atributos"].items():
            assert 1 <= valor <= 10, f"Attribute {nombre_attr}={valor} out of range"

    def test_condiciones_en_rango_valido(self):
        """
        BOUNDARY TEST: condition ranges.
        All conditions should be between 0 and 1 (or empty list for diseases).
        """
        linaje = LINAJES["campesino"]
        p = crear_personaje("Test", "hombre", 25, "aldea", linaje)
        
        for nombre_cond, valor in p["condiciones"].items():
            if nombre_cond == "enfermedades":
                assert isinstance(valor, list), "Enfermedades should be a list"
            else:
                assert 0.0 <= valor <= 1.0, f"Condition {nombre_cond}={valor} out of range"

    def test_social_en_rango_valido(self):
        """
        BOUNDARY TEST: social variable ranges.
        Riqueza, fe, lealtad should be [0, 1]. Reputacion can be [-1, 1].
        """
        linaje = LINAJES["campesino"]
        p = crear_personaje("Test", "hombre", 25, "aldea", linaje)
        
        assert 0.0 <= p["social"]["riqueza"] <= 1.0
        assert 0.0 <= p["social"]["fe"] <= 1.0
        assert 0.0 <= p["social"]["lealtad"] <= 1.0
        assert -1.0 <= p["social"]["reputacion"] <= 1.0

    def test_personaje_empieza_vivo(self):
        """
        FUNCTIONAL TEST: initial vitality.
        Character should start alive (dias_criticos = 0).
        """
        linaje = LINAJES["campesino"]
        p = crear_personaje("Test", "hombre", 25, "aldea", linaje)
        
        assert p["dias_criticos"] == 0, "Should start with 0 critical days"
        assert p["vitalidad"] == 1.0, "Should start with full vitality"

    def test_flags_vacio_al_inicio(self):
        """
        FUNCTIONAL TEST: initial flags.
        Character should start with no flags.
        """
        linaje = LINAJES["campesino"]
        p = crear_personaje("Test", "hombre", 25, "aldea", linaje)
        
        assert len(p["flags"]) == 0, "Should start with no flags"
        assert isinstance(p["flags"], set), "Flags should be a set"

    def test_historial_vacio_al_inicio(self):
        """
        FUNCTIONAL TEST: initial history.
        Character should start with empty history.
        """
        linaje = LINAJES["campesino"]
        p = crear_personaje("Test", "hombre", 25, "aldea", linaje)
        
        assert len(p["historial"]) == 0, "Should start with empty history"
        assert isinstance(p["historial"], list), "History should be a list"

    def test_dia_comienza_en_1(self):
        """
        FUNCTIONAL TEST: initial day.
        Character should start on day 1.
        """
        linaje = LINAJES["campesino"]
        p = crear_personaje("Test", "hombre", 25, "aldea", linaje)
        
        assert p["dia"] == 1, "Should start on day 1"


# ============================================================================
# TESTS: Linaje effects
# ============================================================================

class TestLinajeEffects:
    """Test how lineages affect character creation."""

    @pytest.mark.parametrize("nombre_linaje", list(LINAJES.keys()))
    def test_todos_linajes_crean_personaje_valido(self, nombre_linaje):
        """
        EQUIVALENCE PARTITION: all lineages.
        Every lineage should create a valid character.
        """
        linaje = LINAJES[nombre_linaje]
        p = crear_personaje("Test", "hombre", 25, "aldea", linaje)
        
        # Check all attributes are in range
        for valor in p["atributos"].values():
            assert 1 <= valor <= 10

    def test_linaje_campesino_tiene_constitucion_alta(self):
        """
        EQUIVALENCE PARTITION: campesino lineage.
        Campesino should have higher constitution on average.
        """
        linaje = LINAJES["campesino"]
        
        # Create multiple characters to average out randomness
        constituciones = []
        for _ in range(20):
            p = crear_personaje("Test", "hombre", 25, "aldea", linaje)
            constituciones.append(p["atributos"]["constitucion"])
        
        promedio = sum(constituciones) / len(constituciones)
        assert promedio > 5.0, "Campesino should have higher constitution on average"

    def test_linaje_clerigo_tiene_inteligencia_alta(self):
        """
        EQUIVALENCE PARTITION: cleric lineage.
        Cleric should have higher intelligence on average.
        """
        linaje = LINAJES["clerigo"]
        
        inteligencias = []
        for _ in range(20):
            p = crear_personaje("Test", "hombre", 25, "aldea", linaje)
            inteligencias.append(p["atributos"]["inteligencia"])
        
        promedio = sum(inteligencias) / len(inteligencias)
        assert promedio > 5.0, "Cleric should have higher intelligence on average"

    def test_linaje_soldado_tiene_combate_inicial(self):
        """
        EQUIVALENCE PARTITION: soldier lineage.
        Soldier should start with combat skill.
        """
        linaje = LINAJES["soldado"]
        p = crear_personaje("Test", "hombre", 25, "aldea", linaje)
        
        assert p["habilidades"]["combate"] > 0, "Soldier should start with combat skill"

    def test_linaje_mercader_tiene_riqueza_inicial(self):
        """
        EQUIVALENCE PARTITION: merchant lineage.
        Merchant should start with more wealth.
        """
        linaje_mercader = LINAJES["mercader"]
        linaje_campesino = LINAJES["campesino"]
        
        p_mercader = crear_personaje("Test", "hombre", 25, "aldea", linaje_mercader)
        p_campesino = crear_personaje("Test", "hombre", 25, "aldea", linaje_campesino)
        
        assert p_mercader["social"]["riqueza"] > p_campesino["social"]["riqueza"], \
            "Merchant should start richer than peasant"

    def test_linaje_noble_caido_tiene_riqueza_baja(self):
        """
        EQUIVALENCE PARTITION: fallen noble lineage.
        Fallen noble should start poor despite noble status.
        """
        linaje = LINAJES["noble_caido"]
        p = crear_personaje("Test", "hombre", 25, "aldea", linaje)
        
        assert p["social"]["riqueza"] < 0.3, "Fallen noble should start poor"


# ============================================================================
# TESTS: Edge cases
# ============================================================================

class TestEdgeCases:
    """Test edge cases and unusual inputs."""

    def test_personaje_edad_minima(self):
        """
        BOUNDARY TEST: minimum age.
        Character should be creatable at age 10.
        """
        linaje = LINAJES["campesino"]
        p = crear_personaje("Test", "hombre", 10, "aldea", linaje)
        
        assert p["edad"] == 10

    def test_personaje_edad_maxima(self):
        """
        BOUNDARY TEST: maximum age.
        Character should be creatable at age 90.
        """
        linaje = LINAJES["campesino"]
        p = crear_personaje("Test", "hombre", 90, "aldea", linaje)
        
        assert p["edad"] == 90

    def test_personaje_nombre_vacio(self):
        """
        ERROR CASE: empty name.
        Should still create character (name is just a string).
        """
        linaje = LINAJES["campesino"]
        p = crear_personaje("", "hombre", 25, "aldea", linaje)
        
        assert p["nombre"] == ""

    def test_personaje_sexo_arbitrario(self):
        """
        ERROR CASE: arbitrary sex value.
        Should accept any string (no validation on sex).
        """
        linaje = LINAJES["campesino"]
        p = crear_personaje("Test", "otro", 25, "aldea", linaje)
        
        assert p["sexo"] == "otro"

    def test_personaje_region_arbitraria(self):
        """
        ERROR CASE: arbitrary region.
        Should accept any region string.
        """
        linaje = LINAJES["campesino"]
        p = crear_personaje("Test", "hombre", 25, "marte", linaje)
        
        assert p["region"] == "marte"

    def test_linaje_sin_modificadores(self):
        """
        ERROR CASE: lineage without modifiers.
        Should handle gracefully with default values.
        """
        linaje_vacio = {
            "nombre": "Desconocido",
            "tags": [],
        }
        p = crear_personaje("Test", "hombre", 25, "aldea", linaje_vacio)
        
        # Should create character with default stats (all around 5)
        for valor in p["atributos"].values():
            assert 1 <= valor <= 10


# ============================================================================
# TESTS: Consistency
# ============================================================================

class TestConsistency:
    """Test that character state is consistent."""

    def test_contexto_tiene_todas_variables(self):
        """
        DATA VALIDATION: context completeness.
        Context should have all required environmental variables.
        """
        linaje = LINAJES["campesino"]
        p = crear_personaje("Test", "hombre", 25, "aldea", linaje)
        
        required_context = [
            "clima_region",
            "disponibilidad_agua",
            "disponibilidad_comida",
            "tension_social",
        ]
        for var in required_context:
            assert var in p["contexto"], f"Missing context variable: {var}"

    def test_estado_tiene_todas_derivadas(self):
        """
        DATA VALIDATION: derived state completeness.
        Estado should have all derived health variables.
        """
        linaje = LINAJES["campesino"]
        p = crear_personaje("Test", "hombre", 25, "aldea", linaje)
        
        required_estado = [
            "salud_fisica",
            "salud_mental",
            "condicion",
        ]
        for var in required_estado:
            assert var in p["estado"], f"Missing estado variable: {var}"

    def test_dos_personajes_distintos_tienen_stats_distintos(self):
        """
        RANDOMNESS TEST: uniqueness.
        Two characters created with same inputs should have different stats
        (due to randomness).
        """
        linaje = LINAJES["campesino"]
        p1 = crear_personaje("Test", "hombre", 25, "aldea", linaje)
        p2 = crear_personaje("Test", "hombre", 25, "aldea", linaje)
        
        # Very unlikely they're identical
        assert p1["atributos"] != p2["atributos"], \
            "Two characters should have different random stats"
