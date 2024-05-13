from pathlib import Path
import threading
from tkinter import *
from xml.dom import IndexSizeErr

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def random_button_clicked():
    print("Random button clicked")

import tkinter as tk
from tkinter import ttk


def Leaderboard(parent):
    canvas = Canvas(
    parent,
    bg = "#FFFFFF",
    height = 405,
    width = 675,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")


    
    canvas.place(x = 230, y = 72)
    
    global playlist_bar_image
    playlist_bar_image = PhotoImage(file=relative_to_assets("image_2.png"))
    canvas.create_image(190.0,65.0,image=playlist_bar_image)

    canvas.create_text(
        36.0,
        22.0,
        anchor="nw",
        text="Below is the Currently Playing Playlist",
        fill="#C67FFC",
        font=("Montserrat Bold", 26 * -1)
    )


    
    global playlist_background_image
    playlist_background_image = PhotoImage(file=relative_to_assets("image_1.png"))
    canvas.create_image(335,220,image=playlist_background_image)



    canvas.create_text(
        36.0,
        65.0,
        anchor="nw",
        text="using this You can Choose which song to play !",
        fill="#C67FFC",
        font=("Montserrat SemiBold", 15 * -1)
    )

    global playlist_button_image_1
    playlist_button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    Button(
        image=playlist_button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: threading.Thread(target=random_button_clicked, daemon=True).start(),
        relief="flat",
        bg='#FFFFFF',
        activebackground='#FFFFFF'
    ).place(
        x=485.0,
        y=425.0,
        width=141.0,
        height=39.0
    )


    global playlist_button_image_2
    playlist_button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    Button(
        image=playlist_button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: random_button_clicked(),
        relief="flat",
        bg='#FFFFFF',
        activebackground='#FFFFFF'
    ).place(
        x=650.0,
        y=418.0,
        width=65.0,
        height=55.0
    )