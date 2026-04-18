"""
Game UI: main game loop with travel, encounters, and events.
"""

import tkinter as tk
from tkinter import scrolledtext
from core.motor import avanzar_dia, esta_vivo
from core.modulos import modulos_disponibles, aplicar_opcion
from core.viaje import (
    realizar_viaje,
    completar_viaje_tras_encuentro,
    obtener_destinos_disponibles,
    clasificar_viaje,
    generar_advertencias_viaje,
)
from core.mundo import obtener_contexto_personaje, actualizar_derivadas_region
from data.modulos_data import MODULOS
from data.regiones_data import obtener_region

FRANJAS = ["mañana", "mediodia", "tarde", "noche"]

COLOR_FONDO    = "#1a1a1a"
COLOR_TEXTO    = "#d4c5a9"
COLOR_BOTON    = "#3a2e1e"
COLOR_BOTON_TX = "#d4c5a9"
COLOR_BARRA_OK = "#4a7c4e"
COLOR_BARRA_MAL= "#7c4a4a"
COLOR_TITULO   = "#c9a961"
COLOR_CATEGORIA = "#2a2416"
COLOR_CATEGORIA_TX = "#d4af37"

# Categorías de módulos
CATEGORIAS_MODULOS = {
    "comer": {"nombre": "🍖 Comer", "color": "#4a3a2a"},
    "rezar": {"nombre": "✝️ Rezar", "color": "#3a2a4a"},
    "trabajar": {"nombre": "⚒️ Trabajar", "color": "#3a4a2a"},
    "descansar": {"nombre": "😴 Descansar", "color": "#2a3a4a"},
    "viajar": {"nombre": "🗺️ Viajar", "color": "#4a3a1a"},
    "otro": {"nombre": "❓ Otros", "color": "#3a3a3a"},
}

def _categorizar_modulo(modulo: dict) -> str:
    """Categoriza un módulo por su ID. Usa lógica más robusta."""
    modulo_id = modulo.get("id", "").lower()
    
    # Palabras clave por categoría
    palabras_comer = ["comer", "comida", "desayun", "almuerz", "cen"]
    palabras_rezar = ["rezar", "fe", "iglesia", "cura", "dios", "oración"]
    palabras_trabajar = ["trabajar", "trabajo", "oficio", "labor", "ganancia"]
    palabras_descansar = ["descansar", "dormir", "sueño", "cama", "reposo", "fiebre", "enferm"]
    palabras_viajar = ["viajar", "viaje", "camino", "ruta", "destino"]
    
    for palabra in palabras_comer:
        if palabra in modulo_id:
            return "comer"
    for palabra in palabras_rezar:
        if palabra in modulo_id:
            return "rezar"
    for palabra in palabras_trabajar:
        if palabra in modulo_id:
            return "trabajar"
    for palabra in palabras_descansar:
        if palabra in modulo_id:
            return "descansar"
    for palabra in palabras_viajar:
        if palabra in modulo_id:
            return "viajar"
    
    return "otro"

def _agrupar_modulos_por_categoria(modulos: list) -> dict:
    """Agrupa módulos por categoría."""
    agrupados = {cat: [] for cat in CATEGORIAS_MODULOS.keys()}
    
    for modulo in modulos:
        categoria = _categorizar_modulo(modulo)
        agrupados[categoria].append(modulo)
    
    # Remover categorías vacías
    return {cat: mods for cat, mods in agrupados.items() if mods}


class Interfaz:
    def __init__(self, root: tk.Tk, personaje: dict):
        self.root = root
        self.personaje = personaje
        self.franja_actual = 0
        
        # Estado de viaje
        self.en_preparacion_viaje = False
        self.viaje_destino = None
        self.viaje_preparacion = None
        self.viaje_resultado = None
        
        # Estado de categorías desplegables
        self.categoria_abierta = None
        self.frames_categorias = {}

        self.root.title("Vida Medieval")
        self.root.configure(bg=COLOR_FONDO)
        self.root.geometry("800x700")

        self._construir_ui()
        self._mostrar_estado_dia()

    def _construir_ui(self):
        # Zona superior: info del personaje y región
        self.frame_header = tk.Frame(self.root, bg="#0d0d0d", height=80)
        self.frame_header.pack(fill="x", padx=0, pady=0)
        self.label_header = tk.Label(
            self.frame_header, text="",
            bg="#0d0d0d", fg=COLOR_TITULO,
            font=("Georgia", 12, "bold")
        )
        self.label_header.pack(anchor="w", padx=15, pady=8)

        # Zona narración
        self.texto_narracion = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, height=12,
            bg="#0d0d0d", fg=COLOR_TEXTO,
            font=("Georgia", 10), state="disabled",
            relief="flat", padx=10, pady=10,
        )
        self.texto_narracion.pack(fill="both", expand=True, padx=10, pady=(5, 5))

        # Zona estado (barras)
        self.frame_estado = tk.Frame(self.root, bg=COLOR_FONDO)
        self.frame_estado.pack(fill="x", padx=10, pady=4)
        self.labels_estado = {}
        self._construir_barras_estado()

        # Zona botones
        self.frame_botones = tk.Frame(self.root, bg=COLOR_FONDO)
        self.frame_botones.pack(fill="both", expand=True, padx=10, pady=6)

    def _construir_barras_estado(self):
        variables = [
            ("Vitalidad", "vitalidad", None),
            ("Nutrición", "nutricion", "condiciones"),
            ("Descanso", "descanso", "condiciones"),
            ("Salud física", "salud_fisica", "estado"),
            ("Salud mental", "salud_mental", "estado"),
            ("Riqueza", "riqueza", "social"),
        ]
        for i, (etiqueta, clave, fuente) in enumerate(variables):
            col = i % 3
            row = i // 3
            frame = tk.Frame(self.frame_estado, bg=COLOR_FONDO)
            frame.grid(row=row, column=col, padx=6, pady=2, sticky="w")
            tk.Label(frame, text=etiqueta, bg=COLOR_FONDO, fg=COLOR_TEXTO,
                     font=("Georgia", 8)).pack(anchor="w")
            canvas = tk.Canvas(frame, width=140, height=8,
                                bg="#2a2a2a", highlightthickness=0)
            canvas.pack()
            self.labels_estado[(clave, fuente)] = canvas

    def _actualizar_barras(self):
        for (clave, fuente), canvas in self.labels_estado.items():
            if fuente is None:
                valor = self.personaje.get(clave, 0)
            else:
                valor = self.personaje[fuente].get(clave, 0)
            valor = max(0.0, min(1.0, valor))
            color = COLOR_BARRA_OK if valor > 0.4 else COLOR_BARRA_MAL
            canvas.delete("all")
            canvas.create_rectangle(0, 0, int(140 * valor), 8, fill=color, outline="")

    def _narrar(self, texto: str):
        self.texto_narracion.configure(state="normal")
        self.texto_narracion.insert("end", texto + "\n\n")
        self.texto_narracion.see("end")
        self.texto_narracion.configure(state="disabled")

    def _limpiar_botones(self):
        for widget in self.frame_botones.winfo_children():
            widget.destroy()

    def _actualizar_header(self):
        """Actualiza el encabezado con info del personaje y región."""
        p = self.personaje
        region = obtener_region(p["region"])
        texto = f"Día {p['dia']} | {p['nombre']}, {p['edad']} años | {region['nombre']} | Linaje: {p['linaje']}"
        self.label_header.config(text=texto)

    def _mostrar_estado_dia(self):
        """Muestra el encabezado del día y lanza la primera franja."""
        self._actualizar_header()
        self._actualizar_barras()
        self._narrar(
            f"═══════════════════════════════════════\n"
            f"Día {self.personaje['dia']}\n"
            f"═══════════════════════════════════════"
        )
        self.franja_actual = 0
        self._mostrar_franja()

    def _mostrar_franja(self):
        """Muestra los módulos disponibles agrupados por categoría."""
        if self.franja_actual >= len(FRANJAS):
            self._fin_dia()
            return

        franja = FRANJAS[self.franja_actual]
        disponibles = modulos_disponibles(self.personaje, franja, MODULOS)

        # Añadir módulos de viaje en mediodía
        if franja == "mediodia":
            modulos_viaje = self._generar_modulos_viaje()
            disponibles.extend(modulos_viaje)

        self._limpiar_botones()
        self.categoria_abierta = None
        self.frames_categorias = {}

        if not disponibles:
            self._narrar(f"[{franja.upper()}] Nada especial ocurre.")
            self.franja_actual += 1
            self.root.after(800, self._mostrar_franja)
            return

        # Mostrar encabezado de franja
        self._narrar(f"[{franja.upper()}] ¿Qué haces?\n")
        
        # Agrupar módulos por categoría
        agrupados = _agrupar_modulos_por_categoria(disponibles)
        
        # Crear frame con scroll para botones
        canvas = tk.Canvas(self.frame_botones, bg=COLOR_FONDO, highlightthickness=0)
        scrollbar = tk.Scrollbar(self.frame_botones, orient="vertical", command=canvas.yview)
        frame_scroll = tk.Frame(canvas, bg=COLOR_FONDO)
        
        frame_scroll.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=frame_scroll, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Mostrar botones de categoría
        for categoria in CATEGORIAS_MODULOS.keys():
            if categoria not in agrupados:
                continue
            
            modulos_cat = agrupados[categoria]
            info_cat = CATEGORIAS_MODULOS[categoria]
            
            # Botón de categoría (desplegable)
            btn_categoria = tk.Button(
                frame_scroll,
                text=f"{info_cat['nombre']} ({len(modulos_cat)})",
                bg=info_cat["color"], fg=COLOR_CATEGORIA_TX,
                font=("Georgia", 10, "bold"), relief="flat",
                padx=10, pady=6, cursor="hand2",
                command=lambda cat=categoria, mods=modulos_cat: self._toggle_categoria(cat, mods),
            )
            btn_categoria.pack(fill="x", pady=2)
            
            # Frame para opciones (inicialmente oculto)
            frame_opciones = tk.Frame(frame_scroll, bg=COLOR_FONDO)
            frame_opciones.pack(fill="x", padx=20, pady=0)
            frame_opciones.pack_forget()  # Ocultar inicialmente
            
            self.frames_categorias[categoria] = {
                "frame": frame_opciones,
                "modulos": modulos_cat,
                "visible": False,
            }
        
        # Empacar canvas y scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _toggle_categoria(self, categoria: str, modulos: list):
        """Abre/cierra una categoría. Solo una puede estar abierta a la vez."""
        # Cerrar categoría abierta anterior
        if self.categoria_abierta and self.categoria_abierta != categoria:
            frame_anterior = self.frames_categorias[self.categoria_abierta]["frame"]
            frame_anterior.pack_forget()
            self.frames_categorias[self.categoria_abierta]["visible"] = False
        
        # Toggle categoría actual
        frame_actual = self.frames_categorias[categoria]["frame"]
        
        if self.frames_categorias[categoria]["visible"]:
            # Cerrar
            frame_actual.pack_forget()
            self.frames_categorias[categoria]["visible"] = False
            self.categoria_abierta = None
        else:
            # Abrir
            frame_actual.pack_forget()  # Remover primero
            frame_actual.pack(fill="x", padx=20, pady=0)
            
            # Limpiar frame anterior
            for widget in frame_actual.winfo_children():
                widget.destroy()
            
            # Agregar botones de opciones
            for modulo in modulos:
                self._agregar_opciones_modulo(frame_actual, modulo)
            
            self.frames_categorias[categoria]["visible"] = True
            self.categoria_abierta = categoria

    def _agregar_opciones_modulo(self, parent: tk.Frame, modulo: dict):
        """Agrega los botones de opciones de un módulo a un frame.
        Sistema robusto que maneja textos largos y múltiples opciones."""
        
        # Frame para el módulo completo
        frame_modulo = tk.Frame(parent, bg="#1a1a1a", relief="flat")
        frame_modulo.pack(fill="x", pady=3, padx=0)
        
        # Texto narrativo del módulo (en un Text widget para mejor manejo)
        texto_widget = tk.Text(
            frame_modulo,
            height=2, width=60,
            bg="#0d0d0d", fg=COLOR_TEXTO,
            font=("Georgia", 9), wrap=tk.WORD,
            relief="flat", padx=8, pady=6,
            state="disabled",
        )
        texto_widget.pack(fill="x", padx=5, pady=(4, 2))
        
        # Insertar texto narrativo
        texto_widget.config(state="normal")
        texto_widget.insert("1.0", f"• {modulo['texto']}")
        texto_widget.config(state="disabled")
        
        # Frame para botones de opciones
        frame_opciones = tk.Frame(frame_modulo, bg="#1a1a1a")
        frame_opciones.pack(fill="x", padx=5, pady=(0, 4))
        
        # Botones de opciones
        for i, opcion in enumerate(modulo["opciones"]):
            btn_opcion = tk.Button(
                frame_opciones,
                text=opcion['texto_boton'],
                bg="#2a2a2a", fg=COLOR_BOTON_TX,
                font=("Georgia", 9), relief="flat",
                padx=10, pady=5, cursor="hand2",
                wraplength=400,
                justify="left",
                command=lambda idx=i, m=modulo: self._elegir_opcion(m, idx),
            )
            btn_opcion.pack(fill="x", pady=2)
        
        # Separador visual
        sep = tk.Frame(parent, bg="#3a3a3a", height=1)
        sep.pack(fill="x", pady=2)

    def _elegir_opcion(self, modulo: dict, indice: int):
        """Aplica la opción elegida."""
        opcion = modulo["opciones"][indice]
        transformaciones = opcion.get("transformaciones", {})

        # Detectar si es un viaje
        if "_viaje" in transformaciones:
            destino = transformaciones["_viaje"]
            self._preparar_viaje(destino)
            return

        # Aplicar transformación normal
        self.personaje, resultado = aplicar_opcion(self.personaje, modulo, indice)
        self._narrar(resultado)
        self._actualizar_barras()
        self.franja_actual += 1
        self.root.after(500, self._mostrar_franja)

    def _generar_modulos_viaje(self) -> list:
        """Genera módulos de viaje para los destinos disponibles."""
        try:
            destinos = obtener_destinos_disponibles(self.personaje["region"])
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
            
            region_destino = obtener_region(destino)
            modulo = {
                "id": f"viajar_a_{destino}",
                "franja": "mediodia",
                "condiciones": {},
                "texto": f"Podrías viajar a {region_destino['nombre']} ({desc_distancia}).",
                "opciones": [
                    {
                        "texto_boton": f"Viajar a {region_destino['nombre']}",
                        "transformaciones": {"_viaje": destino},
                        "texto_resultado": f"Te diriges hacia {region_destino['nombre']}...",
                    }
                ],
            }
            modulos.append(modulo)
        
        return modulos

    def _preparar_viaje(self, destino: str):
        """Muestra opciones de preparación para el viaje."""
        region_destino = obtener_region(destino)
        tipo_viaje = clasificar_viaje(
            obtener_destinos_disponibles(self.personaje["region"])[destino]
        )
        
        self._limpiar_botones()
        self.en_preparacion_viaje = True
        self.viaje_destino = destino
        
        # Mostrar advertencias
        advertencias = generar_advertencias_viaje(region_destino)
        if advertencias:
            self._narrar("\n⚠️ ADVERTENCIAS DEL VIAJE:")
            for adv in advertencias:
                self._narrar(f"  • {adv}")
        
        # Mostrar opciones de preparación según tipo de viaje
        if tipo_viaje == "corto":
            self._narrar("\nEs un viaje corto. Puedes partir sin preparación.")
            self._mostrar_opciones_preparacion_corto(destino)
        else:
            self._narrar("\n¿Cómo quieres prepararte para este viaje?")
            self._mostrar_opciones_preparacion_largo(destino)

    def _mostrar_opciones_preparacion_corto(self, destino: str):
        """Opciones para viaje corto (sin preparación necesaria)."""
        btn_partir = tk.Button(
            self.frame_botones,
            text="Partir ahora",
            bg=COLOR_BOTON, fg=COLOR_BOTON_TX,
            font=("Georgia", 10), relief="flat",
            padx=10, pady=6, cursor="hand2",
            command=lambda: self._iniciar_viaje(destino, preparacion=None),
        )
        btn_partir.pack(fill="x", pady=2)
        
        btn_cancelar = tk.Button(
            self.frame_botones,
            text="Cancelar",
            bg="#2a2a2a", fg=COLOR_BOTON_TX,
            font=("Georgia", 10), relief="flat",
            padx=10, pady=6, cursor="hand2",
            command=self._cancelar_preparacion_viaje,
        )
        btn_cancelar.pack(fill="x", pady=2)

    def _mostrar_opciones_preparacion_largo(self, destino: str):
        """Opciones para viaje largo (con preparación)."""
        btn_arma = tk.Button(
            self.frame_botones,
            text="Llevar arma (reduce encuentros)",
            bg=COLOR_BOTON, fg=COLOR_BOTON_TX,
            font=("Georgia", 10), relief="flat",
            padx=10, pady=6, cursor="hand2",
            command=lambda: self._iniciar_viaje(destino, preparacion="arma"),
        )
        btn_arma.pack(fill="x", pady=2)
        
        btn_dinero = tk.Button(
            self.frame_botones,
            text="Llevar dinero (para sobornar)",
            bg=COLOR_BOTON, fg=COLOR_BOTON_TX,
            font=("Georgia", 10), relief="flat",
            padx=10, pady=6, cursor="hand2",
            command=lambda: self._iniciar_viaje(destino, preparacion="dinero"),
        )
        btn_dinero.pack(fill="x", pady=2)
        
        btn_sin_prep = tk.Button(
            self.frame_botones,
            text="Partir sin preparación",
            bg="#2a2a2a", fg=COLOR_BOTON_TX,
            font=("Georgia", 10), relief="flat",
            padx=10, pady=6, cursor="hand2",
            command=lambda: self._iniciar_viaje(destino, preparacion=None),
        )
        btn_sin_prep.pack(fill="x", pady=2)
        
        btn_cancelar = tk.Button(
            self.frame_botones,
            text="Cancelar",
            bg="#1a1a1a", fg=COLOR_BOTON_TX,
            font=("Georgia", 10), relief="flat",
            padx=10, pady=6, cursor="hand2",
            command=self._cancelar_preparacion_viaje,
        )
        btn_cancelar.pack(fill="x", pady=2)

    def _cancelar_preparacion_viaje(self):
        """Cancela la preparación y vuelve a mostrar la franja."""
        self.en_preparacion_viaje = False
        self.viaje_destino = None
        self.viaje_preparacion = None
        self._narrar("Decides quedarte por ahora.")
        self.franja_actual += 1
        self.root.after(500, self._mostrar_franja)

    def _iniciar_viaje(self, destino: str, preparacion: str = None):
        """Inicia el viaje con la preparación elegida."""
        self.viaje_preparacion = preparacion
        region_destino = obtener_region(destino)
        
        prep_texto = ""
        if preparacion == "arma":
            prep_texto = " (armado)"
        elif preparacion == "dinero":
            prep_texto = " (con dinero)"
        
        self._narrar(f"\nTe diriges hacia {region_destino['nombre']}{prep_texto}...")
        self.root.after(1000, lambda: self._realizar_viaje(destino))

    def _realizar_viaje(self, destino: str):
        """Realiza el viaje y maneja encuentros."""
        resultado = realizar_viaje(
            self.personaje,
            destino,
            preparacion=self.viaje_preparacion
        )

        if resultado["estado"] == "encuentro":
            # Hay encuentro durante el viaje
            self.viaje_resultado = resultado
            self._mostrar_encuentro_viaje(resultado["encuentro"])
        else:
            # Viaje completado sin encuentros
            self.personaje = resultado["personaje"]
            self._narrar(resultado["texto"])
            self._actualizar_header()
            self._actualizar_barras()
            self.en_preparacion_viaje = False
            self.franja_actual += 1
            self.root.after(500, self._mostrar_franja)

    def _mostrar_encuentro_viaje(self, encuentro: dict):
        """Muestra un encuentro durante el viaje."""
        self._narrar(f"\n⚠️ {encuentro['texto']}\n")
        self._limpiar_botones()

        for i, opcion in enumerate(encuentro["opciones"]):
            btn = tk.Button(
                self.frame_botones,
                text=opcion["texto_boton"],
                bg=COLOR_BOTON, fg=COLOR_BOTON_TX,
                font=("Georgia", 10), relief="flat",
                padx=10, pady=6, cursor="hand2",
                command=lambda idx=i, enc=encuentro: self._resolver_encuentro_viaje(enc, idx),
            )
            btn.pack(fill="x", pady=2)

    def _resolver_encuentro_viaje(self, encuentro: dict, indice: int):
        """Resuelve el encuentro y completa el viaje."""
        opcion = encuentro["opciones"][indice]
        transformaciones = opcion.get("transformaciones", {})

        # Aplicar transformaciones del encuentro
        for clave, delta in transformaciones.items():
            if clave in self.personaje["condiciones"]:
                self.personaje["condiciones"][clave] = max(0.0, min(1.0,
                    self.personaje["condiciones"][clave] + delta))
            elif clave in self.personaje["social"]:
                if clave == "reputacion":
                    self.personaje["social"][clave] = max(-1.0, min(1.0,
                        self.personaje["social"][clave] + delta))
                else:
                    self.personaje["social"][clave] = max(0.0, min(1.0,
                        self.personaje["social"][clave] + delta))

        self._narrar(opcion["texto_resultado"])
        self._actualizar_barras()

        # Completar viaje
        resultado = completar_viaje_tras_encuentro(self.personaje, self.viaje_destino)
        self.personaje = resultado["personaje"]
        self._narrar(resultado["texto"])
        self._actualizar_header()
        self._actualizar_barras()

        self.en_preparacion_viaje = False
        self.franja_actual += 1
        self.root.after(500, self._mostrar_franja)

    def _fin_dia(self):
        """Cierra el día y avanza al siguiente."""
        self.personaje = avanzar_dia(self.personaje)
        
        # Actualizar región actual
        region = obtener_region(self.personaje["region"])
        region = actualizar_derivadas_region(region)
        self.personaje["contexto"] = obtener_contexto_personaje(region)
        
        self._actualizar_barras()
        self._limpiar_botones()

        if not esta_vivo(self.personaje):
            self._narrar("\n💀 Tu cuerpo no aguanta más. Tu historia termina aquí.")
            tk.Label(
                self.frame_botones, text="FIN DEL JUEGO",
                bg=COLOR_FONDO, fg="#7c4a4a",
                font=("Georgia", 14, "bold"),
            ).pack(pady=20)
            return

        btn = tk.Button(
            self.frame_botones,
            text="Siguiente día →",
            bg=COLOR_BOTON, fg=COLOR_BOTON_TX,
            font=("Georgia", 11), relief="flat",
            padx=10, pady=8, cursor="hand2",
            command=self._mostrar_estado_dia,
        )
        btn.pack(fill="x", pady=4)
