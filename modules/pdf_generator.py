from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import os
from datetime import datetime

class PDFGenerator:
    def __init__(self, filename="matricula.pdf"):
        self.filename = filename
        self.styles = getSampleStyleSheet()
        self.create_custom_styles()

    def create_custom_styles(self):
        self.styles.add(ParagraphStyle(name='Header', fontSize=14, leading=16, alignment=1, spaceAfter=20, fontName='Helvetica-Bold'))
        self.styles.add(ParagraphStyle(name='SubHeader', fontSize=12, leading=14, spaceAfter=10, fontName='Helvetica-Bold'))
        self.styles.add(ParagraphStyle(name='NormalSmall', fontSize=10, leading=12))
        self.styles.add(ParagraphStyle(name='Signature', fontSize=10, leading=12, alignment=1, spaceBefore=40))

    def generate_pdf(self, student_data):
        doc = SimpleDocTemplate(self.filename, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
        elements = []

        # Logo placeholders (optional)
        # elements.append(Image("assets/logo.png", width=50, height=50))

        # Title
        elements.append(Paragraph("FICHA DE MATRÍCULA AÑO ESCOLAR 2024", self.styles['Header']))
        elements.append(Spacer(1, 12))

        # Helper to create data rows
        def create_section(title, data_dict):
            elements.append(Paragraph(title, self.styles['SubHeader']))
            data = []
            for key, value in data_dict.items():
                data.append([Paragraph(f"<b>{key}:</b>", self.styles['NormalSmall']), Paragraph(str(value), self.styles['NormalSmall'])])
            
            t = Table(data, colWidths=[150, 350])
            t.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('BACKGROUND', (0, 0), (0, -1), colors.whitesmoke),
            ]))
            elements.append(t)
            elements.append(Spacer(1, 15))

        # 1. Datos del Estudiante
        student_info = {
            "N° Matrícula": student_data.get('num_matricula', ''),
            "Fecha Matrícula": student_data.get('fecha_matricula', ''),
            "Nombre Completo": student_data.get('nombre_estudiante', ''),
            "RUT": student_data.get('rut_estudiante', ''),
            "Fecha Nacimiento": student_data.get('fecha_nacimiento', ''),
            "Edad": student_data.get('edad', ''),
            "Sexo": student_data.get('sexo', ''),
            "Dirección": student_data.get('direccion', ''),
            "Con quién vive": student_data.get('vive_con', ''),
            "Colegio Anterior": student_data.get('colegio_anterior', ''),
            "Repitencia": student_data.get('repitencia', ''),
            "PIE": f"{student_data.get('es_pie', 'No')} - {student_data.get('diagnostico_pie', '')}"
        }
        create_section("1. ANTECEDENTES DEL ALUMNO", student_info)

        # 2. Datos Apoderado
        guardian_info = {
            "Nombre": student_data.get('nombre_apoderado', ''),
            "RUT": student_data.get('rut_apoderado', ''),
            "Teléfono": student_data.get('telefono_apoderado', ''),
            "Parentesco": student_data.get('parentesco_apoderado', ''),
            "Email": student_data.get('email_apoderado', '')
        }
        create_section("2. ANTECEDENTES DEL APODERADO TITULAR", guardian_info)

        # 3. Contactos Emergencia
        emergency_info = {
            "Contacto 1": f"{student_data.get('tutor1_nombre', '')} ({student_data.get('tutor1_telefono', '')})",
            "Contacto 2": f"{student_data.get('tutor2_nombre', '')} ({student_data.get('tutor2_telefono', '')})"
        }
        create_section("3. CONTACTOS DE EMERGENCIA", emergency_info)

        # 4. Salud
        health_info = {
            "Tratamiento Médico": student_data.get('tratamiento_medico', ''),
            "Alergias": student_data.get('alergias', '')
        }
        create_section("4. ANTECEDENTES DE SALUD", health_info)

        # 5. Observaciones (Nueva Sección)
        obs_text = student_data.get('observaciones', '')
        if obs_text:
            elements.append(Paragraph("5. OBSERVACIONES", self.styles['SubHeader']))
            elements.append(Paragraph(obs_text, self.styles['NormalSmall']))
            elements.append(Spacer(1, 15))

        # Declaration Text
        elements.append(Spacer(1, 20))
        declaration_text = """
        Declaro conocer y aceptar el Proyecto Educativo Institucional, el Reglamento Interno y el Reglamento de Evaluación. 
        Asimismo, autorizo el uso de la imagen de mi pupilo para fines pedagógicos y de difusión del establecimiento, 
        según lo marcado en la ficha.
        """
        elements.append(Paragraph(declaration_text, self.styles['NormalSmall']))
        
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
