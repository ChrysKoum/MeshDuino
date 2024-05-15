import tkinter as tk
from tkinter import Canvas, Text, ttk, simpledialog
from PIL import Image, ImageTk
import random
import time
import cv2
from threading import Thread
from pathlib import Path

# Define the relative_to_assets function
def relative_to_assets(path: str) -> Path:
    return Path(__file__).parent / "assets" / Path(path)

class LogicGateApp(tk.Toplevel):
    def __init__(self, master, switch_to_maze_app):
        super().__init__(master)
        self.title("Networked Digital Logic Gates")
        self.geometry("800x600")
        self.switch_to_maze_app = switch_to_maze_app

        self.canvas = Canvas(self, bg="#FFFFFF", width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.load_images()
        self.create_widgets()
        self.start_time = time.time()
        self.video_thread = None
        self.cap = None

    def load_images(self):
        self.schematic_image = Image.open(relative_to_assets("logic_gate_schematic.png"))
        self.schematic_photo = ImageTk.PhotoImage(self.schematic_image)

    def create_widgets(self):
        self.canvas.create_image(150, 150, image=self.schematic_photo, anchor=tk.NW)

        self.output_text = Text(self, height=10, width=80)
        self.canvas.create_window(400, 450, window=self.output_text)

        self.read_serial_button = ttk.Button(self, text="Simulate Arduino Input", command=self.simulate_arduino_input)
        self.canvas.create_window(400, 550, window=self.read_serial_button)

        # Start video playback
        self.video_label = tk.Label(self)
        self.video_label.place(x=450, y=150)
        self.play_video(relative_to_assets("your_video.mp4"))

    def play_video(self, video_path):
        self.cap = cv2.VideoCapture(str(video_path))

        def stream():
            while self.cap.isOpened():
                ret, frame = self.cap.read()
                if not ret:
                    break

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.video_label.imgtk = imgtk
                self.video_label.config(image=imgtk)
                time.sleep(0.03)

            self.cap.release()

        self.video_thread = Thread(target=stream, daemon=True)
        self.video_thread.start()

    def simulate_arduino_input(self):
        gates = ['NotGate', 'OrGate', 'AndGate', 'NorGate', 'NandGate', 'XorGate', 'XnorGate']
        gate = random.choice(gates)
        output = random.choice(['HIGH', 'LOW'])
        simulated_data = f"Gate: {gate}, Output: {output}\n"

        self.output_text.insert(tk.END, simulated_data)
        self.after(1000, self.simulate_arduino_input)  # Simulate new input every second

        # Example condition to switch to the next app
        if len(self.output_text.get("1.0", tk.END).strip().split('\n')) > 10:
            self.switch_to_maze_app()


class MazeApp(tk.Toplevel):
    def __init__(self, master, switch_to_morse_app):
        super().__init__(master)
        self.title("Maze App")
        self.geometry("800x600")
        self.switch_to_morse_app = switch_to_morse_app

        # Add maze app logic here

    def close_app(self):
        self.switch_to_morse_app()


class MorseApp(tk.Toplevel):
    def __init__(self, master, finish_callback):
        super().__init__(master)
        self.title("Morse App")
        self.geometry("800x600")
        self.finish_callback = finish_callback

        # Add morse app logic here

    def close_app(self):
        self.finish_callback()


def Engeenering(parent):
    def switch_to_maze_app():
        logic_gate_app.destroy()
        global maze_app
        maze_app = MazeApp(parent, switch_to_morse_app)
        maze_app.mainloop()

    def switch_to_morse_app():
        maze_app.destroy()
        global morse_app
        morse_app = MorseApp(parent, finish_callback)
        morse_app.mainloop()

    def finish_callback():
        morse_app.destroy()
        end_time = time.time()
        duration = end_time - start_time
        name = simpledialog.askstring("Input", "Enter your team name:")
        if name:
            with open("results.txt", "a") as file:
                file.write(f"Team: {name}, Time: {duration} seconds\n")

    start_time = time.time()
    global logic_gate_app
    logic_gate_app = LogicGateApp(parent, switch_to_maze_app)
    logic_gate_app.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    Engeenering(root)
    root.mainloop()
