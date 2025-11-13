import tkinter as tk
from tkinter import ttk, messagebox
import math
import pygame
from threading import Thread
import time
import os

# --- Clase Barco ---
class Barco:
    def __init__(self, nombre, posicionX, posicionY, velocidad, rumbo, numeroMunicion):
        self.nombre = nombre
        self.posicionX = posicionX
        self.posicionY = posicionY
        self.velocidad = velocidad
        self.rumbo = rumbo
        self.numeroMunicion = numeroMunicion

    def disparar(self):
        if self.numeroMunicion > 0:
            self.numeroMunicion -= 1
            print(f"{self.nombre} disparó. Munición restante: {self.numeroMunicion}")
            return True
        else:
            print(f"{self.nombre} no tiene munición.")
            return False

    def setVelocidad(self, nueva_velocidad):
        self.velocidad = nueva_velocidad

    def setRumbo(self, nuevo_rumbo):
        self.rumbo = nuevo_rumbo


# --- Clase principal ---
class App:    
    def __init__(self, root):
        self.root = root
        self.root.title("⚓ Simulador de Barcos")
        self.root.geometry("900x600")

        # --- Inicializar sonido con ruta segura ---
        pygame.mixer.init()
        carpeta_script = os.path.dirname(os.path.abspath(__file__))

        # Música de fondo
        try:
            pygame.mixer.music.load(os.path.join(carpeta_script, "fondo.mp3"))
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.5)
        except:
            print("❌ No se encontró fondo.mp3 en la carpeta del script")

        # Sonido de disparo
        try:
            self.sonido_disparo = pygame.mixer.Sound(os.path.join(carpeta_script, "disparo.mp3"))
            self.sonido_disparo.set_volume(0.8)
        except:
            self.sonido_disparo = None
            print("❌ No se encontró disparo.wav en la carpeta del script")

        # --- Canvas ---
        self.canvas = tk.Canvas(root, bg="lightblue", width=650, height=550)
        self.canvas.pack(side="left", fill="both", expand=True)

        # --- Panel lateral ---
        control = tk.Frame(root, padx=10, pady=10)
        control.pack(side="right", fill="y")

        ttk.Label(control, text="Seleccionar Barco:").pack(pady=5)
        self.selector_barco = ttk.Combobox(control, state="readonly")
        self.selector_barco.pack(pady=5)

        ttk.Button(control, text="➕ Crear Barco", command=self.crear_barco).pack(pady=10)
        ttk.Button(control, text="🚀 Aumentar Velocidad", command=self.aumentar_velocidad).pack(pady=5)
        ttk.Button(control, text="🐢 Disminuir Velocidad", command=self.disminuir_velocidad).pack(pady=5)
        ttk.Button(control, text="🧭 Cambiar Rumbo", command=self.cambiar_rumbo).pack(pady=5)
        ttk.Button(control, text="💥 Disparar", command=self.disparar).pack(pady=10)

        # --- Listas de barcos ---
        self.barcos = []
        self.iconos = {}

        # --- Movimiento automático ---
        self.movimiento_activo = True
        Thread(target=self.mover_barcos, daemon=True).start()

        # --- Controles por teclado ---
        root.bind("<Up>", self.mover_adelante)
        root.bind("<Down>", self.mover_atras)
        root.bind("<Left>", self.girar_izquierda)
        root.bind("<Right>", self.girar_derecha)

    # --- Crear barco ---
    def crear_barco(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Nuevo Barco")

        labels = ["Nombre","X","Y","Velocidad","Rumbo","Munición"]
        entradas = {}
        for i, l in enumerate(labels):
            tk.Label(ventana, text=l+":").grid(row=i,column=0)
            e = tk.Entry(ventana)
            e.grid(row=i,column=1)
            entradas[l] = e

        def guardar():
            try:
                b = Barco(
                    entradas["Nombre"].get(),
                    float(entradas["X"].get()),
                    float(entradas["Y"].get()),
                    float(entradas["Velocidad"].get()),
                    float(entradas["Rumbo"].get()),
                    int(entradas["Munición"].get())
                )
                self.barcos.append(b)
                barco_id = self.canvas.create_text(b.posicionX,b.posicionY,text="▲", font=("Arial",20))
                self.iconos[b] = barco_id
                self.actualizar_selector()
                ventana.destroy()
            except:
                messagebox.showerror("Error","Datos inválidos")
        ttk.Button(ventana,text="Guardar",command=guardar).grid(row=6,column=0,columnspan=2,pady=10)

    # --- Selector ---
    def actualizar_selector(self):
        self.selector_barco["values"] = [b.nombre for b in self.barcos]
        if self.barcos:
            self.selector_barco.current(0)

    def obtener_barco(self):
        if not self.barcos:
            messagebox.showwarning("Atención","No hay barcos")
            return None
        nombre = self.selector_barco.get()
        for b in self.barcos:
            if b.nombre==nombre:
                return b
        return None

    # --- Botones ---
    def aumentar_velocidad(self):
        b = self.obtener_barco()
        if b:
            b.setVelocidad(b.velocidad+1)
    def disminuir_velocidad(self):
        b = self.obtener_barco()
        if b and b.velocidad>0:
            b.setVelocidad(b.velocidad-1)
    def cambiar_rumbo(self):
        b = self.obtener_barco()
        if b:
            b.setRumbo((b.rumbo+45)%360)
    def disparar(self):
        b = self.obtener_barco()
        if b:
            exito = b.disparar()
            if exito and self.sonido_disparo:
                self.sonido_disparo.play()

    # --- Movimiento automático ---
    def mover_barcos(self):
        while self.movimiento_activo:
            for b in self.barcos:
                rad = math.radians(b.rumbo)
                b.posicionX += math.cos(rad)*b.velocidad*0.5
                b.posicionY += math.sin(rad)*b.velocidad*0.5
                self.actualizar_icono(b)
            time.sleep(0.1)

    def actualizar_icono(self,b):
        r = b.rumbo%360
        if 45<=r<135:
            simbolo="▶"
        elif 135<=r<225:
            simbolo="▼"
        elif 225<=r<315:
            simbolo="◀"
        else:
            simbolo="▲"
        self.canvas.itemconfig(self.iconos[b], text=simbolo)
        self.canvas.coords(self.iconos[b], b.posicionX, b.posicionY)

    # --- Control por teclado ---
    def mover_adelante(self,event):
        b = self.obtener_barco()
        if b:
            rad=math.radians(b.rumbo)
            b.posicionX += math.cos(rad)*10
            b.posicionY += math.sin(rad)*10
            self.actualizar_icono(b)
    def mover_atras(self,event):
        b = self.obtener_barco()
        if b:
            rad=math.radians(b.rumbo)
            b.posicionX -= math.cos(rad)*10
            b.posicionY -= math.sin(rad)*10
            self.actualizar_icono(b)
    def girar_izquierda(self,event):
        b = self.obtener_barco()
        if b:
            b.setRumbo((b.rumbo-10)%360)
    def girar_derecha(self,event):
        b = self.obtener_barco()
        if b:
            b.setRumbo((b.rumbo+10)%360)


# --- Ejecutar ---
if __name__=="__main__":
    root=tk.Tk()
    app=App(root)
    root.mainloop()
