import customtkinter as ctk
from tkinter import ttk, messagebox
from modules.database import DBManager
from modules.pdf_generator import PDFGenerator
from tkinter import filedialog
from datetime import datetime
from PIL import Image
import os
import sys

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class SchoolApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Matrícula Escolar")
        self.geometry("1100x700")

        self.db = DBManager()
        self.pdf_gen = PDFGenerator()
        
        self.current_student_id = None # Para controlar si es nuevo registro o edición

        # Layout configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1) # Row 1 captures the space for content now

        # ---- Header Frame ----
        self.header_frame = ctk.CTkFrame(self, height=80, corner_radius=0)
        self.header_frame.grid(row=0, column=0, sticky="ew")
        
        # Logo in Header
        logo_path = self.get_asset_path("logo.png")
        if os.path.exists(logo_path):
            try:
                header_image = ctk.CTkImage(light_image=Image.open(logo_path),
                                          dark_image=Image.open(logo_path),
                                          size=(50, 50))
                self.header_logo = ctk.CTkLabel(self.header_frame, image=header_image, text="")
                self.header_logo.pack(side="left", padx=20, pady=10)
            except Exception as e:
                print(f"Error loading header logo: {e}")

        # Title in Header
        self.header_title = ctk.CTkLabel(self.header_frame, text="Sistema de Matrícula Escolar - Escuela Los Leones", 
                                       font=ctk.CTkFont(size=20, weight="bold"))
        self.header_title.pack(side="left", padx=10)

        # Tabview (Now in Row 1)
        self.tabview = ctk.CTkTabview(self, width=1000)
        self.tabview.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        
        self.tab_form = self.tabview.add("Ficha de Matrícula")
        self.tab_list = self.tabview.add("Base de Datos")

        self.setup_form_tab()
        self.setup_list_tab()

    def get_asset_path(self, filename):
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_dir, "assets", filename)

    def setup_form_tab(self):
        self.scroll_frame = ctk.CTkScrollableFrame(self.tab_form, label_text="Formulario de Ingreso")
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Usaremos un grid de 4 columnas:
        # Col 0: Label Izq, Col 1: Entry Izq, Col 2: Label Der, Col 3: Entry Der
        self.scroll_frame.grid_columnconfigure(1, weight=1)
        self.scroll_frame.grid_columnconfigure(3, weight=1)

        # ---- Section 1: Datos del Estudiante ----
        self.add_section_header("1. Datos del Estudiante", 0)
        
        # Row 1
        self.entry_num_matricula = self.add_entry("N° de Matricula:", 1, 0)
        self.entry_fecha_matricula = self.add_entry("Fecha Matrícula:", 1, 1, default=datetime.now().strftime("%d-%m-%Y"))
        
        # Row 2
        self.entry_curso = self.add_entry("Curso al que matricula:", 2, 0)
        self.entry_rut_est = self.add_entry("RUT:", 2, 1)

        # Row 3
        self.entry_nombre_est = self.add_entry("Nombre Completo:", 3, 0)
        self.entry_fecha_nac = self.add_entry("Fecha Nacimiento:", 3, 1, default="", placeholder="dd-mm-yyyy")
        self.entry_fecha_nac.bind("<KeyRelease>", self.format_date_and_calculate_age)

        # Row 4
        self.entry_nacionalidad = self.add_entry("Nacionalidad:", 4, 0)
        self.entry_edad = self.add_entry("Edad:", 4, 1)

        # Row 5
        self.entry_sexo = self.add_entry("Sexo:", 5, 0) 
        self.entry_direccion = self.add_entry("Dirección:", 5, 1)

        # Row 6
        self.entry_comuna = self.add_entry("Comuna:", 6, 0)
        self.entry_vive_con = self.add_entry("Con quién vive:", 6, 1)

        # Row 7
        self.entry_colegio_ant = self.add_entry("Colegio Anterior:", 7, 0)
        
        # Repitencia (Radiobuttons)
        self.lbl_repitencia = ctk.CTkLabel(self.scroll_frame, text="¿Repitencia?:")
        self.lbl_repitencia.grid(row=8, column=0, sticky="w", padx=10)
        
        self.frame_repitencia = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        self.frame_repitencia.grid(row=8, column=1, sticky="w", padx=10)
        self.repitencia_var = ctk.StringVar(value="No")
        self.rb_repitencia_si = ctk.CTkRadioButton(self.frame_repitencia, text="Si", variable=self.repitencia_var, value="Si")
        self.rb_repitencia_si.pack(side="left", padx=(0, 20))
        self.rb_repitencia_no = ctk.CTkRadioButton(self.frame_repitencia, text="No", variable=self.repitencia_var, value="No")
        self.rb_repitencia_no.pack(side="left")

        
        self.lbl_pie = ctk.CTkLabel(self.scroll_frame, text="¿Asiste a PIE?:")
        self.lbl_pie.grid(row=9, column=0, sticky="w", padx=10)
        
        self.frame_pie = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        self.frame_pie.grid(row=9, column=1, sticky="w", padx=10)
        self.es_pie_var = ctk.StringVar(value="No")
        self.rb_pie_si = ctk.CTkRadioButton(self.frame_pie, text="Si", variable=self.es_pie_var, value="Si")
        self.rb_pie_si.pack(side="left", padx=(0, 20))
        self.rb_pie_no = ctk.CTkRadioButton(self.frame_pie, text="No", variable=self.es_pie_var, value="No")
        self.rb_pie_no.pack(side="left")

        # Corrección: Usar add_entry con la fila correcta y NO agregar label manual extra
        self.entry_diag_pie = self.add_entry("Diagnóstico PIE:", 9, 1) 

        # ---- Section 2: Datos Apoderado ----
        self.add_section_header("2. Datos Apoderado Titular", 10)
        self.entry_nom_apo = self.add_entry("Nombre Apoderado:", 11, 0)
        self.entry_rut_apo = self.add_entry("RUT Apoderado:", 11, 1)

        # Row 12
        self.entry_tel_apo = self.add_entry("Teléfono:", 12, 0)
        
        # Parentesco (ComboBox)
        self.lbl_parentesco = ctk.CTkLabel(self.scroll_frame, text="Parentesco:")
        self.lbl_parentesco.grid(row=12, column=2, sticky="w", padx=10)
        self.combo_parentesco = ctk.CTkComboBox(self.scroll_frame, values=["MADRE", "PADRE", "ABUELA/ABUELO", "TIA/TIO", "HERMANA/HERMANO", "OTRO"], width=200)
        self.combo_parentesco.grid(row=12, column=3, pady=2, padx=10, sticky="ew")

        # Row 13
        self.entry_prof_apo = self.add_entry("Profesión/Oficio:", 13, 0)
        self.entry_email_apo = self.add_entry("Email:", 13, 1)

        # Row 14
        self.entry_dir_apo = self.add_entry("Dirección (si distinta):", 14, 0)

        # ---- Section 3: Padres ----
        self.add_section_header("3. Datos de los Padres", 15)
        self.entry_nom_madre = self.add_entry("Nombre Madre:", 16, 0)
        self.entry_rut_madre = self.add_entry("RUT Madre:", 16, 1)
        self.entry_nom_padre = self.add_entry("Nombre Padre:", 17, 0)
        self.entry_rut_padre = self.add_entry("RUT Padre:", 17, 1)

        # ---- Section 4: Emergencia ----
        self.add_section_header("4. Contactos de Emergencia", 18)
        self.entry_tut1_nom = self.add_entry("Tutor 1 Nombre:", 19, 0)
        self.entry_tut1_tel = self.add_entry("Tutor 1 Teléfono:", 19, 1)
        self.entry_tut2_nom = self.add_entry("Tutor 2 Nombre:", 20, 0)
        self.entry_tut2_tel = self.add_entry("Tutor 2 Teléfono:", 20, 1)

        # ---- Section 5: Salud y Social ----
        self.add_section_header("5. Salud y Antecedentes Sociales", 21)
        self.entry_tratamiento = self.add_entry("Tratamiento Médico:", 22, 0)
        self.entry_alergias = self.add_entry("Alergias:", 22, 1)
        self.entry_rsh = self.add_entry("Puntaje RSH:", 23, 0)
        
        # Prioritario (Radiobuttons)
        self.lbl_prioritario = ctk.CTkLabel(self.scroll_frame, text="Alumno Prioritario:")
        self.lbl_prioritario.grid(row=23, column=2, sticky="w", padx=10)
        
        self.frame_prio = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        self.frame_prio.grid(row=23, column=3, sticky="w", padx=10)
        self.prioritario_var = ctk.StringVar(value="No")
        self.rb_prio_si = ctk.CTkRadioButton(self.frame_prio, text="Si", variable=self.prioritario_var, value="Si")
        self.rb_prio_si.pack(side="left", padx=(0, 20))
        self.rb_prio_no = ctk.CTkRadioButton(self.frame_prio, text="No", variable=self.prioritario_var, value="No")
        self.rb_prio_no.pack(side="left")

        # ---- Section 6: Autorizaciones ----
        self.add_section_header("6. Autorizaciones", 24)
        self.chk_imagen_var = ctk.IntVar()
        self.chk_reglamento_var = ctk.IntVar()
        self.chk_textos_var = ctk.IntVar()

        # Observaciones
        self.label_obs = ctk.CTkLabel(self.scroll_frame, text="Observaciones:")
        self.label_obs.grid(row=25, column=0, sticky="w", padx=10, pady=(10, 0))
        self.entry_observaciones = ctk.CTkTextbox(self.scroll_frame, height=60)
        self.entry_observaciones.grid(row=26, column=0, columnspan=4, padx=10, pady=(0, 10), sticky="ew")
        
        # Checkboxes agrupados
        self.frame_aut = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        self.frame_aut.grid(row=27, column=0, columnspan=4, pady=5, padx=10, sticky="w")
        
        self.chk_imagen = ctk.CTkCheckBox(self.frame_aut, text="Autorizo uso de imagen", variable=self.chk_imagen_var)
        self.chk_imagen.pack(side="left", padx=(0, 30))
        
        self.chk_reglamento = ctk.CTkCheckBox(self.frame_aut, text="Acepto reglamentos internos", variable=self.chk_reglamento_var)
        self.chk_reglamento.pack(side="left")
        
        # Save Button (Centrado y ancho fijo razonable)
        self.btn_save = ctk.CTkButton(self.scroll_frame, text="Guardar Matrícula", command=self.save_student, height=40, width=200, fg_color="green")
        self.btn_save.grid(row=28, column=0, columnspan=4, pady=20, padx=20) # Removed sticky="ew" to use fixed width


    def add_section_header(self, text, row):
        label = ctk.CTkLabel(self.scroll_frame, text=text, font=ctk.CTkFont(size=16, weight="bold"))
        label.grid(row=row, column=0, columnspan=4, pady=(15, 5), sticky="w", padx=10)

    def add_entry(self, text, row, section_col, default="", placeholder=""):
        """
        section_col: 0 for Left pair (Cols 0-1), 1 for Right pair (Cols 2-3)
        """
        # Calculate actual grid columns
        # If section_col is 0 -> Label at 0, Entry at 1
        # If section_col is 1 -> Label at 2, Entry at 3
        
        label_col = 0 if section_col == 0 else 2
        entry_col = 1 if section_col == 0 else 3
        
        label = ctk.CTkLabel(self.scroll_frame, text=text)
        label.grid(row=row, column=label_col, sticky="w", padx=10)
        
        entry = ctk.CTkEntry(self.scroll_frame, width=200, placeholder_text=placeholder) # Reduced width slightly to fit better
        entry.grid(row=row, column=entry_col, pady=2, padx=10, sticky="ew")
        
        if default:
            entry.insert(0, default)
        return entry

    def format_date_and_calculate_age(self, event):
        entry = self.entry_fecha_nac
        text = entry.get()
        
        # Remove non-digits
        clean_text = ''.join(filter(str.isdigit, text))
        
        formatted = clean_text
        if len(clean_text) > 2:
            formatted = clean_text[:2] + '-' + clean_text[2:]
        if len(clean_text) > 4:
            formatted = formatted[:5] + '-' + clean_text[4:8]
            
        # Limit length
        if len(formatted) > 10:
            formatted = formatted[:10]
            
        if text != formatted:
             entry.delete(0, 'end')
             entry.insert(0, formatted)

        # Calculate Age
        if len(formatted) == 10:
            try:
                dob = datetime.strptime(formatted, "%d-%m-%Y")
                today = datetime.now()
                age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                
                self.entry_edad.delete(0, 'end')
                self.entry_edad.insert(0, str(age))
            except ValueError:
                pass

    def get_form_data(self):
        raw_data = {
            "num_matricula": self.entry_num_matricula.get(),
            "fecha_matricula": self.entry_fecha_matricula.get(),
            "curso_matricula": self.entry_curso.get(),
            "nombre_estudiante": self.entry_nombre_est.get(),
            "rut_estudiante": self.entry_rut_est.get(),
            "fecha_nacimiento": self.entry_fecha_nac.get(),
            "nacionalidad": self.entry_nacionalidad.get(),
            "edad": self.entry_edad.get(),
            "sexo": self.entry_sexo.get(),
            "direccion": self.entry_direccion.get(),
            "comuna": self.entry_comuna.get(),
            "vive_con": self.entry_vive_con.get(),
            "colegio_anterior": self.entry_colegio_ant.get(),
            "repitencia": self.repitencia_var.get(),
            "es_pie": self.es_pie_var.get(),
            "diagnostico_pie": self.entry_diag_pie.get(),
            "nombre_apoderado": self.entry_nom_apo.get(),
            "rut_apoderado": self.entry_rut_apo.get(),
            "telefono_apoderado": self.entry_tel_apo.get(),
            "parentesco_apoderado": self.combo_parentesco.get(),
            "profesion_apoderado": self.entry_prof_apo.get(),
            "direccion_apoderado": self.entry_dir_apo.get(),
            "email_apoderado": self.entry_email_apo.get(),
            "nombre_madre": self.entry_nom_madre.get(),
            "rut_madre": self.entry_rut_madre.get(),
            "nombre_padre": self.entry_nom_padre.get(),
            "rut_padre": self.entry_rut_padre.get(),
            "tutor1_nombre": self.entry_tut1_nom.get(),
            "tutor1_telefono": self.entry_tut1_tel.get(),
            "tutor2_nombre": self.entry_tut2_nom.get(),
            "tutor2_telefono": self.entry_tut2_tel.get(),
            "tratamiento_medico": self.entry_tratamiento.get(),
            "alergias": self.entry_alergias.get(),
            "rsh_puntaje": self.entry_rsh.get(),
            "alumno_prioritario": self.prioritario_var.get(),
            "aut_imagen": self.chk_imagen_var.get(),
            "aut_reglamento": self.chk_reglamento_var.get(),
            "observaciones": self.entry_observaciones.get("1.0", "end-1c")
        }
        
        # Convert all string values to UPPERCASE
        clean_data = {}
        for key, value in raw_data.items():
            if isinstance(value, str):
                clean_data[key] = value.upper()
            else:
                clean_data[key] = value
                
        return clean_data
    
    def clear_form(self):
        # Clear entries
        entries = [
            self.entry_num_matricula, self.entry_curso, self.entry_nombre_est, self.entry_rut_est, self.entry_fecha_nac,
            self.entry_nacionalidad, self.entry_edad, self.entry_sexo, self.entry_direccion,
            self.entry_comuna, self.entry_vive_con, self.entry_colegio_ant,
            self.entry_diag_pie, self.entry_nom_apo, self.entry_rut_apo, self.entry_tel_apo,
            self.entry_prof_apo, self.entry_email_apo, self.entry_dir_apo,
            self.entry_nom_madre, self.entry_rut_madre, self.entry_nom_padre, self.entry_rut_padre,
            self.entry_tut1_nom, self.entry_tut1_tel, self.entry_tut2_nom, self.entry_tut2_tel,
            self.entry_tratamiento, self.entry_alergias, self.entry_rsh
        ]
        for entry in entries:
            entry.delete(0, 'end')

        # Reset Date to Today
        self.entry_fecha_matricula.delete(0, 'end')
        self.entry_fecha_matricula.insert(0, datetime.now().strftime("%d-%m-%Y"))

        # Reset RadioButtons & Combos
        self.repitencia_var.set("No")
        self.es_pie_var.set("No")
        self.prioritario_var.set("No")
        self.combo_parentesco.set("PADRE")

        # Reset Checkboxes
        self.chk_imagen_var.set(0)
        self.chk_reglamento_var.set(0)
        self.chk_textos_var.set(0)

        # Clear Textbox
        self.entry_observaciones.delete("1.0", "end")
        
        # Reset Edit State
        self.current_student_id = None
        self.btn_save.configure(text="Guardar Matrícula", fg_color="green")
        
        # Set focus to top
        self.entry_num_matricula.focus()

    def load_student_data(self, data):
        self.tabview.set("Ficha de Matrícula")
        self.update_idletasks() # Force UI update
        
        self.clear_form()
        self.current_student_id = data['id']
        self.btn_save.configure(text="Actualizar Matrícula", fg_color="blue")
        
        # Helper to set entry text
        def set_entry(entry, value):
            entry.delete(0, 'end')
            if value:
                entry.insert(0, value)

        set_entry(self.entry_num_matricula, data.get('num_matricula'))
        set_entry(self.entry_fecha_matricula, data.get('fecha_matricula'))
        set_entry(self.entry_curso, data.get('curso_matricula'))
        set_entry(self.entry_nombre_est, data.get('nombre_estudiante'))
        set_entry(self.entry_rut_est, data.get('rut_estudiante'))
        set_entry(self.entry_fecha_nac, data.get('fecha_nacimiento'))
        set_entry(self.entry_nacionalidad, data.get('nacionalidad'))
        set_entry(self.entry_edad, data.get('edad'))
        set_entry(self.entry_sexo, data.get('sexo'))
        set_entry(self.entry_direccion, data.get('direccion'))
        set_entry(self.entry_comuna, data.get('comuna'))
        set_entry(self.entry_vive_con, data.get('vive_con'))
        set_entry(self.entry_colegio_ant, data.get('colegio_anterior'))
        
        # Radios
        self.repitencia_var.set(data.get('repitencia', 'No'))
        self.es_pie_var.set(data.get('es_pie', 'No'))
        self.prioritario_var.set(data.get('alumno_prioritario', 'No'))
        
        set_entry(self.entry_diag_pie, data.get('diagnostico_pie'))
        
        # Apoderados
        set_entry(self.entry_nom_apo, data.get('nombre_apoderado'))
        set_entry(self.entry_rut_apo, data.get('rut_apoderado'))
        set_entry(self.entry_tel_apo, data.get('telefono_apoderado'))
        self.combo_parentesco.set(data.get('parentesco_apoderado', 'PADRE'))
        set_entry(self.entry_prof_apo, data.get('profesion_apoderado'))
        set_entry(self.entry_email_apo, data.get('email_apoderado'))
        set_entry(self.entry_dir_apo, data.get('direccion_apoderado'))
        
        set_entry(self.entry_nom_madre, data.get('nombre_madre'))
        set_entry(self.entry_rut_madre, data.get('rut_madre'))
        set_entry(self.entry_nom_padre, data.get('nombre_padre'))
        set_entry(self.entry_rut_padre, data.get('rut_padre'))
        
        set_entry(self.entry_tut1_nom, data.get('tutor1_nombre'))
        set_entry(self.entry_tut1_tel, data.get('tutor1_telefono'))
        set_entry(self.entry_tut2_nom, data.get('tutor2_nombre'))
        set_entry(self.entry_tut2_tel, data.get('tutor2_telefono'))
        
        set_entry(self.entry_tratamiento, data.get('tratamiento_medico'))
        set_entry(self.entry_alergias, data.get('alergias'))
        set_entry(self.entry_rsh, data.get('rsh_puntaje'))
        
        # Checkboxes 
        self.chk_imagen_var.set(data.get('aut_imagen', 0))
        self.chk_reglamento_var.set(data.get('aut_reglamento', 0))
        
        # Observaciones
        self.entry_observaciones.delete("1.0", "end")
        if data.get('observaciones'):
            self.entry_observaciones.insert("1.0", data.get('observaciones'))

    def save_student(self):
        data = self.get_form_data()
        if not data['nombre_estudiante'] or not data['rut_estudiante']:
            messagebox.showerror("Error", "Nombre y RUT del estudiante son obligatorios.")
            return

        if self.current_student_id:
            # Update
            success, msg = self.db.actualizar_estudiante(self.current_student_id, data)
        else:
            # Insert
            success, msg = self.db.agregar_estudiante(data)

        if success:
            messagebox.showinfo("Éxito", msg)
            self.refresh_list()
            self.clear_form() # This resets the state and button text
        else:
            messagebox.showerror("Error", msg)

    def setup_list_tab(self):
        # Frame for controls
        self.frame_controls = ctk.CTkFrame(self.tab_list)
        self.frame_controls.pack(fill="x", padx=10, pady=10)

        self.entry_search = ctk.CTkEntry(self.frame_controls, placeholder_text="Buscar por Nombre, RUT o Curso")
        self.entry_search.pack(side="left", padx=10, fill="x", expand=True)
        
        self.btn_search = ctk.CTkButton(self.frame_controls, text="Buscar", command=self.search_student)
        self.btn_search.pack(side="left", padx=5)

        self.btn_refresh = ctk.CTkButton(self.frame_controls, text="Recargar", command=self.refresh_list, fg_color="gray")
        self.btn_refresh.pack(side="left", padx=5)

        self.btn_export = ctk.CTkButton(self.frame_controls, text="Exportar Excel", command=self.export_excel, fg_color="green")
        self.btn_export.pack(side="right", padx=5)

        self.btn_pdf = ctk.CTkButton(self.frame_controls, text="Generar PDF", command=self.generate_selected_pdf, fg_color="orange")
        self.btn_pdf.pack(side="right", padx=5)
        
        self.btn_edit = ctk.CTkButton(self.frame_controls, text="Editar", command=self.edit_student, fg_color="blue")
        self.btn_edit.pack(side="right", padx=5)

        self.btn_delete = ctk.CTkButton(self.frame_controls, text="Eliminar", command=self.delete_student, fg_color="red")
        self.btn_delete.pack(side="right", padx=5)

        # Container for Treeview and Scrollbars
        self.frame_tree = ctk.CTkFrame(self.tab_list)
        self.frame_tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Treeview styling
        style = ttk.Style()
        style.theme_use("clam")
        
        # Define ALL columns
        self.columns = [
            "ID", "N° Matrícula", "Fecha Matrícula", "Curso", "Nombre Estudiante", "RUT Estudiante", 
            "Fecha Nacimiento", "Nacionalidad", "Edad", "Sexo", "Dirección", "Comuna", 
            "Vive Con", "Colegio Anterior", "Repitencia", "PIE", "Diag. PIE", 
            "Nombre Apoderado", "RUT Apoderado", "Teléfono Apoderado", "Parentesco", 
            "Profesión", "Email", "Dirección Apoderado", 
            "Nombre Madre", "RUT Madre", "Nombre Padre", "RUT Padre",
            "Tutor 1", "Tel 1", "Tutor 2", "Tel 2",
            "Tratamiento", "Alergias", "RSH", "Prioritario",
            "Aut. Imagen", "Aut. Reglamento", "Observaciones"
        ]
        
        self.tree = ttk.Treeview(self.frame_tree, columns=self.columns, show="headings", selectmode="browse")
        
        # Setup headings and columns
        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, minwidth=100) # Default width
            
        # Specific widths
        self.tree.column("ID", width=40, minwidth=40)
        self.tree.column("RUT Estudiante", width=100)
        self.tree.column("Nombre Estudiante", width=200)

        # Scrollbars
        self.vsb = ttk.Scrollbar(self.frame_tree, orient="vertical", command=self.tree.yview)
        self.hsb = ttk.Scrollbar(self.frame_tree, orient="horizontal", command=self.tree.xview)
        
        self.tree.configure(yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)
        
        self.vsb.pack(side="right", fill="y")
        self.hsb.pack(side="bottom", fill="x")
        self.tree.pack(fill="both", expand=True)
        
        self.refresh_list()

    def refresh_list(self):
        # Clear search entries when refreshing
        self.entry_search.delete(0, 'end')

        for i in self.tree.get_children():
            self.tree.delete(i)
        
        students = self.db.obtener_estudiantes()
        for s in students:
            # Construct values list matching self.columns order
            values = [
                s.get('id', ''),
                s.get('num_matricula', ''),
                s.get('fecha_matricula', ''),
                s.get('curso_matricula', ''),
                s.get('nombre_estudiante', ''),
                s.get('rut_estudiante', ''),
                s.get('fecha_nacimiento', ''),
                s.get('nacionalidad', ''),
                s.get('edad', ''),
                s.get('sexo', ''),
                s.get('direccion', ''),
                s.get('comuna', ''),
                s.get('vive_con', ''),
                s.get('colegio_anterior', ''),
                s.get('repitencia', ''),
                s.get('es_pie', ''),
                s.get('diagnostico_pie', ''),
                s.get('nombre_apoderado', ''),
                s.get('rut_apoderado', ''),
                s.get('telefono_apoderado', ''),
                s.get('parentesco_apoderado', ''),
                s.get('profesion_apoderado', ''),
                s.get('email_apoderado', ''),
                s.get('direccion_apoderado', ''),
                s.get('nombre_madre', ''),
                s.get('rut_madre', ''),
                s.get('nombre_padre', ''),
                s.get('rut_padre', ''),
                s.get('tutor1_nombre', ''),
                s.get('tutor1_telefono', ''),
                s.get('tutor2_nombre', ''),
                s.get('tutor2_telefono', ''),
                s.get('tratamiento_medico', ''),
                s.get('alergias', ''),
                s.get('rsh_puntaje', ''),
                s.get('alumno_prioritario', ''),
                "Si" if s.get('aut_imagen') == 1 else "No",
                "Si" if s.get('aut_reglamento') == 1 else "No",
                s.get('observaciones', '')
            ]
            self.tree.insert("", "end", values=values)

    def search_student(self):
        term = self.entry_search.get()
        students = self.db.buscar_estudiantes(term)
        for i in self.tree.get_children():
            self.tree.delete(i)
        for s in students:
             # Repetir logica de valores, idealmente refactorizar en un metodo pero por ahora duplicamos para ser explícitos
            values = [
                s.get('id', ''),
                s.get('num_matricula', ''),
                s.get('fecha_matricula', ''),
                s.get('curso_matricula', ''),
                s.get('nombre_estudiante', ''),
                s.get('rut_estudiante', ''),
                s.get('fecha_nacimiento', ''),
                s.get('nacionalidad', ''),
                s.get('edad', ''),
                s.get('sexo', ''),
                s.get('direccion', ''),
                s.get('comuna', ''),
                s.get('vive_con', ''),
                s.get('colegio_anterior', ''),
                s.get('repitencia', ''),
                s.get('es_pie', ''),
                s.get('diagnostico_pie', ''),
                s.get('nombre_apoderado', ''),
                s.get('rut_apoderado', ''),
                s.get('telefono_apoderado', ''),
                s.get('parentesco_apoderado', ''),
                s.get('profesion_apoderado', ''),
                s.get('email_apoderado', ''),
                s.get('direccion_apoderado', ''),
                s.get('nombre_madre', ''),
                s.get('rut_madre', ''),
                s.get('nombre_padre', ''),
                s.get('rut_padre', ''),
                s.get('tutor1_nombre', ''),
                s.get('tutor1_telefono', ''),
                s.get('tutor2_nombre', ''),
                s.get('tutor2_telefono', ''),
                s.get('tratamiento_medico', ''),
                s.get('alergias', ''),
                s.get('rsh_puntaje', ''),
                s.get('alumno_prioritario', ''),
                "Si" if s.get('aut_imagen') == 1 else "No",
                "Si" if s.get('aut_reglamento') == 1 else "No",
                s.get('observaciones', '')
            ]
            self.tree.insert("", "end", values=values)

    def get_selected_id(self):
        selected = self.tree.selection()
        if not selected:
            return None
        item = self.tree.item(selected[0])
        # ID is at index 0
        return item['values'][0]

    def edit_student(self):
        student_id = self.get_selected_id()
        if not student_id:
            messagebox.showwarning("Aviso", "Seleccione un estudiante para editar.")
            return

        # Fetch full data by ID
        student_data = self.db.obtener_estudiante_por_id(student_id)
        
        if student_data:
            self.load_student_data(student_data)
        else:
            messagebox.showerror("Error", f"No se encontraron los datos del estudiante (ID: {student_id}).")

    def delete_student(self):
        student_id = self.get_selected_id()
        if not student_id:
            messagebox.showwarning("Aviso", "Seleccione un estudiante para eliminar.")
            return

        confirm = messagebox.askyesno("Confirmar", f"¿Eliminar al estudiante seleccionado (ID: {student_id})?")
        if confirm:
            success, msg = self.db.eliminar_estudiante_por_id(student_id)
            if success:
                messagebox.showinfo("Éxito", msg)
                self.refresh_list()
            else:
                messagebox.showerror("Error", msg)

    def export_excel(self):
        filename = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
        if filename:
            success, msg = self.db.exportar_excel(filename)
            if success:
                messagebox.showinfo("Éxito", msg)
            else:
                messagebox.showerror("Error", msg)

    def generate_selected_pdf(self):
        student_id = self.get_selected_id()
        if not student_id:
            messagebox.showwarning("Aviso", "Seleccione un estudiante para generar el PDF.")
            return
        
        # Fetch data by ID
        student_data = self.db.obtener_estudiante_por_id(student_id)
        
        if student_data:
            rut = student_data.get('rut_estudiante', 'sin_rut')
            initial_name = f"Matricula_{rut}.pdf"
            
            filename = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")], initialfile=initial_name)
            if filename:
                self.pdf_gen.filename = filename # Update filename target
                try:
                    success, msg = self.pdf_gen.generate_pdf(student_data)
                    if success:
                        messagebox.showinfo("Éxito", msg)
                    else:
                        messagebox.showerror("Error", msg)
                except Exception as e:
                    messagebox.showerror("Error Crítico", f"Falló la generación del PDF: {str(e)}")
        else:
            messagebox.showerror("Error", f"No se encontraron los datos del estudiante (ID: {student_id}).")


if __name__ == "__main__":
    from modules.login import LoginWindow
    
    login_app = LoginWindow()
    login_app.mainloop()

    if login_app.authenticated:
        app = SchoolApp()
        app.mainloop()
