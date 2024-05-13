import tkinter as tk
from tkinter import PhotoImage, Canvas, Entry, Button, messagebox
from tkinter.constants import DISABLED
import threading
from pathlib import Path



OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def download_thread(link):
    print("Downloading", link)
    # Download the link here
    


def Download_button_clicked(root):
    link = home_entrybox.get()
    if link:
        threading.Thread(target=download_thread, args=(link,), daemon=True).start()
        home_entrybox.delete(0, "end")
    else:
        messagebox.showerror("Error", "Please enter a valid link")

def Home(parent):
    canvas = Canvas(
        parent,
        bg = "#FFFFFF",
        height = 405,
        width = 675,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 230, y = 72)

    global home_entrybox
    home_entrybox=Entry()
    home_entrybox.place(x=320, y=275, width=500, height=40)
    home_entrybox.configure(font=("Montserrat Bold", 20 * -1),relief="flat",borderwidth="0",fg="#171435")

    global entrybox_image
    entrybox_image = PhotoImage(file=relative_to_assets("image_1.png"))
    canvas.create_image(341,210,image=entrybox_image)


    global home_button_image_1
    home_button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    Button(
        image=home_button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: threading.Thread(args=(parent,),daemon=True).start(),
        relief="flat",
        bg='#FFFFFF',
        activebackground='#FFFFFF').place(
            x=460.0,y=390.0,width=190.0,height=48.0)


    canvas.create_text(
        90.0,
        58.0,
        anchor="nw",
        text="Download A Song Right Now!",
        fill="#C67FFC",
        font=("Montserrat Bold", 32 * -1)
    )
    canvas.create_text(
        130.0,
        100.0,
        anchor="nw",
        text="And Enjoy Playing it From our Playlist Tab",
        fill="#C67FFC",
        font=("Montserrat Bold", 18 * -1)
    )