import sqlite3
import pandas as pd
from datetime import datetime

import os
import sys

class DBManager:
    def __init__(self, db_name="matriculas.db"):
        # Determinar la ruta base (donde está el .exe o el script main.py)
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            # Asumimos que database.py está en modules/, así que subimos un nivel
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
        self.db_name = os.path.join(base_dir, db_name)
        self.create_tables()

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def create_tables(self):
        """Creates the main table for enrollments if it doesn't exist."""
        query = """
        CREATE TABLE IF NOT EXISTS estudiantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            num_matricula TEXT, -- Nuevo campo
            fecha_matricula TEXT,
            observaciones TEXT, -- Nuevo campo
            
            -- Datos del Estudiante
            nombre_estudiante TEXT NOT NULL,
            fecha_nacimiento TEXT,
            nacionalidad TEXT,
            rut_estudiante TEXT UNIQUE NOT NULL,
            edad INTEGER,
            sexo TEXT,
            direccion TEXT,
            comuna TEXT,
            vive_con TEXT,
            colegio_anterior TEXT,
            repitencia TEXT, -- 'Si'/'No'

            -- Programa PIE
            es_pie TEXT, -- 'Si'/'No'
            diagnostico_pie TEXT, -- Si es PIE

            -- Datos Apoderado Titular
            nombre_apoderado TEXT,
            rut_apoderado TEXT,
            telefono_apoderado TEXT,
            parentesco_apoderado TEXT,
            profesion_apoderado TEXT,
            direccion_apoderado TEXT,
            email_apoderado TEXT,

            -- Datos Madre
            nombre_madre TEXT,
            rut_madre TEXT,
            direccion_madre TEXT,
            escolaridad_madre TEXT,
            profesion_madre TEXT,

            -- Datos Padre
            nombre_padre TEXT,
            rut_padre TEXT,
            direccion_padre TEXT,
            escolaridad_padre TEXT,
            profesion_padre TEXT,

            -- Contactos Emergencia
            tutor1_nombre TEXT,
            tutor1_rut TEXT,
            tutor1_telefono TEXT,
            tutor2_nombre TEXT,
            tutor2_rut TEXT,
            tutor2_telefono TEXT,

            -- Salud
            tratamiento_medico TEXT, -- 'Si'/'No' + detalle
            contraindicacion_fisica TEXT, -- 'Si'/'No'
            alergias TEXT, -- 'Si'/'No' + detalle

            -- Antecedentes Sociales
            rsh_puntaje TEXT,
            alumno_prioritario TEXT, -- 'Si'/'No'
            beca TEXT,

            -- Autorizaciones
            aut_imagen INTEGER, -- 0/1
            aut_reglamento INTEGER, -- 0/1
            aut_textos INTEGER -- 0/1
        );
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                conn.commit()
                print("Tabla 'estudiantes' verificada/creada exitosamente.")
                self.check_and_migrate_table(conn)
        except sqlite3.Error as e:
            print(f"Error al crear tabla: {e}")

    def check_and_migrate_table(self, conn):
        """Checks for missing columns and alters table if necessary."""
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(estudiantes)")
        columns = [info[1] for info in cursor.fetchall()]
        
        new_columns = {
            'num_matricula': 'TEXT',
            'observaciones': 'TEXT'
        }
        
        for col_name, col_type in new_columns.items():
            if col_name not in columns:
                try:
                    cursor.execute(f"ALTER TABLE estudiantes ADD COLUMN {col_name} {col_type}")
                    print(f"Columna '{col_name}' agregada exitosamente.")
                except sqlite3.Error as e:
                    print(f"Error al agregar columna '{col_name}': {e}")
        conn.commit()

    def agregar_estudiante(self, data):
        """
        Inserts a new student record.
        :param data: Dictionary with keys matching database columns.
        :return: (True, message) or (False, error_message)
        """
        # Prepare columns and placeholders
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        query = f"INSERT INTO estudiantes ({columns}) VALUES ({placeholders})"
        
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, list(data.values()))
                conn.commit()
            return True, "Estudiante matriculado exitosamente."
        except sqlite3.IntegrityError:
            return False, "Error: El RUT del estudiante ya existe en la base de datos."
        except sqlite3.Error as e:
            return False, f"Error de base de datos: {e}"

    def obtener_estudiantes(self):
        """Returns all students as a list of dictionaries."""
        query = "SELECT * FROM estudiantes"
        try:
            with self.get_connection() as conn:
                conn.row_factory = sqlite3.Row # Access columns by name
                cursor = conn.cursor()
                cursor.execute(query)
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"Error al obtener estudiantes: {e}")
            return []

    def buscar_estudiantes(self, busqueda):
        """Search students by name or RUT."""
        query = """
        SELECT * FROM estudiantes 
        WHERE nombre_estudiante LIKE ? OR rut_estudiante LIKE ?
        """
        term = f"%{busqueda}%"
        try:
            with self.get_connection() as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(query, (term, term))
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"Error al buscar: {e}")
            return []

    def eliminar_estudiante(self, rut):
        """Deletes a student by RUT."""
        query = "DELETE FROM estudiantes WHERE rut_estudiante = ?"
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (rut,))
                conn.commit()
            return True, "Estudiante eliminado."
        except sqlite3.Error as e:
            return False, f"Error al eliminar: {e}"

    def obtener_estudiante_por_id(self, id_estudiante):
        """Returns a single student by ID."""
        query = "SELECT * FROM estudiantes WHERE id = ?"
        try:
            with self.get_connection() as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(query, (id_estudiante,))
                row = cursor.fetchone()
                return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"Error al obtener estudiante por ID: {e}")
            return None

    def eliminar_estudiante_por_id(self, id_estudiante):
        """Deletes a student by ID."""
        query = "DELETE FROM estudiantes WHERE id = ?"
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (id_estudiante,))
                conn.commit()
            return True, "Estudiante eliminado."
        except sqlite3.Error as e:
            return False, f"Error al eliminar: {e}"

    def actualizar_estudiante(self, id_estudiante, data):
        """
        Updates an existing student record.
        :param id_estudiante: ID of the student to update.
        :param data: Dictionary with keys matching database columns.
        :return: (True, message) or (False, error_message)
        """
        # Prepare setters
        setters = ', '.join([f"{key} = ?" for key in data.keys()])
        query = f"UPDATE estudiantes SET {setters} WHERE id = ?"
        
        values = list(data.values())
        values.append(id_estudiante)
        
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, values)
                conn.commit()
            return True, "Estudiante actualizado exitosamente."
        except sqlite3.Error as e:
            return False, f"Error de base de datos al actualizar: {e}"

    def exportar_excel(self, filename="matriculas_export.xlsx"):
        """Exports the entire database to Excel."""
        try:
            conn = self.get_connection()
            df = pd.read_sql_query("SELECT * FROM estudiantes", conn)
            df.to_excel(filename, index=False)
            conn.close()
            return True, f"Base de datos exportada a {filename}"
        except Exception as e:
            return False, f"Error al exportar: {e}"

if __name__ == "__main__":
    # Test rápido de creación
    db = DBManager()
