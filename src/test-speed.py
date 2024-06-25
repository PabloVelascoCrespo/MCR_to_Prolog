import concurrent.futures
import time

# Función simulada que imita una tarea costosa (por ejemplo, una pausa)
def tarea_costosa(n):
    time.sleep(0.1)  # Simula una tarea que tarda 0.1 segundos
    return n * n

# Lista de entradas para procesar
entradas = list(range(100))

# Probar con diferentes números de hilos
numeros_de_hilos = [64]
tiempos_de_ejecucion = []

for numero_hilos in numeros_de_hilos:
    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=numero_hilos) as executor:
        # Ejecutar la función tarea_costosa en varios hilos
        futuros = [executor.submit(tarea_costosa, entrada) for entrada in entradas]

        # Obtener los resultados conforme se vayan completando
        resultados = [futuro.result() for futuro in concurrent.futures.as_completed(futuros)]

    end_time = time.time()
    tiempo_ejecucion = end_time - start_time
    tiempos_de_ejecucion.append((numero_hilos, tiempo_ejecucion))
    print(f"Tiempo de ejecución con {numero_hilos} hilos: {tiempo_ejecucion:.2f} segundos")

# Imprimir los resultados de los tiempos de ejecución
for numero_hilos, tiempo_ejecucion in tiempos_de_ejecucion:
    print(f"{numero_hilos} hilos: {tiempo_ejecucion:.2f} segundos")
