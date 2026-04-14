"""
Interfaz tkinter del juego.
Zona superior: narración del día.
Zona media: estado visible del personaje.
Zona inferior: botones de acciones contextuales.
"""

import tkinter as tk
from tkinter import scrolledtext
from core.motor import avanzar_dia, esta_vivo
from core.modulos import modulos_disponibles, aplicar_opcion
from data.modulos_data import MODULOS

FRANJAS = ["mañana", "mediodia", "tarde", "noche"]

COLOR_FONDO    = "#1a1a1a"
COLOR_TEXTO    = "#d4c5a9"
COLOR_BOTON    = "#3a2e1e"
COLOR_BOTON_TX = "#d4c5a9"
COLOR_BARRA_OK = "#4a7c4e"
COLOR_BARRA_MAL= "#7c4a4a"


class Interfaz:
    def __init__(self, root: tk.Tk, personaje: dict):
        self.root = root
        self.personaje = personaje
        self.franja_actual = 0  # índice en FRANJAS

        self.root.title("Vida Medieval")
        self.root.configure(bg=COLOR_FONDO)
        self.root.geometry("700x600")

        self._construir_ui()
        self._mostrar_estado_dia()

    def _construir_ui(self):
        # zona narración
        self.texto_narracion = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, height=14,
            bg="#0d0d0d", fg=COLOR_TEXTO,
            font=("Georgia", 11), state="disabled",
            relief="flat", padx=10, pady=10,
        )
        self.texto_narracion.pack(fill="x", padx=10, pady=(10, 0))

        # zona estado
        self.frame_estado = tk.Frame(self.root, bg=COLOR_FONDO)
        self.frame_estado.pack(fill="x", padx=10, pady=6)
        self.labels_estado = {}
        self._construir_barras_estado()

        # zona botones
        self.frame_botones = tk.Frame(self.root, bg=COLOR_FONDO)
        self.frame_botones.pack(fill="both", expand=True, padx=10, pady=6)

    def _construir_barras_estado(self):
        variables = [
            ("Vitalidad",   "vitalidad",    None),
            ("Nutrición",   "nutricion",    "condiciones"),
            ("Descanso",    "descanso",     "condiciones"),
            ("Salud física","salud_fisica", "estado"),
            ("Salud mental","salud_mental", "estado"),
            ("Riqueza",     "riqueza",      "social"),
        ]
        for i, (etiqueta, clave, fuente) in enumerate(variables):
            col = i % 3
            row = i // 3
            frame = tk.Frame(self.frame_estado, bg=COLOR_FONDO)
            frame.grid(row=row, column=col, padx=6, pady=2, sticky="w")
            tk.Label(frame, text=etiqueta, bg=COLOR_FONDO, fg=COLOR_TEXTO,
                     font=("Georgia", 9)).pack(anchor="w")
            canvas = tk.Canvas(frame, width=160, height=10,
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
            canvas.create_rectangle(0, 0, int(160 * valor), 10, fill=color, outline="")

    def _narrar(self, texto: str):
        self.texto_narracion.configure(state="normal")
        self.texto_narracion.insert("end", texto + "\n\n")
        self.texto_narracion.see("end")
        self.texto_narracion.configure(state="disabled")

    def _limpiar_botones(self):
        for widget in self.frame_botones.winfo_children():
            widget.destroy()

    def _mostrar_estado_dia(self):
        """Muestra el encabezado del día y lanza la primera franja."""
        p = self.personaje
        self._narrar(
            f"── Día {p['dia']} ── {p['nombre']}, {p['edad']} años ──\n"
            f"Región: {p['region']}  |  Linaje: {p['linaje']}"
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

        self._limpiar_botones()

        if not disponibles:
            # sin módulos en esta franja, avanzar automáticamente
            self._narrar(f"[{franja.upper()}] Nada especial ocurre.")
            self.franja_actual += 1
            self.root.after(800, self._mostrar_franja)
            return

        # mostrar el primer módulo disponible (el más relevante)
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
        """Aplica la opción elegida y avanza a la siguiente franja."""
        self.personaje, resultado = aplicar_opcion(self.personaje, modulo, indice)
        self._narrar(resultado)
        self._actualizar_barras()
        self.franja_actual += 1
        self._mostrar_franja()

    def _fin_dia(self):
        """Cierra el día: aplica degradación, recalcula derivadas, comprueba muerte."""
        self.personaje = avanzar_dia(self.personaje)
        self._actualizar_barras()
        self._limpiar_botones()

        if not esta_vivo(self.personaje):
            self._narrar("Tu cuerpo no aguanta más. Tu historia termina aquí.")
            tk.Label(
                self.frame_botones, text="FIN",
                bg=COLOR_FONDO, fg="#7c4a4a",
                font=("Georgia", 16),
            ).pack()
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
