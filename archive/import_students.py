import os
import sys
import re
import sqlite3

# Add parent directory to path to import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.database import DBManager

def clean_course(course_line):
    if "1er nivel de Transición (Pre-kinder)" in course_line:
        return "PRE-KINDER"
    if "2° nivel de Transición (Kinder)" in course_line:
        return "KINDER"
    match = re.search(r"(\d+°)\s+básico", course_line)
    if match:
        return f"{match.group(1)} BÁSICO"
    return course_line.strip()

def import_students():
    db = DBManager()
    txt_path = 'extracted_text.txt'
    
    if not os.path.exists(txt_path):
        print(f"Error: {txt_path} not found.")
        return

    current_course = "DESCONOCIDO"
    students_to_insert = []
    
    with open(txt_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Detect Course
        if "Alumnos del" in line:
            current_course = clean_course(line)
            continue
            
        # Match student line: [Index] [RUT] [Name] NUEVO ADMITIDO
        # Example: 1 27675519-6 CASTILLO ESPINOZA JULIETTE MARIANELA NUEVO ADMITIDO
        match = re.match(r"^\d+\s+([\d\-Kk]+)\s+(.+?)\s+NUEVO\s+ADMITIDO$", line)
        if match:
            rut = match.group(1).upper()
            name = match.group(2).strip()
            students_to_insert.append((name, rut, current_course))
            
    # Insert into database
    conn = db.get_connection()
    cursor = conn.cursor()
    
    count = 0
    errors = 0
    for name, rut, course in students_to_insert:
        try:
            # We only have name, rut and course
            cursor.execute("""
                INSERT INTO estudiantes (nombre_estudiante, rut_estudiante, curso_matricula, fecha_matricula)
                VALUES (?, ?, ?, DATE('now'))
            """, (name, rut, course))
            count += 1
        except sqlite3.IntegrityError:
            # RUT already exists
            print(f"Skipping (already exists): {rut} - {name}")
            errors += 1
        except Exception as e:
            print(f"Error inserting {rut}: {e}")
            errors += 1
            
    conn.commit()
    conn.close()
    
    print(f"\nImport total: {count} students added.")
    if errors > 0:
        print(f"Skipped/Errors: {errors}")

if __name__ == "__main__":
    import_students()
