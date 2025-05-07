import networkx as nx

# Creación del grafo
G = nx.Graph()

aristas = [
    ("Vigo", "Valladolid", 356),
    ("Valladolid", "Bilbao", 280), ("Valladolid", "Madrid", 193),
    ("Bilbao", "Zaragoza", 324), ("Zaragoza", "Madrid", 325), ("Bilbao", "Madrid", 395),
    ("Zaragoza", "Barcelona", 296), ("Barcelona", "Gerona", 100),
    ("Barcelona", "Valencia", 349), ("Valencia", "Albacete", 191),
    ("Albacete", "Madrid", 251), ("Albacete", "Murcia", 241),
    ("Murcia", "Granada", 278), ("Granada", "Jaén", 99),
    ("Jaén", "Sevilla", 242), ("Sevilla", "Cádiz", 125), ("Sevilla", "Granada", 256),
    ("Badajoz", "Madrid", 403),
    ("Jaén", "Madrid", 335)
]

G.add_weighted_edges_from(aristas)

def vecino_mas_cercano_rapido(grafo, inicio):
    ciudades = set(grafo.nodes)
    visitados = set([inicio])
    ruta = [inicio]
    distancia_total = 0
    actual = inicio

    # Se para el bucle infinito
    max_pasos = 100
    pasos = 0

    while visitados != ciudades and pasos < max_pasos:
        vecinos = list(grafo.neighbors(actual))
        vecinos.sort(key=lambda x: grafo[actual][x]['weight'])

        encontrado = False
        for vecino in vecinos:
            # Evita regresar a la ciudad anterior
            if vecino not in visitados and (actual != "Sevilla" or vecino != "Cádiz"):
                distancia = grafo[actual][vecino]['weight']
                distancia_total += distancia
                ruta.append(vecino)
                visitados.add(vecino)
                actual = vecino
                encontrado = True
                break

        # Si todos los vecinos ya han sido visitados, encunentra el vecino más cercano
        if not encontrado:
            vecino = vecinos[0]
            distancia = grafo[actual][vecino]['weight']
            distancia_total += distancia
            ruta.append(vecino)
            actual = vecino

        pasos += 1

    return ruta, distancia_total

# Ejecuta el algoritmo
ruta, distancia = vecino_mas_cercano_rapido(G, "Madrid")

print("Ruta encontrada:")
print(" -> ".join(ruta))
print(f"Distancia total: {distancia} km")
