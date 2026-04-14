"""
Punto de entrada del juego.
Pantalla de creación de personaje → loop principal.
"""

import tkinter as tk
from tkinter import ttk
from core.personaje import crear_personaje
from data.linajes_data import LINAJES
from ui.interfaz import Interfaz


COLOR_FONDO = "#1a1a1a"
COLOR_TEXTO = "#d4c5a9"
COLOR_BOTON = "#3a2e1e"


def pantalla_creacion(root: tk.Tk):
    """Pantalla inicial de creación de personaje."""
    root.title("Vida Medieval - Nuevo personaje")
    root.configure(bg=COLOR_FONDO)
    root.geometry("420x380")

    def label(texto, row):
        tk.Label(frame, text=texto, bg=COLOR_FONDO, fg=COLOR_TEXTO,
                 font=("Georgia", 10)).grid(row=row, column=0, sticky="w", pady=4)

    frame = tk.Frame(root, bg=COLOR_FONDO, padx=30, pady=20)
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="Tu historia comienza aquí",
             bg=COLOR_FONDO, fg=COLOR_TEXTO,
             font=("Georgia", 14)).grid(row=0, column=0, columnspan=2, pady=(0, 16))

    label("Nombre:", 1)
    entrada_nombre = tk.Entry(frame, bg="#2a2a2a", fg=COLOR_TEXTO,
                               font=("Georgia", 10), relief="flat", insertbackground=COLOR_TEXTO)
    entrada_nombre.insert(0, "Aldric")
    entrada_nombre.grid(row=1, column=1, sticky="ew", padx=(10, 0))

    label("Sexo:", 2)
    sexo_var = tk.StringVar(value="hombre")
    frame_sexo = tk.Frame(frame, bg=COLOR_FONDO)
    frame_sexo.grid(row=2, column=1, sticky="w", padx=(10, 0))
    for s in ["hombre", "mujer"]:
        tk.Radiobutton(frame_sexo, text=s.capitalize(), variable=sexo_var, value=s,
                       bg=COLOR_FONDO, fg=COLOR_TEXTO, selectcolor="#2a2a2a",
                       font=("Georgia", 10)).pack(side="left", padx=4)

    label("Edad:", 3)
    edad_var = tk.IntVar(value=18)
    tk.Spinbox(frame, from_=10, to=60, textvariable=edad_var,
               bg="#2a2a2a", fg=COLOR_TEXTO, font=("Georgia", 10),
               relief="flat", buttonbackground="#2a2a2a").grid(row=3, column=1, sticky="w", padx=(10, 0))

    label("Región:", 4)
    region_var = tk.StringVar(value="aldea")
    ttk.Combobox(frame, textvariable=region_var,
                 values=["aldea", "ciudad", "frontera", "bosque", "camino"],
                 state="readonly", font=("Georgia", 10)).grid(row=4, column=1, sticky="ew", padx=(10, 0))

    label("Linaje:", 5)
    linaje_var = tk.StringVar(value="campesino")
    ttk.Combobox(frame, textvariable=linaje_var,
                 values=list(LINAJES.keys()),
                 state="readonly", font=("Georgia", 10)).grid(row=5, column=1, sticky="ew", padx=(10, 0))

    frame.columnconfigure(1, weight=1)

    def iniciar():
        nombre = entrada_nombre.get().strip() or "Desconocido"
        linaje = LINAJES[linaje_var.get()]
        personaje = crear_personaje(
            nombre=nombre,
            sexo=sexo_var.get(),
            edad=edad_var.get(),
            region=region_var.get(),
            linaje=linaje,
        )
        for widget in root.winfo_children():
            widget.destroy()
        root.geometry("700x600")
        Interfaz(root, personaje)

    tk.Button(frame, text="Comenzar →",
              bg=COLOR_BOTON, fg=COLOR_TEXTO,
              font=("Georgia", 11), relief="flat",
              padx=10, pady=6, cursor="hand2",
              command=iniciar).grid(row=6, column=0, columnspan=2, pady=16, sticky="ew")


if __name__ == "__main__":
    root = tk.Tk()
    pantalla_creacion(root)
    root.mainloop()
