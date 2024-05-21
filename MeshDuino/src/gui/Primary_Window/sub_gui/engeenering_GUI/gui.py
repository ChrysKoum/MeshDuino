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
# from utils.character import Character
# from utils.graph import Graph
from backend.maze_handler.character import Character
from backend.maze_handler.graph import Graph

# Global variables
logic_gate_app = None
maze_app = None
start_time = None

# Function to make an Arduino connection
def make_arduino_connection(port, baudrate, simulation_mode=False):
    if simulation_mode:
        print("Simulation mode activated. No actual serial connection will be made.")
        return None  # Return None to indicate simulation mode
    try:
        arduino_serial = serial.Serial(port, baudrate)
        time.sleep(2)  # Wait for the connection to establish
        return arduino_serial
    except serial.SerialException:
        print("Port not open. Testing.")
        sys.exit()


# Function to get the available serial ports
def get_serial_ports():
    ports = list_ports.comports()
    return [port.device for port in ports]

def EngeeneringApp(parent):
    ports = get_serial_ports()
    port_selection_window = Toplevel(parent)
    port_selection_window.title("Select Serial Port")
    port_selection_window.geometry("300x200")
    port_selection_window.configure(bg="#FFFFFF")

    Label(port_selection_window, text="Select Serial Port", font=("Montserrat Bold", 14), bg="#FFFFFF").pack(pady=10)

    serial_port = tk.StringVar()
    port_combobox = ttk.Combobox(port_selection_window, textvariable=serial_port, values=ports)
    port_combobox.pack(pady=10)
    
    simulation_mode = tk.BooleanVar()
    simulation_checkbutton = tk.Checkbutton(port_selection_window, text="Simulation Mode", variable=simulation_mode, onvalue=True, offvalue=False, bg="#FFFFFF")
    simulation_checkbutton.pack(pady=10)

    def on_port_selected():
        if simulation_mode.get():
            serial_port.set("Simulation")  # Use "Simulation" to indicate simulation mode
        if serial_port.get():
            port_selection_window.destroy()
            # logic_gate_app = LogicGateApp(parent, switch_to_maze_app, serial_port.get(), simulation_mode.get())
            logic_gate_app = MazeApp(parent, serial_port.get())
            logic_gate_app.mainloop()
        else:
            messagebox.showerror("Selection Error", "Please select a serial port.")

    Button(port_selection_window, text="OK", command=on_port_selected, bg='#4CAF50', fg='white', font=('Helvetica', 12, 'bold')).pack(pady=10)

def select_serial_port(parent):
    ports = get_serial_ports()
    port_selection_window = Toplevel(parent)
    port_selection_window.title("Select Serial Port")
    port_selection_window.geometry("300x200")
    port_selection_window.configure(bg="#FFFFFF")

    Label(port_selection_window, text="Select Serial Port", font=("Montserrat Bold", 14), bg="#FFFFFF").pack(pady=10)

    serial_port = tk.StringVar()
    port_combobox = ttk.Combobox(port_selection_window, textvariable=serial_port, values=ports)
    port_combobox.pack(pady=10)
    
    simulation_mode = tk.BooleanVar()
    simulation_checkbutton = tk.Checkbutton(port_selection_window, text="Simulation Mode", variable=simulation_mode, onvalue=True, offvalue=False, bg="#FFFFFF")
    simulation_checkbutton.pack(pady=10)

    def on_port_selected():
        if simulation_mode.get():
            serial_port.set("Simulation")  # Use "Simulation" to indicate simulation mode
        if serial_port.get():
            port_selection_window.destroy()
            parent.selected_serial_port = serial_port.get()
            parent.simulation_mode = simulation_mode.get()
        else:
            messagebox.showerror("Selection Error", "Please select a serial port.")

    Button(port_selection_window, text="OK", command=on_port_selected, bg='#4CAF50', fg='white', font=('Helvetica', 12, 'bold')).pack(pady=10)
    
    parent.wait_window(port_selection_window)
# Define the relative_to_assets function
def relative_to_assets(path: str) -> Path:
    return Path(__file__).parent / "assets" / Path(path)

# Function to simulate serial data from the Arduino
def simulate_serial_data(arduino_serial):
    time.sleep(1)
    responses = ["Experiment 1 Start", "Gate 1 Completed", "Gate 2 Completed", "Gate 3 Completed", "Gate 4 Completed", "Experiment 1 Finish"]
    for response in responses:
        arduino_serial.write(response.encode())
        time.sleep(1)

class LogicGateApp(tk.Toplevel):
    def __init__(self, master, switch_to_maze_app, serial_port, simulation_mode=False):
        super().__init__(master)
        self.title("Networked Digital Logic Gates")
        self.geometry("800x600")
        self.switch_to_maze_app = switch_to_maze_app
        self.serial_port = serial_port
        self.simulation_mode = simulation_mode
        self.arduino_serial = make_arduino_connection(self.serial_port, 9600, simulation_mode)

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
        messagebox.showinfo("Success", "Experiment 1 Finished")

    def send_command_and_wait_for_response(self, command, expected_response):
        print(f"Sending command: {command}")
        self.log_to_terminal(f"Sending command: {command}")
        if self.simulation_mode:
            print(f"Simulating response for command: {command}")
            simulated_responses = {
                '1': "Experiment 1 Start",
                'NotGate': "Gate 1 Completed",
                'OrGate': "Gate 2 Completed",
                'AndGate': "Gate 3 Completed",
                'NorGate': "Gate 4 Completed",
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

    def start_experiment_1(self):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete('1.0', tk.END)

        gates = ['NotGate', 'OrGate', 'AndGate', 'NorGate', 'NandGate', 'XorGate', 'XnorGate']
        selected_gates = random.sample(gates, 4)

        experiment_text = "\n".join([f"{gate}" for gate in selected_gates])
        self.output_text.insert(tk.END, experiment_text)
        self.output_text.config(state=tk.DISABLED)

        if not self.simulation_mode:
            self.arduino_serial.write(b'1')  # Send signal to Arduino to start experiment
        self.send_experiment_command(selected_gates)

    def send_experiment_command(self, gates):
        def send_and_wait(gate):
            command = gate
            expected_response = f"Gate {gates.index(gate) + 1} Completed"
            self.send_command_and_wait_for_response(command, expected_response)
            self.log_to_terminal(f"Sent: {command}")
            self.log_to_terminal(f"Waiting for: {expected_response}")

        for gate in gates:
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
        self.switch_to_maze_app(self.serial_port)

    def log_to_terminal(self, message):
        self.terminal_text.config(state=tk.NORMAL)
        self.terminal_text.insert(tk.END, message + '\n')
        self.terminal_text.config(state=tk.DISABLED)
        self.terminal_text.see(tk.END)

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
    def __init__(self, master, serial_port):
        super().__init__(master)
        self.title("Maze Challenge")
        self.geometry("800x600")
    
        self.serial_port = serial_port if serial_port else master.selected_serial_port
        
        if not self.serial_port:
            messagebox.showerror("Error", "No serial port selected.")
            self.destroy()
            return
        self.arduino_serial = make_arduino_connection(self.serial_port, 9600)

        self.grid_size = 20
        self.side_length = 20
        self.mode = 0  # Solo mode

        self.canvas = tk.Canvas(self, bg="#FFFFFF", width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.start_button = tk.Button(self, text="Start Experiment 2", command=self.start_maze_game, bg='#4CAF50', fg='white', font=('Helvetica', 12, 'bold'), activebackground='#45a049', bd=0, padx=10, pady=5)
        self.start_button.place(x=400, y=550)
        self.start_button.bind("<Enter>", self.on_enter)
        self.start_button.bind("<Leave>", self.on_leave)

        self.pause_event = Event()
        self.pause_event.set()

    def switch_to_morse_app(self, serial_port):
        self.destroy()
        morse_app = MorseApp(self.master, serial_port, self.finish_challenge)
        morse_app.mainloop()
    def start_experiment_2(self):

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
            grid = create_grid(grid_size)
            maze = create_maze(grid, (grid_size // 2, grid_size // 2))
            size = (grid_size * (side_length + border_width) + border_width, grid_size * (side_length + border_width) + border_width)
            screen = pygame.display.set_mode(size)
            pygame.display.set_caption("Maze Game")
            screen.fill(BLACK)
            vertices = maze.get_vertices()
            draw_maze(screen, maze, grid_size, WHITE, side_length, border_width)
            start_point = (0, 0)
            end_point = (grid_size - 1, grid_size - 1)
            player = Character(screen, side_length, border_width, vertices, start_point, end_point, start_point, GREEN, WHITE)
            draw_position(screen, side_length, border_width, end_point, RED)
            pygame.display.flip()
            carryOn = True
            while carryOn:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        carryOn = False
                if self.arduino_serial.in_waiting > 0:
                    receivedMessage = self.arduino_serial.readline().decode().strip()
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
                        self.switch_to_morse_app(self.serial_port)
                pygame.display.update()
            pygame.quit()
        
        runGame(self.grid_size, self.side_length)

class MorseApp(tk.Toplevel):
    def __init__(self, master, serial_port, finish_callback):
        super().__init__(master)
        self.title("Morse App")
        self.geometry("800x600")
        self.serial_port = serial_port
        self.arduino_serial = make_arduino_connection(self.serial_port, 9600)
        self.finish_callback = finish_callback

        self.canvas = Canvas(self, bg="#FFFFFF", width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.create_widgets()
        global start_time
        self.start_time = time.time()

    def create_widgets(self):
        self.output_text = Text(self, height=10, width=30, state=tk.DISABLED)
        self.canvas.create_window(600, 170, window=self.output_text)

        self.terminal_text = Text(self, height=10, width=80, state=tk.DISABLED)
        self.canvas.create_window(400, 400, window=self.terminal_text)

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

        word = self.generate_random_word()
        self.output_text.insert(tk.END, word)
        self.output_text.config(state=tk.DISABLED)

        self.send_experiment_command(word)
        self.monitor_serial_for_success()

    def generate_random_word(self, length=5):
        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        return ''.join(random.choice(letters) for _ in range(length))

    def send_experiment_command(self, word):
        command = "Start Experiment 3\n" + word
        self.arduino_serial.write(command.encode())
        self.log_to_terminal(command)

    def monitor_serial_for_success(self):
        def read_serial():
            while True:
                if self.arduino_serial.inWaiting() > 0:
                    my_data = self.arduino_serial.readline().decode('utf-8').strip()
                    self.log_to_terminal(my_data)
                    if "Experiment 3 Success" in my_data:
                        self.display_success_message()
                        break

        self.serial_thread = Thread(target=read_serial, daemon=True)
        self.serial_thread.start()

    def display_success_message(self):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, "\nExperiment 3 Success")
        self.output_text.config(state=tk.DISABLED)
        self.finish_callback()

    def log_to_terminal(self, message):
        self.terminal_text.config(state=tk.NORMAL)
        self.terminal_text.insert(tk.END, message + '\n')
        self.terminal_text.config(state=tk.DISABLED)
        self.terminal_text.see(tk.END)

def switch_to_maze_app(parent, serial_port):
    logic_gate_app.destroy()
    global maze_app
    maze_app = MazeApp(parent, serial_port)
    maze_app.mainloop()

def switch_to_morse_app(parent, serial_port):
    maze_app.destroy()
    global morse_app
    morse_app = MorseApp(parent, serial_port, finish_callback)
    morse_app.mainloop()


def finish_callback():
    global start_time
    end_time = time.time()
    duration = end_time - start_time
    print(f"Total time taken for the whole process: {duration:.2f} seconds")
    name = simpledialog.askstring("Input", "Enter your team name:")
    if name:
        with open("results.txt", "a") as file:
            file.write(f"Team: {name}, Time: {duration} seconds\n")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    EngeeneringApp(root)
    root.mainloop()