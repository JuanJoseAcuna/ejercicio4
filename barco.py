class Barco:
    def __init__(self, nombre, posicionX, posicionY, velocidad, rumbo, numeroMunicion):
        self.nombre = nombre
        self.posicionX = posicionX
        self.posicionY = posicionY
        self.velocidad = velocidad
        self.rumbo = rumbo
        self.numeroMunicion = numeroMunicion
    def __str__(self):
        return (f"Barco '{self.nombre}':\n"
                f"  la posición es X: {self.posicionX}, Y: {self.posicionY}\n"
                f"  la velocidad es {self.velocidad} km/h\n"
                f"  el rumbo es {self.rumbo}°\n"
                f"  tiene {self.numeroMunicion} proyectiles\n")
    def disparar(self):
        if self.numeroMunicion > 0:
            self.numeroMunicion -= 1
            print(f"{self.nombre} disparó y su munición es {self.numeroMunicion}")
        else:
            print(f"{self.nombre} no tiene munición para disparar.")
    def setVelocidad(self, nueva_velocidad):
        self.velocidad = nueva_velocidad
        print(f"La nueva velocidad de {self.nombre} es {self.velocidad} km/h")

    def setRumbo(self, nuevo_rumbo):
        self.rumbo = nuevo_rumbo
        print(f"El nuevo rumbo de {self.nombre} es {self.rumbo}°")
barco1 = Barco("Perla", 1009, 2400, 10, 90, 5)
barco2 = Barco("Camaron", 503, 75, 15, 180, 3)
barco3 = Barco("La Niña", 10, 10, 5, 270, 2)
for barco in [barco1, barco2, barco3]:
    print("=================================")
    print("INICIAL")
    print(barco)
    barco.disparar()
    barco.disparar()
    barco.setVelocidad(barco.velocidad + 2)
    barco.setRumbo((barco.rumbo + 45) % 360)
    print("\nFINAL")
    print(barco)
