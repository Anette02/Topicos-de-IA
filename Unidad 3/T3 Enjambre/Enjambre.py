# Importar las bibliotecas necesarias
import random
import matplotlib.pyplot as plt
import pandas as pd

# Clase Particula 
class Particula:
    def __init__(self, id_particula, rango_x_min, rango_x_max, rango_y_min, rango_y_max):
        # Inicializar los atributos de la partícula
        self.id_particula = id_particula
        self.posicion_actual = (
            random.uniform(rango_x_min, rango_x_max),
            random.uniform(rango_y_min, rango_y_max)
        )
        self.velocidad = round(random.uniform(0.1, 1.0), 2)
        self.trayectoria = [self.posicion_actual]
        self.cognitivo = round(random.uniform(0.5, 2.0), 2)
        self.social = round(random.uniform(0.5, 2.0), 2)

        # Configura la mejor posición personal y su evaluación inicial
        self.mejor_posicion = self.posicion_actual
        self.mejor_valor = self.evaluar(self.posicion_actual)

    # Evalúa la posición actual de la partícula
    def evaluar(self, posicion):
        x, y = posicion
        return x**2 + y**2

    # Actualiza la posición y velocidad de la partícula
    def actualizar(self, mejor_global):
        # Calcula la nueva velocidad usando factores cognitivo y social
        aleatorio1 = random.random()
        aleatorio2 = random.random()

        nueva_vel_x = (self.velocidad * aleatorio1 * self.cognitivo +
                      (mejor_global[0] - self.posicion_actual[0]) * aleatorio2 * self.social)
        nueva_vel_y = (self.velocidad * aleatorio1 * self.cognitivo +
                      (mejor_global[1] - self.posicion_actual[1]) * aleatorio2 * self.social)

        # Actualiza la posición con la nueva velocidad
        nueva_x = self.posicion_actual[0] + nueva_vel_x
        nueva_y = self.posicion_actual[1] + nueva_vel_y
        self.posicion_actual = (nueva_x, nueva_y)

        # Guarda la nueva posición en el historial
        self.trayectoria.append(self.posicion_actual)

        # Verifica si la nueva posición es la mejor personal
        valor_actual = self.evaluar(self.posicion_actual)
        if valor_actual < self.mejor_valor:
            self.mejor_valor = valor_actual
            self.mejor_posicion = self.posicion_actual

# Clase Enjambre
class Enjambre:
    def __init__(self, num_particulas, rango_x_min, rango_x_max, rango_y_min, rango_y_max):
        # Crear una lista de partículas
        self.particulas = []

        for i in range(num_particulas):
            particula = Particula(i + 1, rango_x_min, rango_x_max, rango_y_min, rango_y_max)
            self.particulas.append(particula)

    # Genera un DataFrame con los datos de las partículas
    def generar_dataframe(self):
        datos = {
            'ID': [],
            'Posición X': [],
            'Posición Y': [],
            'Velocidad': [],
            'Trayectoria': [],
            'Cognitivo': [],
            'Social': [],
            'Mejor Valor': []
        }

        for particula in self.particulas:
            datos['ID'].append(particula.id_particula)
            datos['Posición X'].append(round(particula.posicion_actual[0], 2))
            datos['Posición Y'].append(round(particula.posicion_actual[1], 2))
            datos['Velocidad'].append(particula.velocidad)
            datos['Trayectoria'].append(len(particula.trayectoria))  # Número de posiciones registradas
            datos['Cognitivo'].append(particula.cognitivo)
            datos['Social'].append(particula.social)
            datos['Mejor Valor'].append(round(particula.mejor_valor, 4))

        return pd.DataFrame(datos)

    # Obtiene la mejor posición global entre todas las partículas
    def obtener_mejor_global(self):
        mejor_particula = min(self.particulas, key=lambda p: p.mejor_valor)
        return mejor_particula.mejor_posicion

    # Actualiza todas las partículas del enjambre
    def actualizar_particulas(self):
        mejor_global = self.obtener_mejor_global()
        for particula in self.particulas:
            particula.actualizar(mejor_global)

    # Muestra un gráfico con las posiciones actuales de las partículas
    def graficar(self):
        x_vals = [p.posicion_actual[0] for p in self.particulas]
        y_vals = [p.posicion_actual[1] for p in self.particulas]

        fig, ax = plt.subplots(figsize=(6, 5))
        ax.scatter(x_vals, y_vals, c='blue')

        for p in self.particulas:
            ax.text(p.posicion_actual[0], p.posicion_actual[1], str(p.id_particula), fontsize=9)

        ax.set_title("Posición de Partículas")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.grid(True)

        plt.show()

# Ejecuta el programa 
if __name__ == "__main__":
    print("Simulación de Enjambre de Partículas")

    try:
        # Solicita parámetros iniciales al usuario
        num_particulas = int(input("Ingrese la cantidad de partículas: "))
        rango_x_min = float(input("Ingrese el valor mínimo de X: "))
        rango_x_max = float(input("Ingrese el valor máximo de X: "))
        rango_y_min = float(input("Ingrese el valor mínimo de Y: "))
        rango_y_max = float(input("Ingrese el valor máximo de Y: "))

        # Crea el enjambre con los parámetros proporcionados
        enjambre = Enjambre(num_particulas, rango_x_min, rango_x_max, rango_y_min, rango_y_max)

        while True:
            # Muestra el menú de opciones
            print("\nOpciones:")
            print("1. Mostrar datos del enjambre")
            print("2. Actualizar partículas")
            print("3. Graficar partículas")
            print("4. Salir")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                # Muestra los datos actuales del enjambre
                df = enjambre.generar_dataframe()
                print(df)

            elif opcion == "2":
                # Actualiza las posiciones de las partículas
                enjambre.actualizar_particulas()
                print("Partículas actualizadas.")

            elif opcion == "3":
                # Genera un gráfico con las posiciones de las partículas
                enjambre.graficar()

            elif opcion == "4":
                print("Saliendo del programa.")
                break

            else:
                print("Opción no válida. Intente de nuevo.")

    except Exception as e:
        print("Error:", e)
