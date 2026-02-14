from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import os
import sys
from datetime import datetime

class PDFGenerator:
    def __init__(self, filename="matricula.pdf"):
        self.filename = filename
        self.styles = getSampleStyleSheet()
        self.create_custom_styles()

    def create_custom_styles(self):
        self.styles.add(ParagraphStyle(name='Header', fontSize=14, leading=16, alignment=1, spaceAfter=20, fontName='Helvetica-Bold'))
        self.styles.add(ParagraphStyle(name='HeaderNoSpace', fontSize=14, leading=16, alignment=1, spaceAfter=5, fontName='Helvetica-Bold'))
        self.styles.add(ParagraphStyle(name='SubHeader', fontSize=12, leading=14, spaceAfter=10, fontName='Helvetica-Bold'))
        self.styles.add(ParagraphStyle(name='NormalSmall', fontSize=10, leading=12))
        self.styles.add(ParagraphStyle(name='Signature', fontSize=10, leading=12, alignment=1, spaceBefore=40))

    def get_asset_path(self, filename):
        """Get the absolute path to an asset file."""
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_dir, "assets", filename)

    def generate_pdf(self, student_data):
        doc = SimpleDocTemplate(self.filename, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
        elements = []

        # Logo
        logo_path = self.get_asset_path("logo.png")
        if os.path.exists(logo_path):
            try:
                logo = Image(logo_path, width=50, height=50)
                logo.hAlign = 'CENTER'
                elements.append(logo)
                elements.append(Spacer(1, 12))
            except Exception as e:
                print(f"Error loading logo in PDF: {e}")

        # Title
        elements.append(Paragraph("FICHA DE MATRÍCULA", self.styles['HeaderNoSpace']))
        elements.append(Paragraph("ESCUELA LOS LEONES", self.styles['Header']))
        elements.append(Spacer(1, 12))

        # Helper to create data rows
        def create_section(title, data_dict):
            elements.append(Paragraph(title, self.styles['SubHeader']))
            data = []
            for key, value in data_dict.items():
                data.append([Paragraph(f"<b>{key}:</b>", self.styles['NormalSmall']), Paragraph(str(value) if value else '', self.styles['NormalSmall'])])
            
            t = Table(data, colWidths=[150, 350])
            t.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('BACKGROUND', (0, 0), (0, -1), colors.whitesmoke),
            ]))
            elements.append(t)
            elements.append(Spacer(1, 15))

        # 1. DATOS DE ESTUDIANTE
        student_info = {
            "Nombre": student_data.get('nombre_estudiante', ''),
            "Fecha nacimiento": student_data.get('fecha_nacimiento', ''),
            "Sexo": student_data.get('sexo', ''),
            "Nacionalidad": student_data.get('nacionalidad', ''),
            "RUT": student_data.get('rut_estudiante', ''),
            "Asiste a PIE": student_data.get('es_pie', ''),
            "Teléfono": '',  # No disponible en BD
            "Diagnóstico": student_data.get('diagnostico_pie', ''),
            "Colegio Anterior": student_data.get('colegio_anterior', ''),
            "Dirección": student_data.get('direccion', ''),
            "Con quien vive": student_data.get('vive_con', ''),
            "Repitencia": student_data.get('repitencia', '')
        }
        create_section("DATOS DE ESTUDIANTE", student_info)

        # 2. DATOS DE APODERADO
        guardian_info = {
            "Nombre": student_data.get('nombre_apoderado', ''),
            "Rut": student_data.get('rut_apoderado', ''),
            "Teléfono": student_data.get('telefono_apoderado', ''),
            "Parentesco": student_data.get('parentesco_apoderado', ''),
            "Correo": student_data.get('email_apoderado', ''),
            "Profesión u Oficio": student_data.get('profesion_apoderado', ''),
            "Dirección": student_data.get('direccion_apoderado', '')
        }
        create_section("DATOS DE APODERADO", guardian_info)

        # 3. DATOS DE PADRES
        parents_info = {
            "Nombre Madre": student_data.get('nombre_madre', ''),
            "Rut Madre": student_data.get('rut_madre', ''),
            "Dirección Madre": student_data.get('direccion_madre', ''),
            "Escolaridad Madre": student_data.get('escolaridad_madre', ''),
            "Profesión u Oficio Madre": student_data.get('profesion_madre', ''),
            "Teléfono Madre": '',  # No disponible en BD
            "Nombre Padre": student_data.get('nombre_padre', ''),
            "Rut Padre": student_data.get('rut_padre', ''),
            "Dirección Padre": student_data.get('direccion_padre', ''),
            "Escolaridad Padre": student_data.get('escolaridad_padre', ''),
            "Profesión u Oficio Padre": student_data.get('profesion_padre', ''),
            "Teléfono Padre": ''  # No disponible en BD
        }
        create_section("DATOS DE PADRES", parents_info)

        # 4. DATOS DE 1° TUTOR Y/O APODERADO SUPLENTE
        tutor1_info = {
            "Nombre": student_data.get('tutor1_nombre', ''),
            "Rut": student_data.get('tutor1_rut', ''),
            "Dirección": '',  # No disponible en BD
            "Teléfono": student_data.get('tutor1_telefono', '')
        }
        create_section("DATOS DE 1° TUTOR Y/O APODERADO SUPLENTE", tutor1_info)

        # 5. DATOS DE 2° TUTOR Y/O APODERADO SUPLENTE
        tutor2_info = {
            "Nombre": student_data.get('tutor2_nombre', ''),
            "Rut": student_data.get('tutor2_rut', ''),
            "Dirección": '',  # No disponible en BD
            "Teléfono": student_data.get('tutor2_telefono', ''),
            "Parentesco": ''  # No disponible en BD
        }
        create_section("DATOS DE 2° TUTOR Y/O APODERADO SUPLENTE", tutor2_info)

        # 6. SALUD ESTUDIANTE
        health_info = {
            "Ha estado en tratamiento Psicológico, Psicopedagógico, Fonoaudiológico u otro": '',
            "En la actualidad se encuentra en algún tratamiento": student_data.get('tratamiento_medico', ''),
            "Posee contraindicación para realizar actividad Física y/o deportiva": student_data.get('contraindicacion_fisica', ''),
            "Es alérgico a algún medicamento": student_data.get('alergias', '')
        }
        create_section("SALUD ESTUDIANTE", health_info)

        # 7. SISTEMA DE ADMISIÓN ESCOLAR
        sae_info = {
            "Sistema de Admisión Escolar": ''  # No disponible en BD
        }
        create_section("SISTEMA DE ADMISIÓN ESCOLAR", sae_info)

        # 8. ANTECEDENTES SOCIALES DEL ESTUDIANTE
        social_info = {
            "Registro Social": student_data.get('rsh_puntaje', ''),
            "Prioritario": student_data.get('alumno_prioritario', ''),
            "Puntaje": student_data.get('rsh_puntaje', ''),
            "Beca": student_data.get('beca', '')
        }
        create_section("ANTECEDENTES SOCIALES DEL ESTUDIANTE", social_info)

        # 9. COMPROMISO
        elements.append(Paragraph("COMPROMISO", self.styles['SubHeader']))
        compromiso_text = """El establecimiento se compromete a recibir los textos escolares que proveerá el Ministerio de Educación para el año 2026 y a entregárselos a los profesores y estudiantes. Además, se compromete a informar por escrito esta decisión a los padres y apoderados."""
        elements.append(Paragraph(compromiso_text, self.styles['NormalSmall']))
        elements.append(Spacer(1, 15))

        # 10. USO DE IMAGEN
        elements.append(Paragraph("USO DE IMAGEN", self.styles['SubHeader']))
        imagen_text = f"""Autorizo la difusión de imagen de mi hijo(a) en la página del establecimiento, con el fin de recoger, potenciar y difundir las buenas prácticas pedagógicas desarrolladas por nuestro establecimiento educacional. <b>Autorización: {'SI' if student_data.get('aut_imagen') == 1 else 'NO'}</b>"""
        elements.append(Paragraph(imagen_text, self.styles['NormalSmall']))
        elements.append(Spacer(1, 15))

        # 11. TOMA CONOCIMIENTO DE REGLAMENTOS INSTITUCIONALES
        elements.append(Paragraph("TOMA CONOCIMIENTO DE REGLAMENTOS INSTITUCIONALES", self.styles['SubHeader']))
        reglamento_text = f"""Los padres, apoderados o tutores aceptan el proyecto educativo institucional de nuestro Establecimiento y se comprometen a una total colaboración con el cumplimiento de este. Así mismo certifican que los datos aportados a esta ficha son ciertos, sin que figure ninguna falsedad u omisión de los mismos. El Apoderado/Tutor toma conocimiento quedándose con una copia de este documento. Toma conocimiento y acepta Reglamento de Convivencia Escolar 2026. Toma conocimiento y acepta Reglamento de Promoción y Evaluación Escolar Año 2026. Extractos de Reglamentos Institucionales Año 2026. Estos serán socializados en la primera reunión de apoderados del año, por redes sociales y grupos de cursos. <b>Aceptación: {' SI' if student_data.get('aut_reglamento') == 1 else ' NO'}</b>"""
        elements.append(Paragraph(reglamento_text, self.styles['NormalSmall']))
        elements.append(Spacer(1, 15))

        # 12. OBSERVACIONES
        obs_text = student_data.get('observaciones', '')
        elements.append(Paragraph("OBSERVACIONES", self.styles['SubHeader']))
        elements.append(Paragraph(obs_text if obs_text else '', self.styles['NormalSmall']))
        elements.append(Spacer(1, 15))

        # Signatures
        elements.append(Spacer(1, 50))
        data_sig = [
            ["___________________________", "___________________________"],
            ["Firma Apoderado", "Firma Dirección/Secretaría"]
        ]
        t_sig = Table(data_sig, colWidths=[250, 250])
        t_sig.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        elements.append(t_sig)

        # Footer w/ timestamp
        footer_text = f"Documento generado el: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
        elements.append(Spacer(1, 30))
        elements.append(Paragraph(footer_text, ParagraphStyle(name='Footer', fontSize=8, alignment=2, textColor=colors.grey)))

        try:
            doc.build(elements)
            return True, f"PDF generado: {self.filename}"
        except Exception as e:
            return False, f"Error al generar PDF: {e}"

if __name__ == "__main__":
    # Test Data
    dummy_data = {
        'fecha_matricula': '2024-02-12',
        'nombre_estudiante': 'Juan Pérez',
        'rut_estudiante': '12.345.678-9',
        'fecha_nacimiento': '2015-05-20',
        'edad': 9,
        'sexo': 'M',
        'direccion': 'Calle Falsa 123',
        'vive_con': 'Ambos padres',
        'colegio_anterior': 'Escuela A',
        'repitencia': 'No',
        'es_pie': 'No',
        'nombre_apoderado': 'María López',
        'tutor1_nombre': 'Pedro Pérez',
        'tutor1_telefono': '99999999',
    }
    pdf = PDFGenerator("test_matricula.pdf")
    success, msg = pdf.generate_pdf(dummy_data)
    print(msg)
