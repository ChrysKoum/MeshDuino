from pathlib import Path
import threading
from tkinter import *
from tkinter import ttk
import os
import firebase_admin
from firebase_admin import credentials, db


# Path to your service account key file
service_account_path = os.path.join(
    os.path.dirname(__file__), 'serviceAccountKey.json'
)

# Initialize the app with a service account, granting admin privileges
cred = credentials.Certificate(service_account_path)
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://meshduino-6af30-default-rtdb.europe-west1.firebasedatabase.app"
})



OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def random_button_clicked():
    print("Random button clicked")

def format_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    return f"{int(minutes):02}:{int(seconds):02}"

def fetch_ranking_data():
    ranking_data = []
    leaderboard_ref = db.reference('leaderboard')
    data = leaderboard_ref.get()
    if data:
        for key, value in data.items():
            team_name = value.get('team', 'Unknown')
            times = value.get('times', [])
            # Ensure times are converted to "MM:SS" format
            logic_gates_time = format_time(times[0]) if len(times) > 0 else "00:00"
            maze_time = format_time(times[1]) if len(times) > 1 else "00:00"
            morse_time = format_time(times[2]) if len(times) > 2 else "00:00"
            total_duration = format_time(value.get('total_duration', 0))
            ranking_data.append((team_name, logic_gates_time, maze_time, morse_time, total_duration))
        # Sort ranking data by total time
        ranking_data.sort(key=lambda x: int(x[4].split(":")[0]) * 60 + int(x[4].split(":")[1]))
        # Add ranks
        ranking_data_with_ranks = [(idx + 1, *data) for idx, data in enumerate(ranking_data)]
        return ranking_data_with_ranks
    return []

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

    def load_data():
        ranking_data = fetch_ranking_data()
        for item in ranking_data:
            table.insert('', 'end', values=item)

    table.place(x=265, y=170)
    load_data()

if __name__ == "__main__":
    root = Tk()
    root.geometry("1024x768")
    Leaderboard(root)
    root.mainloop()