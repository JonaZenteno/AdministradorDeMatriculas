@echo off
echo Instalando PyInstaller si no existe...
pip install pyinstaller

echo Creando ejecutable...
pyinstaller --noconfirm --onefile --windowed --name "SistemaMatriculas" --add-data "modules;modules" --hidden-import "reportlab" --hidden-import "pandas" --hidden-import "openpyxl" --hidden-import "customtkinter" main.py

echo Construcción finalizada. El ejecutable está en la carpeta 'dist'.
pause
