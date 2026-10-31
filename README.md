# Práctica 1 – Hilos con Python

Nombre: **Wilder Apaza**

En esta práctica hice un programa con 4 trabajadores que se reparten 24 documentos, cada documento tiene un id y un tamaño al azar entre 1 y 5

- Primero pongo todos los documentos en una `queue.Queue`.
- Cada trabajador toma uno con `get_nowait()` y lo procesa. Cuando ya no quedan documentos, sale `queue.Empty` y el hilo termina.
- Uso `time.sleep(tam * 0.1)` para simular lo que tarda en procesarse cada documento.
- Los resultados se guardan en `resumen` y `registro`, dentro de `with mutex:`.
- Al final hago `join()` a los 4 hilos para esperar a que terminen y mostrar la tabla.

## Interpretación de cada ejecución

En las cuatro ejecuciones se procesaron los 24 documentos, no hubo ids repetidos y los 4 hilos terminaron. Lo que cambia entre una ejecución y otra es el reparto del trabajo.

**Ejecución 1:** Trabajador-1 hizo 5 documentos, Trabajador-2 y Trabajador-3 hicieron 6 cada uno, y Trabajador-4 hizo 7. El último hizo más documentos, pero su tamaño total fue 16. Le tocaron varios pequeños, así que podía terminar y tomar otro más rápido.

**Ejecución 2:** Todos hicieron 6 documentos. Esta vez salió parejo en cantidad, aunque los tamaños totales fueron 19, 16, 18 y 16. Hacer la misma cantidad no significa que todos hayan tenido exactamente el mismo trabajo.

**Ejecución 3:** Trabajador-1 hizo 6 documentos, Trabajador-2 y Trabajador-3 hicieron 7 cada uno, y Trabajador-4 solo hizo 4. Pero Trabajador-4 sumó un tamaño de 15, igual que Trabajador-1 con sus 6 documentos. O sea, hizo menos porque sus documentos eran más grandes en promedio.

**Ejecución 4:** Trabajador-1 hizo 7 documentos, Trabajador-2 hizo 6, Trabajador-3 hizo 5 y Trabajador-4 hizo 6. Sus tamaños totales fueron 21, 20, 21 y 24. En esta ejecución hubo más trabajo que en las anteriores y el tiempo con hilos fue de 2.41 segundos.

**Lo que entendí:** no hay un trabajador que siempre haga más. Cuando uno termina toma el siguiente documento disponible por eso el reparto depende del tamaño que le toca y de cómo el sistema operativo ejecuta los hilos

## Reto adicional

Para comparar los tiempos usé `datetime.now()` antes y después del procesamiento también mostré el tamaño total de los documentos que hizo cada trabajador

La versión sin hilos recorre los mismos documentos con un `for` y hace el mismo `sleep` pero uno después de otro

| Ejecución | 4 hilos | Sin hilos |
|-----------|---------|-----------|
| 1 | 1.71 s | 6.61 s |
| 2 | 1.91 s | 6.91 s |
| 3 | 1.71 s | 6.31 s |
| 4 | 2.41 s | 8.61 s |

Con hilos tardó bastante menos: fue más de 3.5 veces más rápido en las cuatro pruebas. Esto pasa porque `sleep()` es una espera. Mientras un trabajador está esperando los demás pueden seguir con sus documentos. De todas formas, hay que esperar a que termine el último para mostrar el resultado final.

## Respuestas a las preguntas

**1. ¿Por qué queue.Queue es apropiada para compartir trabajos?**

Porque ya está preparada para usarse con varios hilos. Si dos trabajadores intentan sacar un documento al mismo tiempo, la cola coordina el acceso y les entrega documentos distintos. Así no tengo que poner un candado aparte para sacar los trabajos.

**2. ¿Qué protege Lock y qué pasaría si se actualizara el resumen sin él?**

En mi programa, el `mutex` protege la parte donde se actualizan `resumen` y `registro`. Mientras un hilo está ahí, los otros esperan su turno. Esto evita que se mezclen esas actualizaciones. Sin el lock, si varios hilos modifican un mismo dato mediante varios pasos, puede haber una condición de carrera y perderse una actualización.

**3. ¿Qué cambiarías si cada documento tuviera que guardarse en un archivo real?**

En vez de usar `sleep()`, guardaría el contenido con `with open(...)`. Le pondría un nombre diferente a cada archivo, por ejemplo `doc_5.txt`, para que los trabajadores no escriban sobre el mismo. Si también hubiera un archivo de registro para todos, escribiría en él dentro del `mutex`. Además, pondría un `try/except` para manejar algún error al guardar.
