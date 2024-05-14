import tkinter as tk
from tkinter import simpledialog, messagebox, DISABLED
import customtkinter
from tkinter import PhotoImage
import random
from tkinter import ttk
from PIL import Image, ImageTk
import random


# Main application class
class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Main Menu of Connect & Conquer: Adruino Arena")
        self.iconbitmap("4_image/0_logo/Arduino logo transperant.png")
        self.geometry("500x200")

        # Buttons
        tk.Button(self, text="Start", command=self.open_challenges).pack(pady=10)
        tk.Button(self, text="Options", command=self.open_options).pack(pady=10)
        tk.Button(self, text="Credits", command=self.show_credits).pack(pady=10)
        tk.Button(self, text="Exit", command=self.quit).pack(pady=10)

    def open_challenges(self):
        # Disable the main window
        self.withdraw()
        # Open challenges window
        window = ChallengesWindow(self)
        window.grab_set()

    def open_options(self):
        OptionsWindow(self)

    def show_credits(self):
        credits = ("Team Members:\n"
                   "- Chrysostomos Koumides\n"
                   "- Niovi Peratikou\n"
                   "- Stratos Efstratiou\n"
                   "Teacher:\n"
                   "- Dr. Dimitriou Antonios")
        messagebox.showinfo("Credits", credits)

class OptionsWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Options")
        self.geometry("300x200")
        self.configure(bg='light grey')

        # Window size
        tk.Label(self, text="Window Dimensions:").pack(pady=10)
        self.entry_dimensions = tk.Entry(self)
        self.entry_dimensions.pack()

        # Color theme
        tk.Label(self, text="Color Theme:").pack(pady=10)
        self.var_theme = tk.StringVar(self)
        self.var_theme.set("light")  # default value
        tk.OptionMenu(self, self.var_theme, "light", "dark", "blue", "green").pack()

        tk.Button(self, text="Apply", command=self.apply_options).pack(pady=20)

    def apply_options(self):
        # Apply dimension changes
        dimensions = self.entry_dimensions.get()
        try:
            self.master.geometry(dimensions)
        except:
            messagebox.showerror("Error", "Invalid dimensions. Please use the format 'widthxheight'.")
        
        # Apply color theme
        theme = self.var_theme.get()
        if theme == 'light':
            self.master.configure(bg='white')
        elif theme == 'dark':
            self.master.configure(bg='gray')
        else:
            self.master.configure(bg=theme)


class ChallengesWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Current Challenges")
        self.geometry("400x400")
        self.configure(bg='white')

        # Icon for leaderboard
        self.leaderboard_icon = PhotoImage(file="leaderboard_icon_small.png")  # Ensure you have this icon image

        # Challenges
        tk.Button(self, text="Electrical and Computer Challenge", command=self.open_electrical_challenge,  compound='right').pack(pady=10)
        tk.Button(self, text="Physics Challenge", state=DISABLED,  compound='right').pack(pady=10)
        tk.Button(self, text="Sounds Challenge", state=DISABLED,  compound='right').pack(pady=10)
        tk.Button(self, text="Coming Soon", state=DISABLED,  compound='right').pack(pady=10)

    def open_electrical_challenge(self):
        introduction_text = (
            "Welcome to the Electrical and Computer Challenge!\n\n"
            "In this challenge, you will learn about digital logic gates and their applications in computing and electrical engineering. "
            "Please ensure that all necessary cables are connected and that all required software is running. "
            "Follow the on-screen instructions carefully to complete the experiments.\n\n"
            "Click 'OK' to start the challenge and open the logic gates simulation."
        )
        messagebox.showinfo("Electrical and Computer Challenge", introduction_text)
        LogicGateApp().mainloop()

class LogicGateApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Networked Digital Logic Gates")
        self.geometry("800x600")
        
        # Define the main frames first without adding any widgets
        self.top_frame = tk.Frame(self, height=300)
        self.bottom_frame = tk.Frame(self, height=300)
        self.top_frame.pack(fill=tk.X)
        self.bottom_frame.pack(fill=tk.X, expand=True)
        
        # Call update_gui to add widgets after the mainloop starts
        self.after(100, self.update_gui)

    def load_images(self):
        # Load images and keep them in attributes to ensure they stay in memory
        self.schematic_image = Image.open("schematic.png")
        self.schematic_photo = ImageTk.PhotoImage(self.schematic_image)
        self.video_image = Image.open("video_placeholder.png")
        self.video_photo = ImageTk.PhotoImage(self.video_image)

    def update_gui(self):
        self.load_images()
        # Add widgets that use images
        self.schematic_label = tk.Label(self.top_frame, image=self.schematic_photo)
        self.schematic_label.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.video_label = tk.Label(self.top_frame, image=self.video_photo)
        self.video_label.pack(side=tk.RIGHT, padx=10, pady=10)
        
        self.output_text = tk.Text(self.bottom_frame, height=10)
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        self.read_serial_button = ttk.Button(self.bottom_frame, text="Simulate Arduino Input", command=self.simulate_arduino_input)
        self.read_serial_button.pack(pady=10)

    def simulate_arduino_input(self):
        # Generate random logic gate and output
        gates = ['NotGate', 'OrGate', 'AndGate', 'NorGate', 'NandGate', 'XorGate', 'XnorGate']
        gate = random.choice(gates)
        output = random.choice(['HIGH', 'LOW'])
        simulated_data = f"Gate: {gate}, Output: {output}\n"
        self.output_text.insert(tk.END, simulated_data)
        self.after(1000, self.simulate_arduino_input)
        
# Run the application
if __name__ == "__main__":
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")
    root = customtkinter.CTk()
    app = MainApp(root)
    app.mainloop()
