#!/usr/bin/env python3
"""
Script para ejecutar el proceso Write – Audit – Publish:
- Inserta datos en la tabla de staging.
- Aplica auditorías de calidad (utilizando queries SQL para auditorías globales
  y validación por fila para determinar si cada registro es válido).
- Inserta de forma idempotente en la tabla de producción solo los registros válidos
  y limpia la tabla de staging.
"""

import psycopg2
import psycopg2.extras
import csv
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/futbol_db")
CSV_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'futbol.csv')


def safe_int(value):
    """Convierte el valor a entero si es posible, o retorna None para cadenas vacías."""
    if value is None or str(value).strip() == "":
        return None
    try:
        return int(value)
    except ValueError:
        return None


def safe_str(value):
    """Convierte el valor a string y limpia espacios."""
    if value is None:
        return None
    return str(value).strip()


def insert_into_staging():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convierte cada campo
            row_id = safe_int(row['id'])
            nombre = safe_str(row['nombre'])
            edad = safe_int(row['edad'])
            nacionalidad = safe_str(row['nacionalidad'])
            altura = safe_int(row['altura'])
            peso = safe_int(row['peso'])
            equipo = safe_str(row['equipo'])
            posicion = safe_str(row['posicion'])
            partidos = safe_int(row['partidos'])
            goles = safe_int(row['goles'])
            asistencias = safe_int(row['asistencias'])
            tarjetas = safe_int(row['tarjetas'])
            minutos = safe_int(row['minutos'])
            rendimiento = safe_int(row['rendimiento'])

            # TODO: Define el query SQL para insertar cada fila del CSV en la tabla 'futbol_data_staging'.
            # Debes incluir todas las columnas (incluyendo 'id') en el orden del Data Dictionary y utilizar placeholders.
            query = """
                #TODO: Completar el query de inserción en futbol_data_staging
            """
            cur.execute(query, (
                row_id, nombre, edad, nacionalidad, altura, peso, equipo, posicion,
                partidos, goles, asistencias, tarjetas, minutos, rendimiento
            ))
    conn.commit()
    cur.close()
    conn.close()
    print("Datos insertados en staging.")


def is_valid_row(row, seen_ids):
    """
    Valida un registro (como dict) de la tabla staging.
    Se asegura de que ningún campo obligatorio esté vacío y que ciertos valores numéricos cumplan condiciones específicas.
    También verifica si el 'id' ya se ha procesado (para detectar duplicados a nivel de CSV).
    Retorna una lista vacía si el registro es válido, o una lista de mensajes de error en caso contrario.
    """
    errors = []
    mandatory_fields = ['id', 'nombre', 'edad', 'nacionalidad', 'altura', 'peso', 
                       'equipo', 'posicion', 'rendimiento']
    
    for field in mandatory_fields:
        value = row.get(field)
        if value is None or (isinstance(value, str) and value.strip() == ""):
            errors.append(f"{field} falta")

    # Verifica duplicados en 'id' usando el conjunto seen_ids.
    try:
        current_id = int(row['id'])
        if current_id in seen_ids:
            errors.append("id duplicado")
        else:
            seen_ids.add(current_id)
    except Exception:
        errors.append("El id debe ser un entero válido")

    # Validaciones numéricas
    try:
        edad = int(row['edad'])
        # TODO: Define la condición para verificar que 'edad' esté en el rango 16-50.
        if False:  # Reemplazar con la condición correcta
            errors.append("La edad debe estar entre 16 y 50 años")
    except Exception:
        errors.append("La edad debe ser un entero")

    try:
        altura = int(row['altura'])
        # TODO: Define la condición para verificar que 'altura' esté en el rango 150-220.
        if False:  # Reemplazar con la condición correcta
            errors.append("La altura debe estar entre 150 y 220 cm")
    except Exception:
        errors.append("La altura debe ser un entero")

    try:
        peso = int(row['peso'])
        # TODO: Define la condición para verificar que 'peso' esté en el rango 40-100.
        if False:  # Reemplazar con la condición correcta
            errors.append("El peso debe estar entre 40 y 100 kg")
    except Exception:
        errors.append("El peso debe ser un entero")

    try:
        rendimiento = int(row['rendimiento'])
        # TODO: Define la condición para verificar que 'rendimiento' solo contenga 0 o 1.
        if False:  # Reemplazar con la condición correcta
            errors.append("El rendimiento debe ser 0 o 1")
    except Exception:
        errors.append("El rendimiento debe ser un entero")

    # Validaciones para campos que deben ser no negativos
    non_negative_fields = ['partidos', 'goles', 'asistencias', 'tarjetas', 'minutos']
    for field in non_negative_fields:
        try:
            value = int(row[field])
            if value < 0:
                errors.append(f"{field} no puede ser negativo")
        except Exception:
            errors.append(f"{field} debe ser un entero")

    return errors


def publish_data():
    """
    Lee cada registro de la tabla de staging, valida individualmente y
    migra a la tabla de producción sólo los registros válidos.
    Finalmente, limpia la tabla de staging.
    """
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute("""
        SELECT id, nombre, edad, nacionalidad, altura, peso, equipo, posicion, 
               partidos, goles, asistencias, tarjetas, minutos, rendimiento 
        FROM futbol_data_staging;
    """)
    rows = cur.fetchall()

    valid_count = 0
    skipped_count = 0
    seen_ids = set()

    for row in rows:
        row_dict = dict(row)
        errors = is_valid_row(row_dict, seen_ids)
        if errors:
            print(f"Saltando la fila con id {row_dict['id']} debido al error: {errors}")
            skipped_count += 1
            continue

        # TODO: Define el query SQL para migrar los datos desde 'futbol_data_staging' a 'futbol_data'
        # de forma idempotente (por ejemplo, utilizando ON CONFLICT).
        insert_query = """
            #TODO: Completar el query para insertar datos de staging en la tabla de producción.
        """
        cur.execute(insert_query, (
            row_dict['id'], row_dict['nombre'], row_dict['edad'], 
            row_dict['nacionalidad'], row_dict['altura'], row_dict['peso'],
            row_dict['equipo'], row_dict['posicion'], row_dict['partidos'],
            row_dict['goles'], row_dict['asistencias'], row_dict['tarjetas'],
            row_dict['minutos'], row_dict['rendimiento']
        ))
        valid_count += 1

    conn.commit()

    # Limpiar staging: eliminar tabla después de procesar
    # TODO: Define el query SQL para eliminar la tabla 'futbol_data_staging' una vez que los datos han sido publicados.
    query_cleanup = """
        #TODO: Completar el query para eliminar la tabla de staging.
    """
    cur.execute(query_cleanup)
    conn.commit()
    
    cur.close()
    conn.close()
    print(f"Proceso de publicación completado: {valid_count} filas migradas, {skipped_count} filas omitidas, y staging limpiado.")


if __name__ == "__main__":
    print("Iniciando proceso Write – Audit – Publish...")
    insert_into_staging()
    publish_data()
    print("Proceso completado.")
