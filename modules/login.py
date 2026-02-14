import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import os
import sys

class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Login - Sistema de Matrícula")
        self.geometry("400x450") # Increased height for logo
        self.resizable(False, False)

        self.authenticated = False

        # Center the window on screen
        self.eval('tk::PlaceWindow . center')

        self.setup_ui()

    def get_asset_path(self, filename):
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_dir, "assets", filename)

    def setup_ui(self):
        # Logo
        logo_path = self.get_asset_path("logo.png")
        if os.path.exists(logo_path):
            try:
                my_image = ctk.CTkImage(light_image=Image.open(logo_path),
                                      dark_image=Image.open(logo_path),
                                      size=(100, 100))
                self.logo_label = ctk.CTkLabel(self, image=my_image, text="")
                self.logo_label.pack(pady=(20, 10))
            except Exception as e:
                print(f"Error loading logo: {e}")

        # Title Label
        self.lbl_title = ctk.CTkLabel(self, text="SISTEMA DE ADMINISTRACIÓN DE\nMATRICULAS ESCUELA LOS LEONES", 
                                      font=ctk.CTkFont(size=16, weight="bold"), justify="center")
        self.lbl_title.pack(pady=(10, 20), padx=20)

        # Username
        self.entry_user = ctk.CTkEntry(self, placeholder_text="Usuario")
        self.entry_user.pack(pady=10, padx=50, fill="x")

        # Password
        self.entry_pass = ctk.CTkEntry(self, placeholder_text="Contraseña", show="*")
        self.entry_pass.pack(pady=10, padx=50, fill="x")

        # Login Button
        self.btn_login = ctk.CTkButton(self, text="Iniciar Sesión", command=self.check_login)
        self.btn_login.pack(pady=20, padx=50, fill="x")
        
        # Bind Enter key to login
        self.bind('<Return>', lambda event: self.check_login())

    def check_login(self):
        user = self.entry_user.get()
        password = self.entry_pass.get()

        if user == "admin" and password == "admin":
            self.authenticated = True
            self.destroy() # Close login window
        else:
            messagebox.showerror("Error", "Credenciales incorrectas.\nIntente nuevamente.")

if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()
