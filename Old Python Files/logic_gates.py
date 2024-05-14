import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import random
import time

# Main application class
class LogicGateApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Networked Digital Logic Gates")
        self.geometry("800x600")

        # Load images and ensure they are kept in memory by storing them in attributes
        self.load_images()

        # Layout frames
        self.top_frame = tk.Frame(self, height=300)
        self.bottom_frame = tk.Frame(self, height=300)
        self.top_frame.pack(fill=tk.X)
        self.bottom_frame.pack(fill=tk.X, expand=True)

        # Add widgets
        self.schematic_label = tk.Label(self.top_frame, image=self.schematic_photo)
        self.schematic_label.pack(side=tk.LEFT, padx=10, pady=10)

        self.video_label = tk.Label(self.top_frame, image=self.video_photo)
        self.video_label.pack(side=tk.RIGHT, padx=10, pady=10)

        self.output_text = tk.Text(self.bottom_frame, height=10)
        self.output_text.pack(fill=tk.BOTH, expand=True)

        self.read_serial_button = ttk.Button(self.bottom_frame, text="Simulate Arduino Input", command=self.simulate_arduino_input)
        self.read_serial_button.pack(pady=10)

    def load_images(self):
        # Explicitly load images and keep them in attributes to ensure they stay in memory
        self.schematic_image = Image.open("schematic.png")
        self.schematic_photo = ImageTk.PhotoImage(self.schematic_image)
        self.video_image = Image.open("video_placeholder.png")
        self.video_photo = ImageTk.PhotoImage(self.video_image)

    def simulate_arduino_input(self):
        gates = ['NotGate', 'OrGate', 'AndGate', 'NorGate', 'NandGate', 'XorGate', 'XnorGate']
        gate = random.choice(gates)
        output = random.choice(['HIGH', 'LOW'])
        simulated_data = f"Gate: {gate}, Output: {output}\n"
        
        self.output_text.insert(tk.END, simulated_data)
        self.after(1000, self.simulate_arduino_input)  # Simulate new input every second

# Run the application
if __name__ == "__main__":
    app = LogicGateApp()
    app.mainloop()