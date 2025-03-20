import random
import math
import time

def calcular_conflictos(solucion):
    
    conflictos = 0
    n = len(solucion)
    for i in range(n):
        for j in range(i + 1, n):
            # Si la diferencia de columnas es igual a la diferencia de filas,
            # las reinas se atacan en diagonal.
            if abs(solucion[i] - solucion[j]) == abs(i - j):
                conflictos += 1
    return conflictos

def generar_vecino(solucion):
    
    vecino = solucion.copy()
    n = len(solucion)
    i, j = random.sample(range(n), 2)  # Escoge dos índices aleatorios
    vecino[i], vecino[j] = vecino[j], vecino[i]
    return vecino

def obtener_configuracion_usuario(n):
   
    entrada = input(f"Ingrese la configuración inicial de las reinas (ejemplo: 3,1,7,5,0,2,4,6): ")
    try:
        configuracion = [int(x.strip()) for x in entrada.split(',')]
        if len(configuracion) != n or sorted(configuracion) != list(range(n)):
            print("La configuración ingresada no es válida. Se usará una configuración aleatoria.")
            return None
        return configuracion
    except ValueError:
        print("Error al convertir la entrada a números enteros. Se usará una configuración aleatoria.")
        return None

def recocido_simulado(n, max_iter=10000, temp_inicial=100.0, temp_min=0.1, alpha=0.99, solucion_inicial=None):
    
    # Generar o usar la solución inicial
    if solucion_inicial is None:
        solucion_actual = list(range(n))
        random.shuffle(solucion_actual)
        config_inicial_utilizada = solucion_actual.copy()
    else:
        solucion_actual = solucion_inicial.copy()
        config_inicial_utilizada = solucion_actual.copy()
    
    costo_actual = calcular_conflictos(solucion_actual)
    
    # Guardamos la mejor solución encontrada
    mejor_solucion = solucion_actual.copy()
    mejor_conflicto = costo_actual
    
    temperatura = temp_inicial
    iteraciones = 0
    
    inicio_tiempo = time.time()  # Inicia el cronómetro
    
    # Bucle principal del recocido simulado
    while temperatura > temp_min and iteraciones < max_iter and mejor_conflicto != 0:
        iteraciones += 1
        
        # Generar un vecino a partir de la solución actual
        vecino = generar_vecino(solucion_actual)
        costo_vecino = calcular_conflictos(vecino)
        
        # Diferencia de costo entre el vecino y la solución actual
        delta = costo_vecino - costo_actual
        
        # Aceptar el vecino si mejora la solución, o con cierta probabilidad
        if delta < 0 or random.random() < math.exp(-delta / temperatura):
            solucion_actual = vecino
            costo_actual = costo_vecino
        
        # Actualizar la mejor solución si se encuentra una mejor
        if costo_actual < mejor_conflicto:
            mejor_solucion = solucion_actual.copy()
            mejor_conflicto = costo_actual
        
        # Imprimir información de la iteración actual
        print(f"Iteración {iteraciones}: Conflictos = {costo_actual} | Configuración = {solucion_actual}")
        
        # Enfriar la temperatura
        temperatura *= alpha
    
    fin_tiempo = time.time()  # Detiene el cronómetro
    tiempo_transcurrido = fin_tiempo - inicio_tiempo
    
    return mejor_solucion, mejor_conflicto, iteraciones, tiempo_transcurrido, config_inicial_utilizada

if __name__ == '__main__':
    n = 8  # Número de reinas para el problema de 8 reinas
    
    # Menú para elegir el tipo de configuración inicial
    print("Seleccione una opción para la configuración inicial:")
    print("1. Generar configuración aleatoria")
    print("2. Ingresar manualmente la configuración")
    
    opcion = input("Ingrese 1 o 2: ").strip()
    if opcion == "2":
        configuracion = obtener_configuracion_usuario(n)
        if configuracion is None:
            configuracion = None
    else:
        configuracion = None
    
    # Ejecutar el algoritmo de recocido simulado
    solucion, conflictos, iteraciones, tiempo, config_inicial_utilizada = recocido_simulado(n, solucion_inicial=configuracion)
    
    # Mostrar los resultados finales
    print("\nResultado del recocido simulado para el problema de las 8 reinas:")
    print("Configuración inicial utilizada:", config_inicial_utilizada)
    print("Mejor solución encontrada:", solucion)
    print("Número de conflictos:", conflictos)
    print("Número de iteraciones:", iteraciones)
    print("Tiempo transcurrido (segundos):", tiempo)