from pathlib import Path
import threading
from tkinter import *
from tkinter import ttk
import os

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")
DATA_PATH = OUTPUT_PATH / Path("./data")  # Folder where the ranking data files are stored

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def random_button_clicked():
    print("Random button clicked")

def calculate_total_time(*times):
    total_seconds = sum(int(t.split(":")[0]) * 60 + int(t.split(":")[1]) for t in times)
    minutes, seconds = divmod(total_seconds, 60)
    return f"{minutes:02}:{seconds:02}"

def load_ranking_data(folder_path):
    ranking_data = []
    for idx, file in enumerate(sorted(os.listdir(folder_path))):
        if file.endswith(".txt"):
            with open(os.path.join(folder_path, file), "r") as f:
                lines = f.read().splitlines()
                if len(lines) >= 4:
                    team_name = lines[0]
                    logic_gates_time = lines[1]
                    maze_time = lines[2]
                    morse_time = lines[3]
                    total_time = calculate_total_time(logic_gates_time, maze_time, morse_time)
                    ranking_data.append((idx + 1, team_name, logic_gates_time, maze_time, morse_time, total_time))
    return ranking_data

def Leaderboard(parent):
    canvas = Canvas(
        parent,
        bg="#FFFFFF",
        height=405,
        width=675,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=230, y=72)

    global playlist_bar_image
    playlist_bar_image = PhotoImage(file=relative_to_assets("image_2.png"))
    canvas.create_image(190.0, 65.0, image=playlist_bar_image)

    canvas.create_text(
        36.0,
        22.0,
        anchor="nw",
        text="Below is the Currently Leaderboard!",
        fill="#C67FFC",
        font=("Montserrat Bold", 26 * -1)
    )
    canvas.create_text(
        36.0,
        65.0,
        anchor="nw",
        text="Ranking table based on the total time taken to complete all the experiments!",
        fill="#C67FFC",
        font=("Montserrat SemiBold", 15 * -1)
    )

    # Create the table using ttk.Treeview with enhanced styling
    style = ttk.Style()
    style.theme_use("clam")

    # Configure the style for the Treeview widget
    style.configure("Treeview",
                    background="#f0f0f0",
                    foreground="black",
                    rowheight=25,
                    fieldbackground="#f0f0f0",
                    font=("Helvetica", 10))

    style.configure("Treeview.Heading",
                    background="#C67FFC",
                    foreground="white",
                    font=("Helvetica", 12, "bold"))

    # Add striped rows
    style.map('Treeview',
              background=[('selected', '#C67FFC')],
              foreground=[('selected', 'white')])

    style.layout("Treeview", [
        ('Treeview.treearea', {'sticky': 'nswe'}),
        ('Treeview.padding', {'sticky': 'nswe', 'children': [
            ('Treeview.border', {'sticky': 'nswe', 'children': [
                ('Treeview', {'sticky': 'nswe'})
            ]})
        ]})
    ])

    columns = ("Rank", "Team Name", "Logic Gates Time", "Maze Time", "Morse Time", "Total Time")

    table = ttk.Treeview(parent, columns=columns, show='headings', height=8)
    table.heading("Rank", text="Rank")
    table.heading("Team Name", text="Team Name")
    table.heading("Logic Gates Time", text="Logic Gates Time")
    table.heading("Maze Time", text="Maze Time")
    table.heading("Morse Time", text="Morse Time")
    table.heading("Total Time", text="Total Time")

    table.column("Rank", anchor='center', width=50)
    table.column("Team Name", anchor='center', width=150)
    table.column("Logic Gates Time", anchor='center', width=100)
    table.column("Maze Time", anchor='center', width=100)
    table.column("Morse Time", anchor='center', width=100)
    table.column("Total Time", anchor='center', width=100)

    # Load ranking data from files and insert into the table
    ranking_data = load_ranking_data(DATA_PATH)
    for item in ranking_data:
        table.insert('', 'end', values=item)

    table.place(x=265, y=170)