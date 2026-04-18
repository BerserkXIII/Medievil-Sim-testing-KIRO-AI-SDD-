"""
Tests for core/mundo.py
Tests region creation and world mechanics.
"""

import pytest
from core.mundo import (
    calcular_abundancia,
    calcular_seguridad,
    calcular_cohesion_social,
    calcular_peligro_latente,
    actualizar_derivadas_region,
    obtener_contexto_personaje,
    avanzar_ciclo_region,
)
from data.regiones_data import obtener_region, REGIONES


# ============================================================================
# TESTS: Derived calculations
# ============================================================================

class TestCalculoDerivadasRegion:
    """Test region derived value calculations."""

    def test_abundancia_en_rango(self):
        """Abundance should always be in [0, 1]."""
        for _ in range(100):
            abundancia = calcular_abundancia(
                poblacion=0.5,
                clima=0.5,
                geografia=0.5
            )
            assert 0.0 <= abundancia <= 1.0

    def test_abundancia_sube_con_geografia_buena(self):
        """Better geography should increase abundance."""
        abundancia_mala = calcular_abundancia(0.5, 0.5, 0.1)
        abundancia_buena = calcular_abundancia(0.5, 0.5, 0.9)
        assert abundancia_buena > abundancia_mala

    def test_seguridad_en_rango(self):
        """Security should always be in [0, 1]."""
        for _ in range(100):
            seguridad = calcular_seguridad(
                estabilidad=0.5,
                poblacion=0.5,
                gobierno=0.5
            )
            assert 0.0 <= seguridad <= 1.0

    def test_seguridad_baja_con_inestabilidad(self):
        """Low stability should decrease security."""
        seguridad_estable = calcular_seguridad(0.9, 0.5, 0.5)
        seguridad_inestable = calcular_seguridad(0.1, 0.5, 0.5)
        assert seguridad_estable > seguridad_inestable

    def test_cohesion_en_rango(self):
        """Cohesion should always be in [0, 1]."""
        for _ in range(100):
            cohesion = calcular_cohesion_social(
                religion=0.5,
                gobierno=0.5,
                abundancia=0.5
            )
            assert 0.0 <= cohesion <= 1.0

    def test_cohesion_sube_con_religion(self):
        """Higher religion should increase cohesion."""
        cohesion_baja_religion = calcular_cohesion_social(0.1, 0.5, 0.5)
        cohesion_alta_religion = calcular_cohesion_social(0.9, 0.5, 0.5)
        assert cohesion_alta_religion > cohesion_baja_religion

    def test_peligro_latente_en_rango(self):
        """Latent danger should always be in [0, 1]."""
        for _ in range(100):
            peligro = calcular_peligro_latente(
                seguridad=0.5,
                conflicto=0.5,
                epidemia=0.5
            )
            assert 0.0 <= peligro <= 1.0

    def test_peligro_latente_sube_con_conflicto(self):
        """Higher conflict should increase latent danger."""
        peligro_paz = calcular_peligro_latente(0.5, 0.1, 0.0)
        peligro_guerra = calcular_peligro_latente(0.5, 0.9, 0.0)
        assert peligro_guerra > peligro_paz


# ============================================================================
# TESTS: Region initialization
# ============================================================================

class TestRegionInitialization:
    """Test region creation and setup."""

    @pytest.mark.parametrize("nombre_region", list(REGIONES.keys()))
    def test_todas_regiones_validas(self, nombre_region):
        """All regions should be obtainable and valid."""
        region = obtener_region(nombre_region)
        
        # Check structure
        assert "nombre" in region
        assert "tipo" in region
        assert "geografia" in region
        assert "clima" in region
        assert "condiciones" in region
        assert "derivadas" in region
        assert "peligro_latente" in region
        assert "flags" in region

    def test_region_tiene_todas_condiciones(self):
        """Region should have all required conditions."""
        region = obtener_region("puerto_costero")
        
        required = [
            "poblacion", "clima", "estabilidad", "gobierno",
            "religion", "epidemia", "conflicto"
        ]
        for cond in required:
            assert cond in region["condiciones"]

    def test_region_condiciones_en_rango(self):
        """All region conditions should be in valid ranges."""
        region = obtener_region("aldea_agricola")
        
        for nombre, valor in region["condiciones"].items():
            assert 0.0 <= valor <= 1.0, f"{nombre}={valor} out of range"

    def test_obtener_region_retorna_copia(self):
        """Getting a region should return a copy, not the original."""
        region1 = obtener_region("puerto_costero")
        region2 = obtener_region("puerto_costero")
        
        # Modify one
        region1["condiciones"]["poblacion"] = 0.1
        
        # Other should be unchanged
        assert region2["condiciones"]["poblacion"] == 0.8


# ============================================================================
# TESTS: Region updates
# ============================================================================

class TestActualizarRegion:
    """Test region derivate updates."""

    def test_actualizar_calcula_derivadas(self):
        """Updating should calculate all derived values."""
        region = obtener_region("puerto_costero")
        region = actualizar_derivadas_region(region)
        
        assert region["derivadas"]["abundancia"] > 0.0
        assert region["derivadas"]["seguridad"] > 0.0
        assert region["derivadas"]["cohesion"] > 0.0

    def test_actualizar_activa_flags_hambruna(self):
        """Low abundance should activate hambruna flag."""
        region = obtener_region("desierto_arido")
        # Force very low abundance
        region["condiciones"]["poblacion"] = 0.01
        region["geografia"] = 0.05
        region = actualizar_derivadas_region(region)
        
        # Should have very low abundance
        if region["derivadas"]["abundancia"] < 0.2:
            assert "hambruna" in region["flags"]

    def test_actualizar_activa_flags_bandidos(self):
        """Low security should activate bandidos flag."""
        region = obtener_region("montaña_rocosa")
        region = actualizar_derivadas_region(region)
        
        # Mountain should have low security
        assert region["derivadas"]["seguridad"] < 0.4
        assert "bandidos_organizados" in region["flags"]

    def test_actualizar_activa_flags_cultos(self):
        """Low cohesion + low religion should activate cultos flag."""
        region = obtener_region("bosque_denso")
        region = actualizar_derivadas_region(region)
        
        # Forest should have low cohesion and religion
        if region["derivadas"]["cohesion"] < 0.3 and region["condiciones"]["religion"] < 0.4:
            assert "cultos_paganos" in region["flags"]

    def test_avanzar_ciclo_degrada_estabilidad_en_conflicto(self):
        """High conflict should degrade stability."""
        region = obtener_region("ciudad_amurallada")
        region["condiciones"]["conflicto"] = 0.8
        estabilidad_antes = region["condiciones"]["estabilidad"]
        
        region = avanzar_ciclo_region(region)
        
        assert region["condiciones"]["estabilidad"] < estabilidad_antes

    def test_avanzar_ciclo_mejora_estabilidad_en_paz(self):
        """Low conflict should improve stability."""
        region = obtener_region("aldea_agricola")
        region["condiciones"]["conflicto"] = 0.0
        estabilidad_antes = region["condiciones"]["estabilidad"]
        
        region = avanzar_ciclo_region(region)
        
        assert region["condiciones"]["estabilidad"] > estabilidad_antes

    def test_avanzar_ciclo_reduce_epidemia(self):
        """Epidemia should slowly fade."""
        region = obtener_region("puerto_costero")
        region["condiciones"]["epidemia"] = 0.8
        epidemia_antes = region["condiciones"]["epidemia"]
        
        region = avanzar_ciclo_region(region)
        
        assert region["condiciones"]["epidemia"] < epidemia_antes


# ============================================================================
# TESTS: Context extraction
# ============================================================================

class TestObtenerContextoPersonaje:
    """Test extracting character context from region."""

    def test_contexto_tiene_todas_variables(self):
        """Context should have all required variables."""
        region = obtener_region("puerto_costero")
        region = actualizar_derivadas_region(region)
        contexto = obtener_contexto_personaje(region)
        
        required = [
            "clima_region",
            "disponibilidad_agua",
            "disponibilidad_comida",
            "tension_social",
            "peligro_latente",
        ]
        for var in required:
            assert var in contexto

    def test_contexto_en_rango(self):
        """All context values should be in valid ranges."""
        region = obtener_region("aldea_agricola")
        region = actualizar_derivadas_region(region)
        contexto = obtener_contexto_personaje(region)
        
        for nombre, valor in contexto.items():
            assert 0.0 <= valor <= 1.0, f"{nombre}={valor} out of range"

    def test_contexto_refleja_abundancia(self):
        """High abundance should mean high food availability."""
        region1 = obtener_region("puerto_costero")
        region1 = actualizar_derivadas_region(region1)
        contexto1 = obtener_contexto_personaje(region1)
        
        region2 = obtener_region("desierto_arido")
        region2 = actualizar_derivadas_region(region2)
        contexto2 = obtener_contexto_personaje(region2)
        
        # Coastal should have more food than desert
        assert contexto1["disponibilidad_comida"] > contexto2["disponibilidad_comida"]

    def test_contexto_refleja_cohesion(self):
        """Low cohesion should mean high social tension."""
        region1 = obtener_region("aldea_agricola")
        region1 = actualizar_derivadas_region(region1)
        contexto1 = obtener_contexto_personaje(region1)
        
        region2 = obtener_region("ciudad_amurallada")
        region2["condiciones"]["conflicto"] = 0.8
        region2 = actualizar_derivadas_region(region2)
        contexto2 = obtener_contexto_personaje(region2)
        
        # Peaceful village should have less tension than conflicted city
        assert contexto1["tension_social"] < contexto2["tension_social"]
