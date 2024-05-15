import tkinter as tk
from tkinter import Canvas, Text, simpledialog
from PIL import Image, ImageTk
import random
import time
import serial
import pygame
from threading import Thread, Event
from pathlib import Path
import sys
from utils.character import Character
from utils.graph import Graph

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

        self.arduino_serial = None
        try:
            self.arduino_serial = serial.Serial('COM11', 9600)
        except serial.SerialException:
            print("Port not open. Is this a test? (yes/no)")
            user_input = input().strip().lower()
            if user_input == 'yes':
                self.is_test = True
            else:
                print("Stopping the application.")
                self.is_test = False
                self.destroy()
        else:
            self.is_test = False

        self.pause_event = Event()
        self.pause_event.set()

    def load_images(self):
        self.schematic_image = Image.open(relative_to_assets("logic_gate_schematic.png"))
        self.schematic_photo = ImageTk.PhotoImage(self.schematic_image)

    def create_widgets(self):
        self.canvas.create_image(50, 50, image=self.schematic_photo, anchor=tk.NW)

        self.output_text = Text(self, height=10, width=30, state=tk.DISABLED)
        self.canvas.create_window(600, 170, window=self.output_text)

        self.terminal_text = Text(self, height=10, width=80, state=tk.DISABLED)
        self.canvas.create_window(400, 400, window=self.terminal_text)

        self.read_serial_button = tk.Button(self, text="Start Experiment 1", command=self.start_experiment_1,
                                            bg='#4CAF50', fg='white', font=('Helvetica', 12, 'bold'),
                                            activebackground='#45a049', bd=0, padx=10, pady=5)
        self.read_serial_button.place(x=320, y=550)
        self.read_serial_button.bind("<Enter>", self.on_enter)
        self.read_serial_button.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        e.widget['background'] = '#45a049'

    def on_leave(self, e):
        e.widget['background'] = '#4CAF50'

    def start_experiment_1(self):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete('1.0', tk.END)

        gates = ['NotGate', 'OrGate', 'AndGate', 'NorGate', 'NandGate', 'XorGate', 'XnorGate']
        selected_gates = random.sample(gates, 4)
        input_states = ['LOW', 'HIGH', 'LOW', 'HIGH']

        experiment_text = "\n".join([f"{gate}: {state}" for gate, state in zip(selected_gates, input_states)])
        self.output_text.insert(tk.END, experiment_text)
        self.output_text.config(state=tk.DISABLED)

        if self.is_test:
            print("Simulating sending command to Arduino...")
            print("Start Experiment 1\n" + experiment_text)
            self.log_to_terminal(f"Start Experiment 1\n{experiment_text}")
            Thread(target=self.simulate_experiment_success).start()
        else:
            self.send_experiment_command(selected_gates, input_states)
            self.monitor_serial_for_success()

    def send_experiment_command(self, gates, states):
        command = "Start Experiment 1\n" + "\n".join([f"{gate}:{state}" for gate, state in zip(gates, states)])
        self.arduino_serial.write(command.encode())
        self.log_to_terminal(command)

    def monitor_serial_for_success(self):
        def read_serial():
            while True:
                if self.arduino_serial.in_waiting > 0:
                    my_data = self.arduino_serial.readline().decode().strip()
                    self.log_to_terminal(my_data)
                    if "Experiment 1 Success" in my_data:
                        self.display_success_message()
                        break

        self.serial_thread = Thread(target=read_serial, daemon=True)
        self.serial_thread.start()

    def simulate_experiment_success(self):
        time.sleep(5)
        self.log_to_terminal("Experiment 1 Success")
        self.display_success_message()

    def display_success_message(self):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, "\nExperiment 1 Success")
        self.output_text.config(state=tk.DISABLED)

        self.read_serial_button.config(text="Start Experiment 2", command=self.start_experiment_2)

    def start_experiment_2(self):
        self.switch_to_maze_app()

    def log_to_terminal(self, message):
        self.terminal_text.config(state=tk.NORMAL)
        self.terminal_text.insert(tk.END, message + '\n')
        self.terminal_text.config(state=tk.DISABLED)
        self.terminal_text.see(tk.END)

    def simulate_arduino_input(self):
        gates = ['NotGate', 'OrGate', 'AndGate', 'NorGate', 'NandGate', 'XorGate', 'XnorGate']
        gate = random.choice(gates)
        output = random.choice(['HIGH', 'LOW'])
        simulated_data = f"Gate: {gate}, Output: {output}\n"

        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, simulated_data)
        self.output_text.config(state=tk.DISABLED)

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

    def on_enter(self, e):
        e.widget['background'] = '#45a049'

    def on_leave(self, e):
        e.widget['background'] = '#4CAF50'

    def start_maze_game(self):
        self.start_button.destroy()
        Thread(target=self.run_maze_game).start()

    def run_maze_game(self):
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
            cooldown = 100
            start_timer = pygame.time.get_ticks()
            carryOn = True
            while carryOn:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        carryOn = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            carryOn = False
                keys = pygame.key.get_pressed()
                if pygame.time.get_ticks() - start_timer > cooldown:
                    current_point = player.get_current_position()
                    next_point = None
                    if keys[pygame.K_RIGHT] and (current_point[0] + 1, current_point[1]) in vertices and maze.is_edge((current_point, (current_point[0] + 1, current_point[1]))):
                        next_point = (current_point[0] + 1, current_point[1])
                    elif keys[pygame.K_LEFT] and (current_point[0] - 1, current_point[1]) in vertices and maze.is_edge((current_point, (current_point[0] - 1, current_point[1]))):
                        next_point = (current_point[0] - 1, current_point[1])
                    elif keys[pygame.K_UP] and (current_point[0], current_point[1] - 1) in vertices and maze.is_edge((current_point, (current_point[0], current_point[1] - 1))):
                        next_point = (current_point[0], current_point[1] - 1)
                    elif keys[pygame.K_DOWN] and (current_point[0], current_point[1] + 1) in vertices and maze.is_edge((current_point, (current_point[0], current_point[1] + 1))):
                        next_point = (current_point[0], current_point[1] + 1)
                    if next_point:
                        player.move_character(next_point)
                    if player.reached_goal():
                        carryOn = False
                        self.switch_to_morse_app()
                    start_timer = pygame.time.get_ticks()
                pygame.display.update()
            pygame.quit()
        
        runGame(self.grid_size, self.side_length)


class MorseApp(tk.Toplevel):
    def __init__(self, master, finish_callback):
        super().__init__(master)
        self.title("Morse App")
        self.geometry("800x600")
        self.finish_callback = finish_callback

        self.canvas = Canvas(self, bg="#FFFFFF", width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.create_widgets()
        self.start_time = time.time()

        self.arduino_serial = None
        try:
            self.arduino_serial = serial.Serial('COM11', 9600)
        except serial.SerialException:
            print("Port not open. Is this a test? (yes/no)")
            user_input = input().strip().lower()
            if user_input == 'yes':
                self.is_test = True
            else:
                print("Stopping the application.")
                self.is_test = False
                self.destroy()
        else:
            self.is_test = False

        self.pause_event = Event()
        self.pause_event.set()

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

        if self.is_test:
            print("Simulating sending command to Arduino...")
            print("Start Experiment 3\n" + word)
            self.log_to_terminal(f"Start Experiment 3\n{word}")
            Thread(target=self.simulate_experiment_success).start()
        else:
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
                if self.arduino_serial.in_waiting > 0:
                    my_data = self.arduino_serial.readline().decode().strip()
                    self.log_to_terminal(my_data)
                    if "Experiment 3 Success" in my_data:
                        self.display_success_message()
                        break

        self.serial_thread = Thread(target=read_serial, daemon=True)
        self.serial_thread.start()

    def simulate_experiment_success(self):
        time.sleep(5)
        self.log_to_terminal("Experiment 3 Success")
        self.display_success_message()

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
