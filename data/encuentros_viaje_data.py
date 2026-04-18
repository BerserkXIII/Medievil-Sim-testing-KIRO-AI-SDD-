"""
Travel modules: dynamically generated based on available destinations.
"""


def generar_modulos_viaje(region_actual: str) -> list:
    """
    Generate travel modules for current region.
    Shows available destinations with distance info.
    """
    from core.viaje import obtener_destinos_disponibles, clasificar_viaje
    
    try:
        destinos = obtener_destinos_disponibles(region_actual)
    except ValueError:
        return []
    
    modulos = []
    
    for destino, distancia in destinos.items():
        tipo_viaje = clasificar_viaje(distancia)
        
        # Descripción según distancia
        if tipo_viaje == "corto":
            desc_distancia = "muy cerca"
        elif tipo_viaje == "medio":
            desc_distancia = "a media jornada"
        else:
            desc_distancia = "varios días de viaje"
        
        modulo = {
            "id": f"viajar_a_{destino}",
            "franja": "mediodia",
            "condiciones": {},
            "texto": f"Podrías viajar a {destino} ({desc_distancia}).",
            "opciones": [
                {
                    "texto_boton": f"Viajar a {destino}",
                    "transformaciones": {"_viaje": destino},  # marcador especial
                    "texto_resultado": f"Te diriges hacia {destino}...",
                }
            ],
        }
        modulos.append(modulo)
    
    return modulos
