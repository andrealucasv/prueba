# Ejercicio: "Proceso de Datos de Fútbol con Git y SQL"

## Objetivo General

Demostrar habilidades en:

- Manejo de Git y GitHub (fork, branches, pull requests)
- Creación y validación de nuevas tablas en Postgres mediante un proceso **Write – Audit – Publish**
- Población de la tabla utilizando datos de un CSV

---

## Información Importante

**Nota:** Ante cualquier duda, se espera que preguntes, ya que la actitud proactiva es fundamental en nuestro entorno de trabajo.

**Uso de Materiales Externos:** Está permitido y se alienta el uso de recursos en internet, incluyendo herramientas de IA como ChatGPT, para avanzar en el ejercicio y resolver dudas. Verifica siempre el código generado para evitar errores.

---

## Data Dictionary (archivo futbol.csv)

Todas las columnas son obligatorias y deben incluirse en la definición de la tabla:

- **id:** Identificador único del jugador
- **nombre:** Nombre del jugador
- **edad:** Edad del jugador
- **nacionalidad:** País de origen
- **altura:** Altura en cm
- **peso:** Peso en kg
- **equipo:** Nombre del equipo
- **posicion:** Posición en el campo
- **partidos:** Número de partidos jugados
- **goles:** Número de goles anotados
- **asistencias:** Número de asistencias
- **tarjetas:** Número total de tarjetas
- **minutos:** Minutos jugados
- **rendimiento:** 0 = bajo rendimiento, 1 = alto rendimiento

---

## Pasos e Instrucciones

### 1. Configuración Inicial y Git

**Fork del Repositorio:**
- Haz un fork del repositorio base a tu cuenta personal de GitHub

**Clonado Local:**
- Clona tu fork a tu máquina local
- Crea un archivo llamado `comandos_utilizados.txt` donde documentes todos los comandos Git utilizados

### 2. Estructura de Tablas en Postgres

**Nueva Tabla:**
En el archivo `migrations/001_create_futbol_data.sql` completa la definición de las tablas:

- **Staging:**
  Crea la tabla `futbol_data_staging` con todas las columnas del Data Dictionary

- **Producción:**
  Crea la tabla `futbol_data` con la misma estructura, estableciendo `id` como PRIMARY KEY y UNIQUE

### 3. Proceso Write – Audit – Publish

Este proceso se implementa en el script `scripts/write_audit_publish.py`:

**Write:**
- Completa el query SQL para insertar cada fila del CSV en `futbol_data_staging`
- **[#TODO: Completa el query de inserción]**

**Audit:**
Implementa 4 auditorías de validación:
- Verificar que `rendimiento` solo contenga 0 o 1
- Verificar que `edad` esté en el rango 16-50
- Verificar que `altura` esté en el rango 150-220
- Verificar que `peso` esté en el rango 40-100
- **[#TODO: Completa las validaciones]**

**Publish:**
- Define el query SQL para migrar datos de staging a producción de forma idempotente
- Define el query para limpiar la tabla de staging
- **[#TODO: Completa los queries de publicación]**

### 4. Entrega Final

- **Commits:** Realiza commits descriptivos de tu progreso
- **Push:** Sube tus cambios a tu fork en GitHub
- **Pull Request:** Abre un Pull Request desde tu fork hacia el repositorio original



Buena suerte.
