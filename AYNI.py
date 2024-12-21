import tkinter as tk
from tkinter import messagebox
import random
import time

# Clase base para las páginas, proporciona un diseño común
class BasePage:
    def __init__(self, parent, title, bg_color="#E3F2FD", text_color="#0D47A1", font=("Helvetica", 16, "bold")):
        self.parent = parent
        self.bg_color = bg_color
        self.text_color = text_color
        self.font = font
        self.frame = tk.Frame(self.parent, bg=self.bg_color)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Etiqueta de título de la página
        self.title_label = tk.Label(
            self.frame,
            text=title,
            bg=self.bg_color,
            fg=self.text_color,
            font=self.font,
            pady=20,
            wraplength=320,
        )
        self.title_label.pack()

    def clear_frame(self):
        # Limpia el contenido de la página
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.frame.pack_forget()

# Página principal con el mensaje de bienvenida
class HomePage(BasePage):
    def __init__(self, parent):
        super().__init__(parent, "Bienvenido a AYNI EQUILIBRIO")

        # Mensaje adicional de bienvenida
        welcome_label = tk.Label(
            self.frame,
            text="Elige una sección para comenzar:",
            bg=self.bg_color,
            fg="#0D47A1",
            font=("Helvetica", 14),
            pady=10,
            wraplength=320,
        )
        welcome_label.pack()

# Página que muestra un consejo al usuario
class TipsPage(BasePage):
    def __init__(self, parent, go_back_callback):
        super().__init__(parent, "Consejo del día")

        # Lista de consejos predefinidos
        tips = [
            "Tómate un momento para respirar profundo hoy.",
            "Recuerda, este también es un buen día para empezar de nuevo.",
            "Escribe tres cosas por las que estés agradecido hoy.",
            "Haz una pausa y disfruta del momento presente.",
            "Cuida de ti mismo como cuidarías de un amigo querido."
        ]
        selected_tip = random.choice(tips)

        # Muestra el consejo seleccionado
        tip_label = tk.Label(
            self.frame,
            text=f"\u2022 {selected_tip}",
            bg=self.bg_color,
            fg="#37474F",
            font=("Helvetica", 12),
            wraplength=320,
            justify="left",
        )
        tip_label.pack(pady=20)

        # Botón para regresar a la página principal
        back_button = tk.Button(
            self.frame,
            text="Volver",
            command=go_back_callback,
            font=("Helvetica", 12),
            bg="#81D4FA",
            fg="white",
            relief="flat",
            pady=10,
        )
        back_button.pack(pady=20)

# Página para realizar un ejercicio de respiración guiado
import tkinter as tk

class ExercisePage(BasePage):
    def __init__(self, parent, go_back_callback):
        super().__init__(parent, "Ejercicio Guiado: Respiración")

        # Instrucciones iniciales
        self.instruction_label = tk.Label(
            self.frame,
            text="Inhala cuando el círculo se expanda y exhala cuando se contraiga.",
            bg=self.bg_color,
            fg="#37474F",
            font=("Helvetica", 12),
            wraplength=320,
        )
        self.instruction_label.pack(pady=5)

        # Lienzo para el círculo (aumento de tamaño del lienzo)
        self.canvas = tk.Canvas(
            self.frame, width=300, height=300, bg=self.bg_color, highlightthickness=0
        )
        self.canvas.pack(pady=10)

        # Círculo inicial (más grande)
        self.x1, self.y1, self.x2, self.y2 = 50, 50, 250, 250  # Círculo más grande
        self.circle = self.canvas.create_oval(self.x1, self.y1, self.x2, self.y2, fill="#81D4FA")

        # Variables de control
        self.running = False
        self.expand = True  # Estado de la animación (expandir o contraer)
        self.countdown_started = False  # Control para el conteo regresivo

        # Botón para retroceder
        back_button = tk.Button(
            self.frame,
            text="Volver",
            command=lambda: self.stop_animation_and_go_back(go_back_callback),
            font=("Helvetica", 12),
            bg="#81D4FA",
            fg="white",
            relief="flat",
            pady=10,
        )
        back_button.pack(pady=20)

        # Comenzar el conteo
        self.start_countdown()

    def start_countdown(self):
        # Muestra el mensaje del conteo regresivo
        self.instruction_label.config(text="Prepárate para el ejercicio...")
        self.countdown(3)  # Empieza el conteo de 3 segundos

    def countdown(self, time_left):
        # Actualiza el mensaje de conteo regresivo
        if time_left > 0:
            self.instruction_label.config(text=f"Comienza en {time_left}...")
            self.canvas.after(1000, self.countdown, time_left - 1)  # Llama la función después de 1 segundo
        else:
            # Al final del conteo, comienza el ejercicio de respiración
            self.instruction_label.config(text="Inhala... Respira profundamente.")
            self.running = True
            self.animate_breathing()  # Comienza la animación de respiración

    def animate_breathing(self):
        if self.running:
            if self.expand:
                # Agrandar el círculo al inhalar
                self.x1 -= 15
                self.y1 -= 15
                self.x2 += 15
                self.y2 += 15
                self.instruction_label.config(text="Inhala... Respira profundamente.")
            else:
                # Reducir el círculo al exhalar
                self.x1 += 15
                self.y1 += 15
                self.x2 -= 15
                self.y2 -= 15
                self.instruction_label.config(text="Exhala... Deja ir el aire lentamente.")

            # Actualizar las coordenadas del círculo
            self.canvas.coords(self.circle, self.x1, self.y1, self.x2, self.y2)

            # Cambiar la dirección (expandir o contraer)
            self.expand = not self.expand

            # Repetir la animación después de un intervalo de 2 segundos
            self.canvas.after(2000, self.animate_breathing)  # Intervalo de 2 segundos

    def stop_animation_and_go_back(self, go_back_callback):
        # Detener la animación y regresar
        self.running = False
        self.clear_frame()
        go_back_callback()



# Página para que el usuario escriba sus pensamientos
class JournalPage(BasePage):
    def __init__(self, parent, go_back_callback):
        super().__init__(parent, "Bitácora Emocional")

        # Instrucciones para el usuario
        prompt_label = tk.Label(
            self.frame,
            text="¿Cómo te sientes hoy? Escribe tus pensamientos abajo:",
            bg=self.bg_color,
            fg="#37474F",
            font=("Helvetica", 12),
            wraplength=320,
        )
        prompt_label.pack(pady=10)

        # Caja de texto para que el usuario escriba
        self.text_box = tk.Text(self.frame, height=10, width=30, wrap=tk.WORD, font=("Helvetica", 12))
        self.text_box.pack(padx=20, pady=10)

        # Botón para guardar la entrada
        save_button = tk.Button(
            self.frame,
            text="Guardar",
            command=self.save_entry,
            bg="#81D4FA",
            fg="white",
            font=("Helvetica", 12),
            relief="flat",
            padx=10,
            pady=5,
        )
        save_button.pack(pady=10)

        # Botón para regresar a la página principal
        back_button = tk.Button(
            self.frame,
            text="Volver",
            command=go_back_callback,
            font=("Helvetica", 12),
            bg="#81D4FA",
            fg="white",
            relief="flat",
            pady=10,
        )
        back_button.pack(pady=20)

    def save_entry(self):
        # Guarda la entrada escrita por el usuario
        entry_text = self.text_box.get("1.0", tk.END).strip()
        if entry_text:
            try:
                with open("journal_entries.txt", "a") as file:
                    file.write(entry_text + "\n---\n")
                messagebox.showinfo("Éxito", "Tu entrada ha sido guardada.")
                self.text_box.delete("1.0", tk.END)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar la entrada: {e}")
        else:
            messagebox.showwarning("Advertencia", "Por favor, escribe algo en la bitácora.")

# Clase principal de la aplicación
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicación Serenidad")
        self.root.geometry("360x640")  # Dimensiones para dispositivos móviles
        self.current_page = None
        self.main_menu()

    def main_menu(self):
        # Muestra el menú principal
        if self.current_page:
            self.current_page.clear_frame()

        home_page = HomePage(self.root)
        self.current_page = home_page

        home_page_frame = home_page.frame

        # Botón para ir a la página de consejos
        tips_button = tk.Button(
            home_page_frame,
            text="Consejos del Día",
            command=lambda: self.show_tips(home_page_frame),
            font=("Helvetica", 12),
            width=20,
            pady=10,
            bg="#81D4FA",
            fg="white",
        )
        tips_button.pack(pady=10)

        # Botón para ir a la página de ejercicios
        exercise_button = tk.Button(
            home_page_frame,
            text="Ejercicio Guiado",
            command=lambda: self.show_exercise(home_page_frame),
            font=("Helvetica", 12),
            width=20,
            pady=10,
            bg="#81D4FA",
            fg="white",
        )
        exercise_button.pack(pady=10)

        # Botón para ir a la página de bitácora
        journal_button = tk.Button(
            home_page_frame,
            text="Bitácora Emocional",
            command=lambda: self.show_journal(home_page_frame),
            font=("Helvetica", 12),
            width=20,
            pady=10,
            bg="#81D4FA",
            fg="white",
        )
        journal_button.pack(pady=10)

    def clear_main_buttons(self, home_page_frame):
        # Limpia los botones del menú principal
        for widget in home_page_frame.winfo_children():
            if isinstance(widget, tk.Button):
                widget.destroy()

    def show_tips(self, home_page_frame):
        # Muestra la página de consejos
        self.current_page.clear_frame()
        self.current_page = TipsPage(self.root, go_back_callback=self.main_menu)

    def show_exercise(self, home_page_frame):
        # Muestra la página de ejercicios
        self.current_page.clear_frame()
        self.current_page = ExercisePage(self.root, go_back_callback=self.main_menu)

    def show_journal(self, home_page_frame):
        self.current_page.clear_frame()
        self.current_page = JournalPage(self.root, go_back_callback=self.main_menu)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
