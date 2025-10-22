#  Ejercicio Integral: Integración de Bases de Datos
## Objetivo General
Demostrar habilidades en:

- Manejo de Base de Datos SQL y Git (incluyendo la documentación de comandos usados en la terminal)
- Creación y validación de nuevas tablas en Postgres mediante un proceso Write – Audit – Publish
- Población de la tabla utilizando datos de un CSV (incluido en el repositorio)
- Generación de queries

> **Nota:**
Está permitido y se alienta el uso de recursos en internet, incluyendo herramientas de IA como ChatGPT, para avanzar en el ejercicio y resolver dudas. Verifica siempre el código generado para evitar errores.


### 1. Uso de Git
- Crea un directorio con tu nombre, siguiendo el formato ` proyecto_nombre` , por ejemplo: proyecto_jose
- Inicializa un repositorio Git dentro del directorio
- Documenta todos los comandos utilizados en un archivo llamado `comandos_utilizados.txt`


### 2. Creación y Población de Nueva Tabla en Postgres

Diccionario de Datos (archivo futbol_stats.csv):
- id: Identificador único del jugador
- nombre: Nombre del jugador
- edad: Edad del jugador
- nacionalidad: País de origen
- altura: Altura en cm
- peso: Peso en kg
- equipo: Nombre del equipo
- posicion: Posición en el campo
- partidos: Número de partidos jugados
- goles: Número de goles anotados
- asistencias: Número de asistencias
- tarjetas: Número total de tarjetas
- minutos: Minutos jugados
- rendimiento: 0 = bajo rendimiento, 1 = alto rendimiento

Migraciones:
- Crear dos tablas:
  - futbol_data_staging: para carga inicial
  - futbol_data: tabla de producción con id como PRIMARY KEY y UNIQUE

### 3. Proceso Write – Audit – Publish

Write:
- Insertar cada fila del CSV en futbol_data_staging

Audit:
- Verificar:
  1. Duplicados en id
  2. Nulos en columnas clave (id, nombre, rendimiento)
  3. rendimiento solo debe contener 0 o 1
  4. edad debe ser mayor que 15
  5. goles y asistencias no deben ser negativos
  6. minutos debe estar entre 0 y 5400

Publish:
- Migrar datos a futbol_data usando ON CONFLICT
- Limpiar la tabla de staging después de publicar



📁 5. Archivos Incluidos
- futbol_stats.csv – Datos ficticios de jugadores
- queries_futbol.sql – Consultas SQL para Superset
- auditoria_publish_futbol.sql – Auditorías y publicación de datos

