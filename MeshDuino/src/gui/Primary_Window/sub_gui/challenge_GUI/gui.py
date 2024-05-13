from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox
import threading


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def Challenge(parent):
    
    canvas = Canvas(
        parent,
        bg = "#FFFFFF",
        height = 405,
        width = 675,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    


    def round_rectangle(x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1+radius, y1,
                x1+radius, y1,
                x2-radius, y1,
                x2-radius, y1,
                x2, y1,
                x2, y1+radius,
                x2, y1+radius,
                x2, y2-radius,
                x2, y2-radius,
                x2, y2,
                x2-radius, y2,
                x2-radius, y2,
                x1+radius, y2,
                x1+radius, y2,
                x1, y2,
                x1, y2-radius,
                x1, y2-radius,
                x1, y1+radius,
                x1, y1+radius,
                x1, y1]

        return canvas.create_polygon(points, **kwargs, smooth=True)


    canvas.place(x = 230, y = 72)


    #engeenering
    global challange_coding_button_image
    challange_coding_button_image = PhotoImage(file=relative_to_assets("image_coding.png"))
    Button(
        image=challange_coding_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: threading.Thread(args=("engeenering",parent),daemon=True).start(),
        relief="flat",
        activebackground="#FFFFFF",
        activeforeground="#FFFFFF"
        ).place(x=284, y=140, width=117, height=112)




    #physics
    global challange_lofi_button_image
    challange_lofi_button_image = PhotoImage(file=relative_to_assets("image_lofi.png"))
    Button(
        image=challange_lofi_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: threading.Thread(args=("lofi",parent),daemon=True).start(),
        relief="flat",
        activebackground="#FFFFFF",
        activeforeground="#FFFFFF"
        ).place(x=468, y=140, width=117, height=112)


    #Sounds
    global challange_bass_button_image
    challange_bass_button_image = PhotoImage(file=relative_to_assets("image_bass.png"))
    Button(
        image=challange_bass_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: threading.Thread( args=("Sounds",parent),daemon=True).start(),
        relief="flat",
        activebackground="#FFFFFF",
        activeforeground="#FFFFFF"
        ).place(x=643, y=140, width=117, height=112)

    

    #Add leaderboard
    '''round_rectangle(52,267,170,375,fill="#171435",outline="")'''
    global challange_add_button_image
    challange_add_button_image = PhotoImage(file=relative_to_assets("image_2.png"))
    Button(
        image=challange_add_button_image,
        borderwidth=0,
        highlightthickness=0,
        relief="flat",
        activebackground="#FFFFFF",
        activeforeground="#FFFFFF"
        ).place(x=284, y=335, width=117, height=112)

    canvas.create_text(
        52.0,
        212.0,
        anchor="nw",
        text="Suggest New Challenge :",
        fill="#3b5e74",
        font=("Montserrat Bold", 32 * -1)
    )

    global leaderboard_image_1
    leaderboard_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    canvas.create_image(
        342.0,
        201.99993896484375,
        image=leaderboard_image_1
    )

    canvas.create_text(
        52.0,
        21.0,
        anchor="nw",
        text="Challenges :",
        fill="#3b5e74",
        font=("Montserrat Bold", 32 * -1)
    )
