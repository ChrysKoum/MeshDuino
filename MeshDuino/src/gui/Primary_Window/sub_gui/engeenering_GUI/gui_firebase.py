import tkinter as tk
from tkinter import ttk, simpledialog, PhotoImage, Canvas, Button, Toplevel, Label, Text, messagebox
from PIL import Image, ImageTk
from tkinter.constants import DISABLED, LEFT
import random
import serial
import pygame
import time
from threading import Thread, Event
from pathlib import Path
import sys
from serial.tools import list_ports
import os
from dotenv import load_dotenv

# from utils.character import Character
# from utils.graph import Graph
from backend.maze_handler.character import Character
from backend.maze_handler.graph import Graph

# Firebase
import firebase_admin
from firebase_admin import credentials, db

# Global variables
logic_gate_app = None
maze_app = None
morse_app = None
start_time = None
time_array = []
# Morse code dictionary
MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
    'Z': '--..'
}
words = [
    'APPLE', 'GRAPE', 'PEACH', 'LEMON', 'BERRY',
    'MANGO', 'PLUMS', 'OLIVE', 'PEARS', 'APRIC',
    'KIWIS', 'DATES', 'BEETS', 'CARRO', 'CHILI',
    'GUAVA', 'RADIC', 'CHARD', 'KALES', 'LEEKS',
    'LIMES', 'MELON', 'ONION', 'RAISN', 'TOMAT'
]

# Function to make an Arduino connection
def make_arduino_connection(port, baudrate, simulation_mode=False):
    if simulation_mode:
        print("Simulation mode activated. No actual serial connection will be made.")
        return None  # Return None to indicate simulation mode
    try:
        arduino_serial = serial.Serial(port, baudrate)
        time.sleep(2)  # Wait for the connection to establish
        return arduino_serial
    except serial.SerialException as e:
        print(f"Port not open. Error: {e}")
        sys.exit()


# Function to get the available serial ports
def get_serial_ports():
    ports = list_ports.comports()
    return [port.device for port in ports]

def EngeeneringApp(parent):
    ports = get_serial_ports()
    port_selection_window = Toplevel(parent)
    port_selection_window.title("Select Serial Port")
    port_selection_window.geometry("400x300")
    port_selection_window.configure(bg="#F0F0F0")
    port_selection_window.iconbitmap(relative_to_assets("minilogo.ico"))
    
    # Title label
    title_label = Label(port_selection_window, text="Select Serial Port", font=("Montserrat Bold", 16), bg="#F0F0F0", fg="#C67FFC")
    title_label.pack(pady=20)
    
    global start_time
    start_time = time.time()

    # Serial port selection combobox
    serial_port = tk.StringVar()
    port_combobox = ttk.Combobox(port_selection_window, textvariable=serial_port, values=ports)
    port_combobox.pack(pady=10, padx=20)
    
    # Simulation mode checkbutton
    simulation_mode = tk.BooleanVar()
    simulation_checkbutton = tk.Checkbutton(port_selection_window, text="Simulation Mode", variable=simulation_mode, onvalue=True, offvalue=False, bg="#F0F0F0", fg="#C67FFC", font=("Helvetica", 12))
    simulation_checkbutton.pack(pady=10)

    def on_port_selected():
        if simulation_mode.get():
            serial_port.set("Simulation")  # Use "Simulation" to indicate simulation mode
        if serial_port.get():
            port_selection_window.destroy()
            logic_gate_app = LogicGateApp(parent, switch_to_maze_app, serial_port.get(), simulation_mode.get())
            logic_gate_app.mainloop()
            # maze_app = MazeApp(parent, serial_port.get(), None,  simulation_mode.get())
            # maze_app.mainloop()
            # morse_app = MorseApp(parent, serial_port.get(), finish_callback,  None, simulation_mode.get())
            # morse_app.mainloop()
        else:
            messagebox.showerror("Selection Error", "Please select a serial port.")

    ok_button = Button(port_selection_window, text="OK", command=on_port_selected, bg='#4CAF50', fg='white', font=('Helvetica', 12, 'bold'))
    ok_button.pack(pady=20)

# Define the relative_to_assets function
def relative_to_assets(path: str) -> Path:
    return Path(__file__).parent / "assets" / Path(path)

class LogicGateApp(tk.Toplevel):
    def __init__(self, master, switch_to_maze_app, serial_port, simulation_mode=False):
        super().__init__(master)
        self.title("Networked Digital Logic Gates")
        self.geometry("800x600")
        self.switch_to_maze_app = switch_to_maze_app
        self.serial_port = serial_port
        self.simulation_mode = simulation_mode
        self.arduino_serial = make_arduino_connection(self.serial_port, 9600, simulation_mode)
        self.iconbitmap(relative_to_assets("minilogo.ico"))

        self.canvas = Canvas(self, bg="#FFFFFF", width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.load_images()
        self.create_widgets()

        self.pause_event = Event()
        self.pause_event.set()

    def load_images(self):
        self.schematic_image = PhotoImage(file=relative_to_assets("logic_gate_schematic.png"))

    def create_widgets(self):
        self.canvas.create_image(50, 50, image=self.schematic_image, anchor=tk.NW)

        self.output_text = Text(self, height=10, width=30, state=DISABLED)
        self.canvas.create_window(600, 170, window=self.output_text)

        self.terminal_text = Text(self, height=10, width=80, state=DISABLED)
        self.canvas.create_window(400, 400, window=self.terminal_text)

        self.read_serial_button = Button(self, text="Start Experiment 1", command=self.start_experiment_1,
                                         bg='#4CAF50', fg='white', font=('Helvetica', 12, 'bold'),
                                         activebackground='#45a049', bd=0, padx=10, pady=5)
        self.read_serial_button.place(x=320, y=550)
        self.read_serial_button.bind("<Enter>", self.on_enter)
        self.read_serial_button.bind("<Leave>", self.on_leave)

        # Help button
        self.help_button = Button(self, text="Help", command=self.show_help,
                                  bg='#2196F3', fg='white', font=('Helvetica', 12, 'bold'),
                                  activebackground='#1E88E5', bd=0, padx=10, pady=5)
        self.help_button.place(x=720, y=20)
        self.help_button.bind("<Enter>", self.on_enter_help)
        self.help_button.bind("<Leave>", self.on_leave_help)

    def on_enter(self, e):
        e.widget['background'] = '#45a049'

    def on_leave(self, e):
        e.widget['background'] = '#4CAF50'

    def on_enter_help(self, e):
        e.widget['background'] = '#1E88E5'

    def on_leave_help(self, e):
        e.widget['background'] = '#2196F3'

    def display_success_message(self):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, "\nExperiment 1 Finish")
        self.output_text.config(state=tk.DISABLED)

        self.read_serial_button.config(text="Start Experiment 2", command=self.start_experiment_2)

    def send_command_and_wait_for_response(self, command, expected_response):
        def task():
            print(f"Sending command: {command}")
            self.log_to_terminal(f"Sending command: {command}")
            if self.simulation_mode:
                print(f"Simulating response for command: {command}")
                simulated_responses = {
                    '1': "Experiment 1 Start",
                    'NotGate': "Experiment 1 Finish",
                }
                time.sleep(1)  # Simulate delay
                response = simulated_responses.get(command, "")
                self.log_to_terminal(f"Simulated response: {response}")
            else:
                self.arduino_serial.write(command.encode())
                response = ""
                while True:
                    if self.arduino_serial.inWaiting() > 0:
                        time.sleep(1)  # Wait for the data to be available
                        response = self.arduino_serial.readline().decode('utf-8').strip()
                        print(f"Received response: {response}")
                        self.log_to_terminal(f"Received response: {response}")
                        if response == expected_response:
                            break
            return response

        thread = Thread(target=task)
        thread.start()

    def start_experiment_1(self):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete('1.0', tk.END)

        gates = ['NotGate', 'OrGate', 'AndGate', 'NorGate', 'NandGate', 'XorGate', 'XnorGate']
        selected_gate = random.sample(gates, 1)[0]

        self.output_text.insert(tk.END, f"Selected gate: {selected_gate}\n")
        self.output_text.config(state=tk.DISABLED)

        if not self.simulation_mode:
            self.arduino_serial.write(b'1')  # Send signal to Arduino to start experiment
        self.send_experiment_command(selected_gate)

    def send_experiment_command(self, gate):
        def send_and_wait(gate):
            command = gate
            expected_response = "Experiment 1 Finish"
            print(f"Sending command: {command}")
            self.log_to_terminal(f"Sending command: {command}")
            print(f"Waiting for response: {expected_response}")
            self.send_command_and_wait_for_response(command, expected_response)
            self.log_to_terminal(f"Sent: {command}")
            self.log_to_terminal(f"Waiting for: {expected_response}")

        self.after(100, send_and_wait, gate)  # Delay to avoid blocking

        self.monitor_serial_for_success()

    def monitor_serial_for_success(self):
        def read_serial():
            if self.simulation_mode:
                time.sleep(1)  # Simulate delay
                self.log_to_terminal("Experiment 1 Finish")
                self.display_success_message()
            else:
                while True:
                    if self.arduino_serial.inWaiting() > 0:
                        time.sleep(0.4)  # Add a small delay to ensure all incoming messages are read
                        my_data = self.arduino_serial.readline().decode('utf-8').strip()
                        self.log_to_terminal(my_data)
                        if "Experiment 1 Finish" in my_data:
                            self.display_success_message()
                            break

        self.serial_thread = Thread(target=read_serial, daemon=True)
        self.serial_thread.start()

    def display_success_message(self):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, "\nExperiment 1 Finish")
        self.output_text.config(state=tk.DISABLED)

        self.read_serial_button.config(text="Start Experiment 2", command=self.start_experiment_2)

    def start_experiment_2(self):
        global start_time
        global time_array
        time_array.append(time.time() - start_time)
        start_time = time.time()
        self.switch_to_maze_app(self, self.serial_port, self.arduino_serial, self.simulation_mode)

    def log_to_terminal(self, message):
        def update_terminal():
            self.terminal_text.config(state=tk.NORMAL)
            self.terminal_text.insert(tk.END, message + '\n')
            self.terminal_text.config(state=tk.DISABLED)
            self.terminal_text.see(tk.END)

        self.after(0, update_terminal)

    def show_help(self):
        help_window = Toplevel(self)
        help_window.title("Help")
        help_window.geometry("700x500")
        help_window.configure(bg="#FFFFFF")

        Label(help_window, text="Help and Support", font=("Montserrat Bold", 24), fg="#171435", bg="#FFFFFF").pack(pady=10)

        help_text = """
        Welcome to Meshduino!

        Meshduino is an Arduino network integrated with Python, featuring a GUI.

        Sections:
        - Home: Introduction to Meshduino and its features.
        - Challenges: View and participate in available challenges.
        - Leaderboard: See the best times and rankings of teams.
        - About Us: Learn more about our team.

        For further assistance, please contact us at:
        support@meshduino.com

        Future Products and Tutorials:
        - Detailed guides for Users/Parents/Teachers.
        - Comprehensive tutorials for Students to master challenges.
        """

        Label(help_window, text=help_text, font=("Montserrat", 14), fg="#171435", bg="#FFFFFF", justify=LEFT, wraplength=580).pack(pady=10, padx=20)

class MazeApp(tk.Toplevel):
    def __init__(self, master, serial_port, arduino_serial=None, simulation_mode=False):
        super().__init__(master)
        self.title("Maze Challenge")
        self.geometry("800x600")
        self.iconbitmap(relative_to_assets("minilogo.ico"))

        self.serial_port = serial_port
        self.simulation_mode = simulation_mode
        print(f"Selected serial port: {self.serial_port}")
        if arduino_serial is None:
            self.arduino_serial = make_arduino_connection(self.serial_port, 9600, simulation_mode)
        else:
            self.arduino_serial = arduino_serial

        self.grid_size = 7
        self.side_length = 7
        self.mode = 0  # Solo mode

        self.canvas = tk.Canvas(self, bg="#FFFFFF", width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.create_widgets()

        self.pause_event = Event()
        self.pause_event.set()

        if self.simulation_mode:
            self.bind_all("<Key>", self.simulate_keypress)
        
    def create_widgets(self):
        self.terminal_text = Text(self, height=10, width=80, state=DISABLED)
        self.canvas.create_window(400, 400, window=self.terminal_text)

        self.start_button = tk.Button(self, text="Start Experiment 2", command=self.start_maze_game,
                                      bg='#4CAF50', fg='white', font=('Helvetica', 12, 'bold'),
                                      activebackground='#45a049', bd=0, padx=10, pady=5)
        self.start_button.place(x=320, y=550)
        self.start_button.bind("<Enter>", self.on_enter)
        self.start_button.bind("<Leave>", self.on_leave)

    def log_to_terminal(self, message):
        def update_terminal():
            self.terminal_text.config(state=tk.NORMAL)
            self.terminal_text.insert(tk.END, message + '\n')
            self.terminal_text.config(state=tk.DISABLED)
            self.terminal_text.see(tk.END)

        self.after(0, update_terminal)

    def switch_to_morse_app(self, serial_port, arduino_serial, simulation_mode=False):
        global maze_app
        if maze_app is not None:
            maze_app.destroy()
            maze_app = None  # Ensure reference is cleared
        global start_time
        global time_array
        time_array.append(time.time() - start_time)
        start_time = time.time()
        global morse_app
        morse_app = MorseApp(self.master, serial_port, finish_callback, arduino_serial, simulation_mode)
        morse_app.mainloop()

    def start_experiment_2(self):
        if not self.simulation_mode:
            self.arduino_serial.write(b'2')  

    def on_enter(self, e):
        e.widget['background'] = '#45a049'

    def on_leave(self, e):
        e.widget['background'] = '#4CAF50'

    def start_maze_game(self):
        self.start_button.destroy()
        self.start_experiment_2()
        self.run_maze_game()

    def run_maze_game(self):
        # Run Pygame in a separate thread
        Thread(target=self.run_pygame_maze_game, daemon=True).start()

    def handle_key_press(self, event, player, vertices, maze):
        move = None
        current_point = player.get_current_position()
        next_point = None

        if event.key == pygame.K_RIGHT and (current_point[0] + 1, current_point[1]) in vertices and maze.is_edge((current_point, (current_point[0] + 1, current_point[1]))):
            move = "Right"
            next_point = (current_point[0] + 1, current_point[1])
        elif event.key == pygame.K_LEFT and (current_point[0] - 1, current_point[1]) in vertices and maze.is_edge((current_point, (current_point[0] - 1, current_point[1]))):
            move = "Left"
            next_point = (current_point[0] - 1, current_point[1])
        elif event.key == pygame.K_UP and (current_point[0], current_point[1] - 1) in vertices and maze.is_edge((current_point, (current_point[0], current_point[1] - 1))):
            move = "Up"
            next_point = (current_point[0], current_point[1] - 1)
        elif event.key == pygame.K_DOWN and (current_point[0], current_point[1] + 1) in vertices and maze.is_edge((current_point, (current_point[0], current_point[1] + 1))):
            move = "Down"
            next_point = (current_point[0], current_point[1] + 1)

        if next_point:
            player.move_character(next_point)
            self.log_to_terminal(f"Move: {move}")
            if player.reached_goal():
                print("Maze completed")
                self.switch_to_morse_app(self.serial_port, self.arduino_serial, self.simulation_mode)

    def run_pygame_maze_game(self):
        import os

        def set_window_position(x, y):
            os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)

        def create_grid(size):
            grid = Graph()
            for i in range(size):
                for j in range(size):
                    grid.add_vertex((i, j))
            return grid

        def create_maze(grid, vertex, completed=None, vertices=None):
            if vertices is None:
                vertices = grid.get_vertices()
            if completed is None:
                completed = [vertex]
            paths = list(int(i) for i in range(4))
            random.shuffle(paths)
            up = (vertex[0], vertex[1] - 1)
            down = (vertex[0], vertex[1] + 1)
            left = (vertex[0] - 1, vertex[1])
            right = (vertex[0] + 1, vertex[1])
            for direction in paths:
                if direction == 0 and up in vertices and up not in completed:
                    grid.add_edge((vertex, up))
                    grid.add_edge((up, vertex))
                    completed.append(up)
                    create_maze(grid, up, completed, vertices)
                elif direction == 1 and down in vertices and down not in completed:
                    grid.add_edge((vertex, down))
                    grid.add_edge((down, vertex))
                    completed.append(down)
                    create_maze(grid, down, completed, vertices)
                elif direction == 2 and left in vertices and left not in completed:
                    grid.add_edge((vertex, left))
                    grid.add_edge((left, vertex))
                    completed.append(left)
                    create_maze(grid, left, completed, vertices)
                elif direction == 3 and right in vertices and right not in completed:
                    grid.add_edge((vertex, right))
                    grid.add_edge((right, vertex))
                    completed.append(right)
                    create_maze(grid, right, completed, vertices)
            return grid

        def draw_maze(screen, maze, size, colour, side_length, border_width):
            for i in range(size):
                for j in range(size):
                    if i != 0 and maze.is_edge(((i, j), (i - 1, j))):
                        pygame.draw.rect(screen, colour, [(side_length + border_width) * i, border_width + (side_length + border_width) * j, side_length + border_width, side_length])
                    if i != size - 1 and maze.is_edge(((i, j), (i + 1, j))):
                        pygame.draw.rect(screen, colour, [border_width + (side_length + border_width) * i, border_width + (side_length + border_width) * j, side_length + border_width, side_length])
                    if j != 0 and maze.is_edge(((i, j), (i, j - 1))):
                        pygame.draw.rect(screen, colour, [border_width + (side_length + border_width) * i, (side_length + border_width) * j, side_length, side_length + border_width])
                    if j != size - 1 and maze.is_edge(((i, j), (i, j + 1))):
                        pygame.draw.rect(screen, colour, [border_width + (side_length + border_width) * i, border_width + (side_length + border_width) * j, side_length, side_length + border_width])

        def draw_position(screen, side_length, border_width, current_point, colour):
            pygame.draw.rect(screen, colour, [border_width + (side_length + border_width) * current_point[0], border_width + (side_length + border_width) * current_point[1], side_length, side_length])

        def runGame(grid_size, side_length):
            pygame.init()
            BLACK = (0, 0, 0)
            WHITE = (255, 255, 255)
            GREEN = (0, 255, 0)
            RED = (255, 0, 0)
            border_width = side_length // 5
            # Scale factors for larger rendering
            scale_factor = 3
            scaled_side_length = side_length * scale_factor
            scaled_border_width = border_width * scale_factor

            grid = create_grid(grid_size)
            maze = create_maze(grid, (grid_size // 2, grid_size // 2))
            size = (grid_size * (scaled_side_length + scaled_border_width) + scaled_border_width, grid_size * (scaled_side_length + scaled_border_width) + scaled_border_width)
            screen = pygame.display.set_mode(size)
            pygame.display.set_caption("Maze Game")
            screen.fill(BLACK)
            vertices = maze.get_vertices()
            draw_maze(screen, maze, grid_size, WHITE, scaled_side_length, scaled_border_width)
            start_point = (0, 0)
            end_point = (grid_size - 1, grid_size - 1)
            player = Character(screen, scaled_side_length, scaled_border_width, vertices, start_point, end_point, start_point, GREEN, WHITE)
            draw_position(screen, scaled_side_length, scaled_border_width, end_point, RED)
            pygame.display.flip()
            carryOn = True

            while carryOn:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        carryOn = False
                    elif self.simulation_mode and event.type == pygame.KEYDOWN:
                        self.handle_key_press(event, player, vertices, maze)
                    elif not self.simulation_mode and self.arduino_serial.in_waiting > 0:
                        receivedMessage = self.arduino_serial.readline().decode().strip()
                        self.log_to_terminal(receivedMessage)  # Log received message to terminal
                        current_point = player.get_current_position()
                        next_point = None
                        if receivedMessage == "Right" and (current_point[0] + 1, current_point[1]) in vertices and maze.is_edge((current_point, (current_point[0] + 1, current_point[1]))):
                            next_point = (current_point[0] + 1, current_point[1])
                        elif receivedMessage == "Left" and (current_point[0] - 1, current_point[1]) in vertices and maze.is_edge((current_point, (current_point[0] - 1, current_point[1]))):
                            next_point = (current_point[0] - 1, current_point[1])
                        elif receivedMessage == "Up" and (current_point[0], current_point[1] - 1) in vertices and maze.is_edge((current_point, (current_point[0], current_point[1] - 1))):
                            next_point = (current_point[0], current_point[1] - 1)
                        elif receivedMessage == "Down" and (current_point[0], current_point[1] + 1) in vertices and maze.is_edge((current_point, (current_point[0], current_point[1] + 1))):
                            next_point = (current_point[0], current_point[1] + 1)
                        if next_point:
                            player.move_character(next_point)
                        if player.reached_goal():
                            carryOn = False
                            print("Maze completed")
                            self.arduino_serial.write(b'Experiment 2 Finish')
                            time.sleep(2)
                            self.switch_to_morse_app(self.serial_port, self.arduino_serial, self.simulation_mode)

                pygame.display.update()
            pygame.quit()

        runGame(self.grid_size, self.side_length)

    def simulate_keypress(self, event):
        key = event.keysym
        message_map = {
            'Right': 'Right',
            'Left': 'Left',
            'Up': 'Up',
            'Down': 'Down'
        }
        if key in message_map:
            message = message_map[key]
            self.log_to_terminal(f"Simulated {message} keypress")
            self.arduino_serial.write(message.encode())

class MorseApp(tk.Toplevel):
    def __init__(self, master, serial_port, finish_callback, arduino_serial=None, simulation_mode=False):
        super().__init__(master)
        self.title("Morse App")
        self.geometry("800x600")
        self.serial_port = serial_port
        self.simulation_mode = simulation_mode
        self.iconbitmap(relative_to_assets("minilogo.ico"))
        print(f"Selected serial port: {self.serial_port}")
        if arduino_serial is None:
            self.arduino_serial = make_arduino_connection(self.serial_port, 9600, simulation_mode)
        else:
            self.arduino_serial = arduino_serial
        self.finish_callback = lambda: finish_callback(master, self)  # Adjust callback to pass master and self

        self.canvas = Canvas(self, bg="#FFFFFF", width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.create_widgets()

    def create_widgets(self):
        self.output_text = Text(self, height=10, width=30, state=DISABLED)
        self.canvas.create_window(600, 170, window=self.output_text)

        self.terminal_text = Text(self, height=10, width=80, state=DISABLED)
        self.canvas.create_window(400, 400, window=self.terminal_text)

        self.morse_text = Text(self, height=10, width=30, state=DISABLED)
        self.canvas.create_window(200, 170, window=self.morse_text)

        self.read_serial_button = tk.Button(self, text="Start Experiment 3", command=self.start_experiment_3,
                                            bg='#4CAF50', fg='white', font=('Helvetica', 12, 'bold'),
                                            activebackground='#45a049', bd=0, padx=10, pady=5)
        self.read_serial_button.place(x=320, y=550)
        self.read_serial_button.bind("<Enter>", self.on_enter)
        self.read_serial_button.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        e.widget['background'] = '#45a049'

    def on_leave(self, e):
        e.widget['background'] = '#4CAF50'

    def start_experiment_3(self):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete('1.0', tk.END)

        word = self.select_random_word()
        self.output_text.insert(tk.END, f"Selected word: {word}\n")
        self.output_text.config(state=tk.DISABLED)

        self.send_experiment_command(word)
        self.display_morse_code(word)
        self.monitor_serial_for_success(word)

    def select_random_word(self):
        selected_word = random.choice(words)
        print(f"Selected word for decoding: {selected_word}")
        return selected_word

    def send_experiment_command(self, word):
        if self.simulation_mode:
            self.log_to_terminal("Experiment 3 Start")
            time.sleep(1)  # Simulate delay
            self.log_to_terminal(f"Sent word: {word}")
        else:
            self.arduino_serial.write(b'3')  # Send '3' to start
            self.log_to_terminal("Experiment 3 Start")
            time.sleep(5)  # Wait for the connection to establish

            self.arduino_serial.write(word.encode())  # Send the selected word
            self.log_to_terminal(f"Sent word: {word}")

    def display_morse_code(self, word):
        self.morse_text.config(state=tk.NORMAL)
        self.morse_text.delete('1.0', tk.END)
        for letter in word:
            morse_code = MORSE_CODE_DICT.get(letter.upper(), '')
            self.morse_text.insert(tk.END, f"{letter}: {morse_code}\n")
        self.morse_text.config(state=tk.DISABLED)

    def monitor_serial_for_success(self, word):
        if self.simulation_mode:
            Thread(target=self.simulate_serial_data, args=(word,), daemon=True).start()
        else:
            def read_serial():
                while True:
                    if self.arduino_serial.in_waiting > 0:
                        my_data = self.arduino_serial.readline().decode('utf-8').strip()
                        self.log_to_terminal(my_data)
                        if "Experiment 3 Finish" in my_data:
                            self.display_success_message()
                            break

            self.serial_thread = Thread(target=read_serial, daemon=True)
            self.serial_thread.start()

    def simulate_serial_data(self, word):
        for letter in word:
            morse_code = MORSE_CODE_DICT.get(letter.upper(), '')
            self.log_to_terminal(f"{letter}: {morse_code}")
            time.sleep(1)  # Simulate delay for each letter
        time.sleep(2)  # Simulate some additional delay
        self.log_to_terminal("Experiment 3 Finish")
        self.display_success_message()

    def display_success_message(self):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, "\nExperiment 3 Finish")
        self.output_text.config(state=tk.DISABLED)
        
        global start_time
        global time_array
        time_array.append(time.time() - start_time)

        self.finish_callback()

    def log_to_terminal(self, message):
        def update_terminal():
            self.terminal_text.config(state=tk.NORMAL)
            self.terminal_text.insert(tk.END, message + '\n')
            self.terminal_text.config(state=tk.DISABLED)
            self.terminal_text.see(tk.END)

        self.after(0, update_terminal)



def switch_to_maze_app(parent, serial_port, arduino_serial, simulation_mode=False):
    global logic_gate_app
    if logic_gate_app is not None:
        logic_gate_app.destroy()
        logic_gate_app = None  # Ensure reference is cleared
    global maze_app
    maze_app = MazeApp(parent, serial_port, arduino_serial, simulation_mode)
    maze_app.mainloop()



def finish_callback(root, morse_app):
    print("Experiment 3 Finish. Showing Results...")
    duration = 0
    global time_array
    for i in range(len(time_array)):
        print(f"Time taken for experiment {i+1}: {time_array[i]:.2f} seconds")
        duration += time_array[i]
    print(f"Total time taken for the whole process: {duration:.2f} seconds")

    def save_results():
        # Function to show the dialog and save results
        def show_dialog_and_save():
            name = simpledialog.askstring("Input", "Enter your team name:", parent=root)
            if name:
                # Save results to Firebase Realtime Database
                leaderboard_ref = db.reference('leaderboard')

                new_entry = {
                    'team': name,
                    'times': [t for t in time_array],
                    'total_duration': duration
                }

                leaderboard_ref.push(new_entry)

                result_window = tk.Toplevel(root)
                result_window.title("Results")
                result_window.geometry("300x200")

                result_label = tk.Label(result_window, text=f"Team {name}\nDuration: {duration:.2f} seconds")
                result_label.pack(pady=20)

                def on_ok():
                    result_window.destroy()
                    morse_app.destroy()

                ok_button = tk.Button(result_window, text="OK", command=on_ok)
                ok_button.pack(pady=20)

        # Use the `after` method to call the dialog function on the main thread
        root.after(0, show_dialog_and_save)

    # Call the save_results function to schedule the dialog display
    save_results()



if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    EngeeneringApp(root)
    root.mainloop()
