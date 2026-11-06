"""
Ejercicio 2: Ejecución con CONCURRENCIA
Ejemplo de la vida real: hacer la lavandería.

Una sola persona (un solo hilo) maneja varias tareas a la vez: mientras la
lavadora trabaja, la persona no se queda esperando; aprovecha ese tiempo para
atender otra cosa. Las tareas se INTERCALAN, no se ejecutan en paralelo.

Se implementa con asyncio: cada tarea es una corrutina y `await` indica
"estoy esperando, puedes atender otra tarea mientras tanto".
"""

import asyncio
import threading
import time

INICIO = time.perf_counter()

# Duración (en segundos) de cada paso de una carga de ropa
CARGAR_LAVADORA = 1
LAVAR = 3
PASAR_A_SECADORA = 1
SECAR = 3
DOBLAR = 1
CALENTAR_PLANCHA = 2

# Si todo se hiciera uno tras otro (secuencial) tardaría:
POR_CARGA = CARGAR_LAVADORA + LAVAR + PASAR_A_SECADORA + SECAR + DOBLAR  # 9 s
TIEMPO_SECUENCIAL = POR_CARGA * 2 + CALENTAR_PLANCHA  # 20 s


def log(mensaje: str) -> None:
    """Imprime un mensaje con el segundo exacto y el hilo que lo ejecuta."""
    transcurrido = time.perf_counter() - INICIO
    hilo = threading.current_thread().name
    print(f"[{transcurrido:5.1f}s] [{hilo}] {mensaje}")


async def lavar_carga(nombre: str, retraso_inicio: float = 0) -> None:
    """Ciclo completo de una carga: lavar, secar y doblar."""
    await asyncio.sleep(retraso_inicio)

    log(f"{nombre}: cargando la lavadora...")
    await asyncio.sleep(CARGAR_LAVADORA)

    log(f"{nombre}: LAVANDO (la lavadora trabaja sola, la persona queda libre)")
    await asyncio.sleep(LAVAR)

    log(f"{nombre}: pasando la ropa a la secadora...")
    await asyncio.sleep(PASAR_A_SECADORA)

    log(f"{nombre}: SECANDO (la secadora trabaja sola, la persona queda libre)")
    await asyncio.sleep(SECAR)

    log(f"{nombre}: doblando la ropa...")
    await asyncio.sleep(DOBLAR)

    log(f"{nombre}: LISTA.")


async def calentar_plancha() -> None:
    log("Plancha: calentando la plancha...")
    await asyncio.sleep(CALENTAR_PLANCHA)
    log("Plancha: lista para usar.")


async def main() -> None:
    print("=" * 66)
    print("EJECUCION CONCURRENTE: Haciendo la lavanderia")
    print("Una sola persona (un solo hilo) atiende varias tareas a la vez.")
    print("=" * 66)

    # gather() lanza todas las corrutinas y las intercala cada vez que una
    # de ellas hace `await` (es decir, cuando queda esperando).
    await asyncio.gather(
        lavar_carga("Ropa blanca"),
        lavar_carga("Ropa de color", retraso_inicio=1),  # se carga 1 s despues
        calentar_plancha(),
    )

    total = time.perf_counter() - INICIO
    print("=" * 66)
    print(f"Tiempo total CONCURRENTE: {total:.1f} segundos")
    print(f"Tiempo si fuera SECUENCIAL: {TIEMPO_SECUENCIAL} segundos "
          f"({POR_CARGA} + {POR_CARGA} + {CALENTAR_PLANCHA})")
    print(f"Se ahorraron aprox. {TIEMPO_SECUENCIAL - total:.1f} segundos "
          "aprovechando los tiempos de espera.")
    print("Nota: todo se ejecuto en UN solo hilo -> concurrencia, no paralelismo.")
    print("=" * 66)


if __name__ == "__main__":
    asyncio.run(main())
