# Sistema de Matrícula Escolar

Aplicación de escritorio para la gestión de matrículas, diseñada para ser portátil y fácil de usar.

## Requisitos

- Python 3.x
- Dependencias listadas en `requirements.txt`

## Instalación

1.  Clonar o descargar este repositorio.
2.  Instalar las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

## Uso

Ejecutar el archivo principal:
```bash
python main.py
```

## Estructura

- `main.py`: Archivo principal de ejecución.
- `modules/`: Contiene la lógica de base de datos, generación de PDF y exportación.
- `assets/`: Recursos gráficos (iconos, imágenes).

## Preparar versión portable (Windows)

Pasos recomendados para generar una versión portable (parte entregable para Secretaría):

1. Crear un entorno virtual e instalar dependencias:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Instalar PyInstaller y generar build `--onedir` (incluye carpetas estáticas):

```powershell
pip install pyinstaller
pyinstaller --noconfirm --onedir --windowed \
    --add-data "assets;assets" \
    --add-data "modules;modules" \
    main.py
```

- El ejecutable generado estará en `dist\main\` (copiar esa carpeta y comprimirla como ZIP para entrega).
- Si prefieres un único `.exe`, usar `--onefile`, aunque puede requerir ajustes para archivos externos.

3. Probar en una máquina limpia (sin Python instalado) — descomprimir el ZIP y ejecutar `main.exe`.

4. Entregar ZIP con un `run.bat` (simple) y un `README_entrega.md` con instrucciones.

## Limpieza del proyecto y control de versiones (checkpoint Git)

Antes de reorganizar o eliminar archivos, crea un punto de control en Git para poder volver atrás:

```powershell
# Crear rama temporal y commitear cambios actuales
git checkout -b prepare-cleanup
git add -A
git commit -m "chore: checkpoint before cleanup and portability tasks"
# Crear tag de referencia
git tag -a checkpoint-cleanup -m "Checkpoint before cleanup"
```

Si no quieres crear una rama, puedes crear solo el tag sobre `HEAD` después de commitear.

## Revisión rápida de archivos/scripts que parecen obsoletos

En este punto del proyecto, los siguientes archivos parecen ser utilitarios de importación/extracción usados solo durante la migración de datos:

- `scripts/extract_students.py`
- `scripts/import_students.py`
- `scripts/verify_import.py`
- `extracted_text.txt`
- `FALTANTES.txt`

Recomendación: no borrar aún. Moverlos a una carpeta `archive/` o `tools/` y documentar su propósito. Ejemplo:

```powershell
mkdir archive
move scripts\extract_students.py archive\
move scripts\import_students.py archive\
move scripts\verify_import.py archive\
move extracted_text.txt archive\
move FALTANTES.txt archive\
```

Luego commitear esos movimientos en Git para mantener historial:

```powershell
git add -A
git commit -m "chore: archive legacy import/extract scripts"
```

## Organización recomendada (mínima)

- `main.py` — entrada de la aplicación.
- `modules/` — lógica modular (no cambiar nombres public API sin pruebas).
- `assets/` — recursos estáticos.
- `scripts/` — utilidades temporales. Mover a `archive/` si ya no se usan.
- `build/` — (opcional) guardar builds generados o scripts de empaquetado.

## Archivos y scripts que puedo preparar para ti

- `build.ps1` y `build.bat` con el comando de PyInstaller listo para usar.
- `README_entrega.md` con pasos exactos para Secretaría (cómo ejecutar, qué archivos enviar).
- Un ejemplo de `run.bat` para arrancar la app desde la carpeta `dist\main`.

Si quieres, puedo crear esos archivos ahora y además crear el checkpoint Git (commit + tag) en tu repo local; dime si quieres que proceda con eso.

