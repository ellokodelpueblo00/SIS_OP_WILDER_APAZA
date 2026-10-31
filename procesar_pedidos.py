#  PRACTICA SIS OP Wilder Apaza
import threading
import queue
import time
import random
from datetime import datetime

pendientes = queue.Queue()
mutex = threading.Lock()
resumen = {}
registro = []

documentos = []
for i in range(1, 25):
    documentos.append((i, random.randint(1, 5)))

for d in documentos:
    pendientes.put(d)

def trabajador(nombre):
    while True:
        try:
            ident, tam = pendientes.get_nowait()
        except queue.Empty:
            with mutex:
                print(">>", nombre, "no encontro mas documentos y termina")
            break

        time.sleep(tam * 0.1)

        with mutex:
            resumen[nombre]["docs"] += 1
            resumen[nombre]["tamano"] += tam
            resumen[nombre]["ids"].append(ident)
            registro.append(ident)
lista_hilos = []
for n in range(1, 5):
    nombre = "Trabajador-" + str(n)
    resumen[nombre] = {"docs": 0, "tamano": 0, "ids": []}
    lista_hilos.append(threading.Thread(target=trabajador, args=(nombre,)))

hora_inicio = datetime.now()
for h in lista_hilos:
    h.start()
for h in lista_hilos:
    h.join()
duracion_hilos = (datetime.now() - hora_inicio).total_seconds()

print()
print("RESULTADOS")
print("-----------------------------------------")
print("Trabajador      Documentos   Tamano total   IDs")
for nombre in resumen:
    print(nombre, "     ", resumen[nombre]["docs"], "          ", resumen[nombre]["tamano"],
          "           ", resumen[nombre]["ids"])
print("-----------------------------------------")
print("Total procesado:", len(registro))
print("Orden en que salieron:", registro)
print("IDs repetidos?:", len(registro) != len(set(registro)))

hora_inicio = datetime.now()
for ident, tam in documentos:
    time.sleep(tam * 0.1)
duracion_secuencial = (datetime.now() - hora_inicio).total_seconds()

print()
print("Tiempo usando 4 hilos   =", duracion_hilos, "s")
print("Tiempo sin hilos        =", duracion_secuencial, "s")