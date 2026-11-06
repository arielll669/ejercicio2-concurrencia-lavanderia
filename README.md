# Ejercicio 2: Ejecución con concurrencia - Hacer la lavandería

Script en Python que muestra una **ejecución con concurrencia** con un ejemplo de la vida diaria: una sola persona haciendo la lavandería.

## ¿Qué es la concurrencia?

Es la capacidad de **manejar varias tareas a la vez, intercalándolas**, aunque solo haya un único "trabajador" (un solo hilo). Cuando una tarea queda esperando (por ejemplo, a que termine una máquina), se aprovecha ese tiempo para avanzar en otra.

> Concurrencia ≠ paralelismo. Aquí hay **un solo hilo**: nunca se hacen dos cosas en el mismo instante, pero tampoco se pierde tiempo esperando.

## El ejemplo

Una persona tiene que lavar dos cargas de ropa y además calentar la plancha. Cada carga pasa por estos pasos:

| Paso | Tarea | Duración | ¿Necesita a la persona? |
|------|-------|----------|-------------------------|
| 1 | Cargar la lavadora | 1 s | Sí |
| 2 | Lavar | 3 s | No, la lavadora trabaja sola |
| 3 | Pasar a la secadora | 1 s | Sí |
| 4 | Secar | 3 s | No, la secadora trabaja sola |
| 5 | Doblar la ropa | 1 s | Sí |

- **Si fuera secuencial** (una carga completa y luego la otra, y al final la plancha): 9 + 9 + 2 = **20 s**.
- **Con concurrencia**: mientras la lavadora lava, la persona carga la segunda ropa y calienta la plancha. Todo termina en **~10 s**.

Se implementa con `asyncio`: cada tarea es una corrutina (`async def`) y cada `await` significa "estoy esperando, atiende otra tarea mientras tanto". `asyncio.gather()` lanza todas las tareas juntas.

En cada línea de la salida se imprime el nombre del hilo (`MainThread`) para demostrar que **todo ocurre en un solo hilo**.

## Requisitos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado y en ejecución (incluye Docker Compose).

## Cómo ejecutarlo con Docker

1. Clonar el repositorio y entrar a la carpeta:

   ```bash
   git clone https://github.com/arielll669/ejercicio2-concurrencia-lavanderia.git
   cd ejercicio2-concurrencia-lavanderia
   ```

2. Construir la imagen y ejecutar el script:

   ```bash
   docker compose up --build
   ```

3. Al terminar, limpiar el contenedor:

   ```bash
   docker compose down
   ```

## Salida esperada

```
==================================================================
EJECUCION CONCURRENTE: Haciendo la lavanderia
Una sola persona (un solo hilo) atiende varias tareas a la vez.
==================================================================
[  0.0s] [MainThread] Plancha: calentando la plancha...
[  0.0s] [MainThread] Ropa blanca: cargando la lavadora...
[  1.0s] [MainThread] Ropa de color: cargando la lavadora...
[  1.0s] [MainThread] Ropa blanca: LAVANDO (la lavadora trabaja sola, la persona queda libre)
[  2.0s] [MainThread] Plancha: lista para usar.
[  2.0s] [MainThread] Ropa de color: LAVANDO (la lavadora trabaja sola, la persona queda libre)
[  4.0s] [MainThread] Ropa blanca: pasando la ropa a la secadora...
[  5.0s] [MainThread] Ropa de color: pasando la ropa a la secadora...
[  5.0s] [MainThread] Ropa blanca: SECANDO (la secadora trabaja sola, la persona queda libre)
[  6.0s] [MainThread] Ropa de color: SECANDO (la secadora trabaja sola, la persona queda libre)
[  8.0s] [MainThread] Ropa blanca: doblando la ropa...
[  9.0s] [MainThread] Ropa de color: doblando la ropa...
[  9.0s] [MainThread] Ropa blanca: LISTA.
[ 10.0s] [MainThread] Ropa de color: LISTA.
==================================================================
Tiempo total CONCURRENTE: 10.0 segundos
Tiempo si fuera SECUENCIAL: 20 segundos (9 + 9 + 2)
Se ahorraron aprox. 10.0 segundos aprovechando los tiempos de espera.
Nota: todo se ejecuto en UN solo hilo -> concurrencia, no paralelismo.
==================================================================
```

Observa que las tareas **se intercalan** (la plancha se calienta mientras se carga la lavadora) y que todas las líneas dicen `MainThread`.

## Estructura del proyecto

```
.
├── main.py              # Script con la ejecución concurrente (asyncio)
├── Dockerfile           # Imagen de Python 3.12
├── docker-compose.yml   # Definición del servicio
└── README.md
```

## Ejecución sin Docker (opcional)

```bash
python main.py
```
