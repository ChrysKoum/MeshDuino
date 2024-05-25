        
class MazeApp(tk.Toplevel):
    def __init__(self, master, serial_port, arduino_serial = None):
        super().__init__(master)
        self.title("Maze Challenge")
        self.geometry("800x600")

        self.serial_port = serial_port 
        print(f"Selected serial port: {self.serial_port}")
        if arduino_serial is None:
            self.arduino_serial = make_arduino_connection(self.serial_port, 9600)
        else:
            self.arduino_serial = arduino_serial

        self.grid_size = 5
        self.side_length = 5
        self.mode = 0  # Solo mode

        self.canvas = tk.Canvas(self, bg="#FFFFFF", width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.create_widgets()

        self.pause_event = Event()
        self.pause_event.set()
        
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

    def switch_to_morse_app(parent, serial_port, arduino_serial):
        global maze_app
        if maze_app is not None:
            maze_app.destroy()
            maze_app = None  # Ensure reference is cleared
        global morse_app
        morse_app = MorseApp(parent, serial_port, finish_callback, arduino_serial)
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
                if self.arduino_serial.in_waiting > 0:
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
                        time.sleep(2);
                        self.switch_to_morse_app(self.serial_port, self.arduino_serial)
                pygame.display.update()
            pygame.quit()

        runGame(self.grid_size, self.side_length)
