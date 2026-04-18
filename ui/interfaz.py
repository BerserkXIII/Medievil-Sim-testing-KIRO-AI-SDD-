"""
Game UI: main game loop with travel, encounters, and events.
"""

import tkinter as tk
from tkinter import scrolledtext
from core.motor import avanzar_dia, esta_vivo, actualizar_derivadas_region
from core.modulos import modulos_disponibles, aplicar_opcion
from core.viaje import realizar_viaje, completar_viaje_tras_encuentro, preparar_viaje
from core.mundo import obtener_contexto_personaje
from data.modulos_data import MODULOS
from data.encuentros_viaje_data import generar_modulos_viaje
from data.regiones_data import obtener_region

FRANJAS = ["mañana", "mediodia", "tarde", "noche"]

COLOR_FONDO    = "#1a1a1a"
COLOR_TEXTO    = "#d4c5a9"
COLOR_BOTON    = "#3a2e1e"
COLOR_BOTON_TX = "#d4c5a9"
COLOR_BARRA_OK = "#4a7c4e"
COLOR_BARRA_MAL= "#7c4a4a"
COLOR_TITULO   = "#c9a961"


class Interfaz:
    def __init__(self, root: tk.Tk, personaje: dict):
        self.root = root
        self.personaje = personaje
        self.franja_actual = 0
        self.en_viaje = False
        self.viaje_destino = None
        self.viaje_resultado = None

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
        """Muestra los módulos disponibles para la franja actual."""
        if self.franja_actual >= len(FRANJAS):
            self._fin_dia()
            return

        franja = FRANJAS[self.franja_actual]
        disponibles = modulos_disponibles(self.personaje, franja, MODULOS)

        # Añadir módulos de viaje en mediodía
        if franja == "mediodia":
            modulos_viaje = generar_modulos_viaje(self.personaje["region"])
            disponibles.extend(modulos_viaje)

        self._limpiar_botones()

        if not disponibles:
            self._narrar(f"[{franja.upper()}] Nada especial ocurre.")
            self.franja_actual += 1
            self.root.after(800, self._mostrar_franja)
            return

        # Mostrar primer módulo
        modulo = disponibles[0]
        self._narrar(f"[{franja.upper()}] {modulo['texto']}")

        for i, opcion in enumerate(modulo["opciones"]):
            btn = tk.Button(
                self.frame_botones,
                text=opcion["texto_boton"],
                bg=COLOR_BOTON, fg=COLOR_BOTON_TX,
                font=("Georgia", 10), relief="flat",
                padx=10, pady=6, cursor="hand2",
                command=lambda idx=i, m=modulo: self._elegir_opcion(m, idx),
            )
            btn.pack(fill="x", pady=2)

    def _elegir_opcion(self, modulo: dict, indice: int):
        """Aplica la opción elegida."""
        opcion = modulo["opciones"][indice]
        transformaciones = opcion.get("transformaciones", {})

        # Detectar si es un viaje
        if "_viaje" in transformaciones:
            destino = transformaciones["_viaje"]
            self._iniciar_viaje(destino)
            return

        # Aplicar transformación normal
        self.personaje, resultado = aplicar_opcion(self.personaje, modulo, indice)
        self._narrar(resultado)
        self._actualizar_barras()
        self.franja_actual += 1
        self.root.after(500, self._mostrar_franja)

    def _iniciar_viaje(self, destino: str):
        """Inicia un viaje a destino."""
        self._narrar(f"Te diriges hacia {obtener_region(destino)['nombre']}...")
        self.root.after(1000, lambda: self._realizar_viaje(destino))

    def _realizar_viaje(self, destino: str):
        """Realiza el viaje y maneja encuentros."""
        resultado = realizar_viaje(self.personaje, destino, preparacion=None)

        if resultado["estado"] == "encuentro":
            # Hay encuentro durante el viaje
            self.en_viaje = True
            self.viaje_destino = destino
            self.viaje_resultado = resultado
            self._mostrar_encuentro_viaje(resultado["encuentro"])
        else:
            # Viaje completado sin encuentros
            self.personaje = resultado["personaje"]
            self._narrar(resultado["texto"])
            self._actualizar_barras()
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

        self.en_viaje = False
        self.franja_actual += 1
        self.root.after(500, self._mostrar_franja)

    def _fin_dia(self):
        """Cierra el día."""
        self.personaje = avanzar_dia(self.personaje)
        
        # Actualizar contexto de la región
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
