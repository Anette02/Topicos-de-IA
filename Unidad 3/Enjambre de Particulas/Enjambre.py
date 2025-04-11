import random
import matplotlib.pyplot as plt
import pandas as pd

# Clase Abejita  
class Abejita:
    def __init__(self, identificador, limite_x_min, limite_x_max, limite_y_min, limite_y_max):
        # Identificador de la abejita
        self.identificador = identificador

        # Posición inicial aleatoria dentro de los límites dados
        self.ubicacion = (
            random.uniform(limite_x_min, limite_x_max),
random.uniform(limite_y_min, limite_y_max)
        )

        # Velocidad inicial aleatoria positiva
        self.rapidez = round(random.uniform(0.1, 1.0), 2)

        # Historial: lista de ubicaciones por donde ha pasado
        self.historial = [self.ubicacion]

        # Coeficientes aleatorios
        self.coeficienteCognitivo = round(random.uniform(0.8, 2.0), 2)
        self.coeficienteSocial = round(random.uniform(0.8, 2.0), 2)

        # Coeficiente de inercia
        self.inercia = round(random.uniform(0.5, 1.0), 2)

    def actualizar_rapidez(self, nueva_rapidez):
        # Actualiza la rapidez considerando la inercia
        self.rapidez = round(self.inercia * self.rapidez + nueva_rapidez, 2)

# Clase Enjambre 
class Enjambre:
    def __init__(self, total_abejitas, limite_x_min, limite_x_max, limite_y_min, limite_y_max):
        self.abejitas = []

        # Crea la cantidad de abejitas solicitadas
        for indice in range(total_abejitas):
            abejita = Abejita(indice + 1, limite_x_min, limite_x_max, limite_y_min, limite_y_max)
            self.abejitas.append(abejita)

    # Genera DataFrame con los datos de las abejitas para mostrar en tabla
    def generar_dataframe(self):
        datos = {
            'Identificador': [],
            'Ubicación X': [],
            'Ubicación Y': [],
            'Rapidez': [],
            'Historial': [],
            'Coeficiente Cognitivo': [],
            'Coeficiente Social': []
        }

        # Extrae los datos de cada abejita
        for abejita in self.abejitas:
            datos['Identificador'].append(abejita.identificador)
            datos['Ubicación X'].append(round(abejita.ubicacion[0], 2))
            datos['Ubicación Y'].append(round(abejita.ubicacion[1], 2))
            datos['Rapidez'].append(abejita.rapidez)
            datos['Historial'].append(abejita.historial)
            datos['Coeficiente Cognitivo'].append(abejita.coeficienteCognitivo)
            datos['Coeficiente Social'].append(abejita.coeficienteSocial)

        return pd.DataFrame(datos)

    def actualizar_abejitas(self):
        for abejita in self.abejitas:
            # Ejemplo de actualización de rapidez con un valor aleatorio
            nueva_rapidez = random.uniform(0.1, 1.0)
            abejita.actualizar_rapidez(nueva_rapidez)

# Funciones de consola 
def crear_enjambre():
    try:
        # Solicita parámetros al usuario
        total_abejitas = int(input("Ingrese la cantidad de abejitas: "))
        limite_x_min = float(input("Ingrese el valor mínimo de X: "))
        limite_x_max = float(input("Ingrese el valor máximo de X: "))
        limite_y_min = float(input("Ingrese el valor mínimo de Y: "))
        limite_y_max = float(input("Ingrese el valor máximo de Y: "))

        # Crea el enjambre y obtener los datos
        enjambre = Enjambre(total_abejitas, limite_x_min, limite_x_max, limite_y_min, limite_y_max)
        dataframe = enjambre.generar_dataframe()

        # Actualiza las abejitas después de crearlas
        enjambre.actualizar_abejitas()

        # Muestra en consola
        print("\nDatos del enjambre:")
        print(dataframe)

        # Muestragráfica
        graficar_abejitas(enjambre)

    except Exception as error:
        print("Error:", error)

def graficar_abejitas(enjambre):
    # Obtiene coordenadas X e Y
    coordenadas_x = [abejita.ubicacion[0] for abejita in enjambre.abejitas]
    coordenadas_y = [abejita.ubicacion[1] for abejita in enjambre.abejitas]

    # Crea figura y ejes
    figura, ejes = plt.subplots(figsize=(6, 5))
    ejes.scatter(coordenadas_x, coordenadas_y, c='yellow') 

    # Etiqueta cada abejita con su identificador
    for abejita in enjambre.abejitas:
        ejes.text(abejita.ubicacion[0], abejita.ubicacion[1], str(abejita.identificador), fontsize=9)

    ejes.set_title("Ubicación de Abejitas")
    ejes.set_xlabel("X")
    ejes.set_ylabel("Y")
    ejes.grid(True)

    # Muestra la gráfica
    plt.show()

# Ejecuta la aplicación 
if __name__ == "__main__":
    crear_enjambre()
